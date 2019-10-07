#The teacher modes of the program: functionSelection, editFunction, createFunction
#This file establishes the graphics for these modes as well as updating the appropriate tables with information about new, edited, or deleted functions
#Note: the editFunction mode serves as a dispatcher for more specific function editting modes (in the FunctionEditor file)

####################################
#sqlite 3
####################################

import sqlite3

conn = sqlite3.connect('termproject.db')
c = conn.cursor()
    
def createFunctionTable(functionName):
    #creates table to store description, sampleCode, prompts for particular function
    command = """CREATE TABLE IF NOT EXISTS %s (inputType TEXT, lineNum REAL, lineType TEXT, lineText TEXT)""" %(functionName)
    c.execute(command)

def dataEntryFunction(courseCode, functionName):
    #adds function to list of functions for a given course
    c.execute("""INSERT INTO %s VALUES('%s')""" % ("a" + str(courseCode), functionName))
    createFunctionTable(functionName)
    conn.commit()
    
def readFunctionList(courseCode):
    #returns function list for a given course
    c.execute("""SELECT * FROM %s""" %("a" + str(courseCode)))
    data = c.fetchall()
    realdata = []
    for element in data:
        realdata.append(element[0])
    return realdata
    
def removeTable(functionName):
    #removes table if function is removed from class
    c.execute("""DROP TABLE IF EXISTS %s""" %(functionName))
    
def removeElement(table, element):
    #removes function from list of functions for a given course
    c.execute("""DELETE FROM %s WHERE funcName = '%s'""" %("a" + table, element))
    conn.commit()
    
def getDescription(functionName):
    #returns the description of a particular function
    command = """SELECT lineText FROM %s WHERE inputType = 'description'""" %(functionName)
    c.execute(command)
    description = c.fetchone()
    return description

####################################
# helper functions
####################################

def centerOfRectangle(values):
    #aligns text in center
    x = values[0] + values[2]
    y = values[1] + values[3]
    return (x/2, y/2)
    
def leftAlign(values):
    #aligns text to left
    x = values[0] + 10
    y = values[1] + values[3]
    return (x, y/2)
    
def clickCheck(event, box):
    #checks if a box is clicked in
    if event.x > box[0] and event.x < box[2] and event.y > box[1] and event.y < box[3]:
        return True
    else:
        return False
        
def resetFunctionName(data):
    #resets functionName data
    data.functionNameInput = 'function name here'
    data.current2 = ''
    
####################################
# print functionList
####################################
    
def printFunctions(canvas, data, courseCode):
    #prints list of functions for a given course with appropriate spacing
    canvas.create_rectangle(data.functionList)
    functions = readFunctionList(courseCode)
    if functions == []:
        canvas.create_text(centerOfRectangle(data.functionList), text = "no functions created", font= ("Courier New", 10))
    else:
        height = data.functionList[3] - data.functionList[1]
        thickness = height/len(functions)
        for functionNum in range(len(functions)):
            x1 = data.functionList[0]
            x2 = data.functionList[2]
            y1 = data.functionList[1] + thickness*functionNum
            y2 = y1 + thickness
            functionBlock = (functions[functionNum], x1, y1, x2, y2)
            data.functions.append(functionBlock)
        for function in data.functions:
            canvas.create_rectangle(function[1:])
            canvas.create_text(leftAlign(function[1:]), text = function[0], anchor = 'w', font= ("Courier New", 10))

####################################
# functionSelection mode
####################################

def functionSelectionKeyPressed(event, data):
    pass
    
def functionSelectionMousePressed(event, data):
    if clickCheck(event, data.editButton) and data.selectedFunction != '':
        #edit existing function
        data.mode = "editFunction"
    elif clickCheck(event, data.createButton):
        #create new function
        data.mode = "createFunction"
    elif clickCheck(event, data.removeButton) and data.selectedFunction != '':
        #remove existing function
        data.functions = []
        removeTable(data.selectedFunction)
        removeElement(str(data.courseCode), data.selectedFunction)
    data.selectionFunction = ''
    selected = False
    for function in data.functions:
        #check if a function is selected
        if clickCheck(event, function[1:]):
            data.selectedFunction = function[0]
            selected = True
        if data.mode != "functionSelection":
            selected = True
    if selected == False: data.selectedFunction = ''

def functionSelectionRedrawAll(canvas, data):
    canvas.create_text(data.width/2, data.height/4, text = "FUNCTION CREATION", font= ("Courier New", 44, "bold"))
    canvas.create_rectangle(data.editButton)
    canvas.create_text(centerOfRectangle(data.editButton), text = "EDIT FUNCTION", font= ("Courier New", 10))
    canvas.create_rectangle(data.removeButton)
    canvas.create_text(centerOfRectangle(data.createButton), text = "CREATE FUNCTION", font= ("Courier New", 10))
    canvas.create_rectangle(data.createButton)
    canvas.create_text(centerOfRectangle(data.removeButton), text = "REMOVE FUNCTION", font= ("Courier New", 10))
    printFunctions(canvas, data, data.courseCode)

####################################
# editFunction mode
####################################

def editFunctionKeyPressed(event, data):
    pass
    
def editFunctionMousePressed(event, data):
    #dispatcher to other editing modes
    if clickCheck(event, data.backButton2):
        data.selectedFunction = ''
        data.mode = "functionSelection"
    elif clickCheck(event, data.functionDescription):
        try:
            description = getDescription(data.selectedFunction)[0]
            rows = len(description)//(data.width//10) + 1
            data.description = []
            for row in range(1,rows):
                data.description.append(description[(row-1)*(data.width//10):row*(data.width//10)])
            data.description.append(description[(rows-1)*(data.width//10):])
            data.descriptionLine = len(data.description)-1
        except:
            data.description = ['']
        data.mode = "functionDescription"
    elif clickCheck(event, data.linePrompts):
        data.lineSelected = False
        data.selectedLine = -1
        data.mode = "linePrompts"
    elif clickCheck(event, data.sampleCode):
        data.mode = "sampleCode"
        data.lineSelected = False
        data.selectedLine = -1
    elif clickCheck(event, data.addTestCaseButton):
        data.mode = 'testCase'

def editFunctionRedrawAll(canvas, data):
    canvas.create_text(data.width/2, data.height/8, text = data.selectedFunction, font= ("Courier New", 30, "bold"))
    canvas.create_rectangle(data.backButton2)
    canvas.create_text(centerOfRectangle(data.backButton2), text = "back", font= ("Courier New", 10))
    canvas.create_rectangle(data.functionDescription)
    canvas.create_text(centerOfRectangle(data.functionDescription), text = "Description of Function", font= ("Courier New", 10))
    canvas.create_rectangle(data.linePrompts)
    canvas.create_text(centerOfRectangle(data.linePrompts), text = "Line Prompts", font= ("Courier New", 10))
    canvas.create_rectangle(data.sampleCode)
    canvas.create_text(centerOfRectangle(data.sampleCode), text = "Sample Code", font= ("Courier New", 10))
    canvas.create_rectangle(data.addTestCaseButton)
    canvas.create_text(centerOfRectangle(data.addTestCaseButton)[0], centerOfRectangle(data.addTestCaseButton)[1] -8, text = "Add Test", font= ("Courier New", 10))
    canvas.create_text(centerOfRectangle(data.addTestCaseButton)[0], centerOfRectangle(data.addTestCaseButton)[1] + 8, text = "Case", font= ("Courier New", 10))
    
####################################
# createFunction mode
####################################

def createFunctionKeyPressed(event, data):
    if data.readyForName:
        if event.char in data.functionInputs:
            data.current2 += event.char
        elif event.keysym == "BackSpace" and len(data.current2) > 0:
            data.current2 = data.current2[:len(data.current2)-1]
        data.functionNameInput = data.current2
    
def createFunctionMousePressed(event, data):
    if clickCheck(event, data.backButton2):
        #back to functionSelection page
        resetFunctionName(data)
        data.mode = "functionSelection"
    elif clickCheck(event, data.submitButton2) and data.functionNameInput != "function name here":
        #adding new function to list
        data.functions = []
        createFunctionTable(data.functionNameInput)
        dataEntryFunction(data.courseCode, data.functionNameInput)
        resetFunctionName(data)
        data.mode = 'functionSelection'
    elif clickCheck(event, data.functionNameBox):
        data.readyForName = True
        if data.functionNameInput == 'function name here':
            data.functionNameInput = ''
    else:
        data.readyForName = False

def createFunctionRedrawAll(canvas, data):
    canvas.create_text(data.width/2, data.height/4, text = "Create Function", font= ("Courier New", 44, "bold"))
    canvas.create_rectangle(data.functionNameBox)
    canvas.create_text(leftAlign(data.functionNameBox), text = data.functionNameInput, anchor = "w", font= ("Courier New", 10))
    canvas.create_rectangle(data.submitButton2)
    canvas.create_text(centerOfRectangle(data.submitButton2), text = "SUBMIT", font= ("Courier New", 10))
    canvas.create_rectangle(data.backButton2)
    canvas.create_text(centerOfRectangle(data.backButton2), text = "back", font= ("Courier New", 10))