#The function editing modes of the program: testCase, functionDescription, sampleCode, linePrompts
#This file establishes the graphics for these modes as well as updating the appropriate function tables with information about the function's description, ideal code, and teacher prompts for future student use

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
    
def topLeftAlign(values):
    #aligns text in top left
    x = values[0] + 10
    y = values[1] + 10
    return (x, y)

def clickCheck(event, box):
    #checks if a box is clicked in
    if event.x > box[0] and event.x < box[2] and event.y > box[1] and event.y < box[3]:
        return True
    else:
        return False
        
####################################
#sqlite 3
####################################

import sqlite3

conn = sqlite3.connect('termproject.db')
c = conn.cursor()

def editDescription(functionName, description):
    #edits description for given function
    command = """UPDATE %s SET lineText = '%s' WHERE inputType = 'description'""" %(functionName, description)
    c.execute(command)
    conn.commit()
    
def getDescription(functionName):
    #returns the description of a particular function
    command = """SELECT lineText FROM %s WHERE inputType = 'description'""" %(functionName)
    c.execute(command)
    description = c.fetchone()
    return description
    
def getTestCase(functionName):
    #returns the test case for a particular function
    command = """SELECT lineText FROM %s WHERE inputType = 'testCase'""" %(functionName)
    c.execute(command)
    testCase = c.fetchone()
    return testCase
    
def dataEntryTestCase(functionName, testCase):
    #adds test case for a particular function to function's table
    c.execute("""INSERT INTO %s VALUES('testCase', 0, 'NA', '%s')""" %(functionName, testCase))
    conn.commit()
    
def editTestCase(functionName, testCase):
    #edits test case for a particular function
    c.execute("""UPDATE %s SET lineText = '%s' where inputType = 'testCase'""" %(functionName, testCase))
    conn.commit()
    
def dataEntryDescription(functionName, description):
    #adds description of function to function's table
    realDescription = ""
    for line in description:
        realDescription += line
    command = """INSERT INTO %s VALUES('description', 0, 'NA', '%s')""" % (functionName, realDescription)
    c.execute(command)
    conn.commit()
    
def dataEntryLineCode(functionName, lineNum, code):
    #adds line of teacher-inputted code for function to function's table
    c.execute("""INSERT INTO %s VALUES('sampleCode', %d, 'NA', '%s')""" %(functionName, lineNum, code))
    conn.commit()
    
def editLineCode(functionName, lineNum, code):
    #edits line of code for function in function's table
    command = """UPDATE %s SET lineText = '%s' WHERE inputType = 'sampleCode' AND lineNum = %d""" %(functionName, code, lineNum)
    c.execute(command)
    conn.commit()
    
def getLineCode(functionName, lineNum):
    #returns code for a particular line in a given function
    command = """SELECT lineText from %s WHERE lineNum = %d AND inputType = 'sampleCode'""" %(functionName,lineNum)
    c.execute(command)
    code = c.fetchone()
    return code
    
def getPrompt(functionName, lineNum):
    #returns teacher prompt for a particular line in a given function
    command = """SELECT lineText from %s WHERE lineNum = %d AND inputType = 'prompt'""" %(functionName, lineNum)
    c.execute(command)
    code = c.fetchone()
    return code
    
def dataEntryPrompt(functionName, lineNum, lineType, prompt):
    #adds teacher-inputted prompt for a specific line in a given function
    c.execute("""INSERT INTO %s VALUES('prompt', %d, '%s', '%s')""" %(functionName, lineNum, lineType, prompt))
    conn.commit()
   
####################################
# testCase mode: writing an exemplary test case for a funciton
####################################
      
def testCaseKeyPressed(event, data):
    if event.char in data.inputs:
        data.testCaseWords += event.char
    elif event.keysym == "space":
        data.testCaseWords += " "
    elif event.keysym == "Tab":
        data.testCaseWords += "    "
    elif event.keysym == "BackSpace" and len(data.testCaseWords) > 0:
        data.testCaseWords = data.testCaseWords[:len(data.testCaseWords)-1]
    if data.currentInput == 'input': data.testInput = data.testCaseWords
    elif data.currentInput == 'output': data.testOutput = data.testCaseWords
    
def testCaseMousePressed(event, data):
    if clickCheck(event, data.backButton2):
        data.mode = "editFunction"
    elif clickCheck(event, data.inputBox):
        data.testInput = ' '
        data.testCaseWords = ''
        data.currentInput = 'input'
    elif clickCheck(event, data.outputBox):
        data.testOutput = ' '
        data.testCaseWords = ''
        data.currentInput = 'output'
    elif clickCheck(event, data.submitButton2) and data.testInput!= '' and data.testOutput != '':
        #submits test case for particular function
        if getTestCase(data.selectedFunction) == None:
            #if test case does not exist already, creates it
            dataEntryTestCase(data.selectedFunction, data.testInput + "$$$"+ data.testOutput)
        else:
            #if test case exists, update it
            editTestCase(data.selectedFunction, data.testInput + "$$$"+ data.testOutput)
        data.mode = "editFunction"
    
def testCaseRedrawAll(canvas, data):
    canvas.create_rectangle(data.backButton2)
    canvas.create_text(centerOfRectangle(data.backButton2), text = "back", font= ("Courier New", 10))
    canvas.create_text(data.width/2, data.height/8, text = "Add a Sample Test Case", font= ("Courier New", 10))
    canvas.create_rectangle(data.submitButton2)
    canvas.create_text(centerOfRectangle(data.submitButton2), text = "Submit", font= ("Courier New", 10))
    canvas.create_rectangle(data.inputBox)
    if data.testInput == "":
        canvas.create_text(leftAlign(data.inputBox), text = "Write input for test case here", anchor = 'w', font= ("Courier New", 10))
    else: canvas.create_text(leftAlign(data.inputBox), text = data.testInput, anchor = 'w', font= ("Courier New", 10))
    canvas.create_rectangle(data.outputBox)
    if data.testOutput == "":
        canvas.create_text(leftAlign(data.outputBox), text = "Write output for test case here", anchor = 'w', font= ("Courier New", 10))
    else: canvas.create_text(leftAlign(data.outputBox), text = data.testOutput, anchor ='w', font= ("Courier New", 10))
    
####################################
# functionDescription mode: writing description of a particular function
####################################

def functionDescriptionKeyPressed(event, data):
    if data.descriptionCheck:
        if event.char in data.inputs:
            data.description[data.descriptionLine] += event.char
            if len(data.description[data.descriptionLine]) > data.width//10:
                data.description.append('')
                data.descriptionLine += 1
        elif event.keysym == "space":
            data.description[data.descriptionLine] += " "
            if len(data.description[data.descriptionLine]) > data.width//10:
                data.description.append('')
                data.descriptionLine += 1
        elif event.keysym == "Tab":
            data.description[data.descriptionLine] += "    "
            if len(data.description[data.descriptionLine]) > data.width//10:
                data.description.append('')
                data.descriptionLine += 1
        elif event.keysym == "BackSpace" and len(data.description[data.descriptionLine]) > 0:
            #backspace within a line
            data.description[data.descriptionLine] = data.description[data.descriptionLine][:len(data.description[data.descriptionLine])-1]
            if len(data.description[data.descriptionLine]) > data.width//10:
                data.description.append('')
                data.descriptionLine += 1
        elif event.keysym == "BackSpace" and len(data.description[data.descriptionLine]) == 0:
            #backspace across lines
            data.description.pop()
            data.descriptionLine -=1

def functionDescriptionMousePressed(event, data):
    if clickCheck(event, data.backButton2):
        try:
            description = getDescription(data.selectedFunction)[0]
            rows = len(description)//(data.width//10) + 1
            data.description = []
            for row in range(1,rows):
                data.description.append(description[(row-1)*(data.width//10):row*(data.width//10)])
            data.description.append(description[(rows-1)*(data.width//10):])
        except: data.description = ['']
        data.mode = "editFunction"
    elif clickCheck(event, data.descriptionBox):
        data.descriptionCheck = True
    elif clickCheck(event, data.submitButton2) and data.description!= ['']:
        #submits description for particular function
        if getDescription(data.selectedFunction) == None:
            #if description does not exist already, create it
            description = ''
            for des in range(len(data.description)):
                description += data.description[des]
            dataEntryDescription(data.selectedFunction, description)
        else:
            #if description exists, update it
            description = ''
            for des in range(len(data.description)):
                description += data.description[des]
            editDescription(data.selectedFunction, description)
        data.mode = "editFunction"
    else:
        data.descriptionCheck = False

def functionDescriptionRedrawAll(canvas, data):
    canvas.create_rectangle(data.backButton2)
    canvas.create_text(centerOfRectangle(data.backButton2), text = "back", font= ("Courier New", 10))
    canvas.create_text(data.width/2, data.height/8, text = "Description of Function", font= ("Courier New", 10))
    canvas.create_rectangle(data.descriptionBox)
    for description in range(len(data.description)):
        canvas.create_text(data.width/12 + 10, data.height/4 + 10+ 15*description, text = data.description[description], anchor = "nw", font= ("Courier New", 10))
    canvas.create_rectangle(data.submitButton2)
    canvas.create_text(centerOfRectangle(data.submitButton2), text = "Submit", font= ("Courier New", 10))

####################################
# sampleCode mode: writing the code for the function
####################################

def sampleCodeKeyPressed(event, data):
    if data.selectedLine != -1:
        if event.char in data.inputs:
            data.sampleLine += event.char
        elif event.keysym == "space":
            data.sampleLine += " "
        elif event.keysym == "Tab":
            data.sampleLine += "    "
        elif event.keysym == "BackSpace" and len(data.sampleLine) > 0:
            data.sampleLine = data.sampleLine[:len(data.sampleLine)-1]

def sampleCodeMousePressed(event, data):
    if clickCheck(event, data.backButton2):
        data.mode = "editFunction"
    data.lineSelected = False
    for line in data.lines:
        #checks if a line is selected
        if clickCheck(event, line):
            data.selectedLine=line[3]//20
            data.lineSelected = True
            if getLineCode(data.selectedFunction, data.selectedLine) != None:
                data.sampleLine = getLineCode(data.selectedFunction, data.selectedLine)[0]
    if clickCheck(event, data.submitLine) and data.sampleLine != '':
        #submit line of code
        if getLineCode(data.selectedFunction, data.selectedLine) == None:
            #if line of code does not exist, create it
            dataEntryLineCode(data.selectedFunction, data.selectedLine, data.sampleLine)
        else:
            #if line of code exists, update it
            editLineCode(data.selectedFunction, data.selectedLine, data.sampleLine)
        data.sampleLine = ''
    if data.lineSelected == False:
        data.selectedLine = -1

def sampleCodeRedrawAll(canvas,data):
    canvas.create_rectangle(data.backButton2)
    canvas.create_text(centerOfRectangle(data.backButton2), text = "back", font= ("Courier New", 10))
    canvas.create_line(data.width*3/4, 0, data.width*3/4, data.height)
    for line in range(data.numLines):
        canvas.create_rectangle(0, line*20, data.width*3/4, (line+1)*20)
        canvas.create_text(topLeftAlign((0, line*20, data.width*3/4, (line+1)*20)), text = str(line+1), font= ("Courier New", 9))
        if line != data.selectedLine and getLineCode(data.selectedFunction, line) != None:
            canvas.create_text(30, (line-1)*20+3, text = getLineCode(data.selectedFunction, line)[0], anchor = 'nw', font= ("Courier New", 9))
        elif line == data.selectedLine:
            canvas.create_text(30, (line-1)*20+3, text = data.sampleLine, anchor = 'nw', font= ("Courier New", 9))
    if data.selectedLine != -1:
        canvas.create_text(data.width*7/8, data.height/8, text = "Line #: " + str(data.selectedLine), font= ("Courier New", 10))
        canvas.create_rectangle(data.submitLine)
        canvas.create_text(centerOfRectangle(data.submitLine), text = "Submit line", font= ("Courier New", 9))
    
####################################
# linePrompts mode: writing teacher prompts for each line of code so students can reconstruct the function with guidance
####################################

def linePromptsKeyPressed(event, data):
    if event.char in data.inputs:
        data.currentInput += event.char
    elif event.keysym == "space":
        data.currentInput += " "
    elif event.keysym == "Tab":
        data.currentInput += "    "
    elif event.keysym == "BackSpace" and len(data.currentInput) > 0:
        data.currentInput = data.currentInput[:len(data.currentInput)-1]
    if data.currentBox == 'question': data.questionInput[0] = data.currentInput
    elif data.currentBox == 'answer': data.questionInput[1] = data.currentInput
    elif data.currentBox == 'partialLine': data.lineCompletionInput[0] = data.currentInput
    elif data.currentBox == 'lineInstructions': data.lineCompletionInput[1] = data.currentInput
    elif data.currentBox == 'error': data.errorInput[0] = data.currentInput
    elif data.currentBox == "errorExp": data.errorInput[1] = data.currentInput

def linePromptsMousePressed(event, data):
    if clickCheck(event, data.backButton2) and data.lineSelected == False:
        data.mode = "editFunction"
    if clickCheck(event, data.backButton2) and data.lineSelected == True:
        data.lineType = ''
        data.lineSelected = False
    if data.lineType == 'question':
        questionExec(event, data)
    elif data.lineType == 'lineCompletion':
        lineCompletionExec(event, data)
    elif data.lineType == 'identifyError':
        identifyErrorExec(event, data)
    if data.lineSelected and data.lineType == "" and getPrompt(data.selectedFunction, data.selectedLine) == None:
        if clickCheck(event, data.lineCompletion):
            data.lineType = "lineCompletion"
        elif clickCheck(event, data.question):
            data.lineType = "question"
        elif clickCheck(event, data.identifyError):
            data.lineType = "identifyError"
    for line in data.lines:
        if data.lineSelected == False and getLineCode(data.selectedFunction, line[3]//20) != None and clickCheck(event, line):
            data.selectedLine=line[3]//20
            if getPrompt(data.selectedFunction, data.selectedLine) == None:
                data.lineSelected = True
            elif getPrompt(data.selectedFunction, data.selectedLine) != None:
                data.selectedLine = -1
                
def questionExec(event, data):
    #if prompt is question
    if clickCheck(event, data.questionBox):
        data.currentInput = ''
        data.questionInput[0] = " "
        data.currentBox = 'question'
    elif clickCheck(event, data.answerBox):
        data.currentInput = ''
        data.questionInput[1] = " "
        data.currentBox = 'answer'
    elif clickCheck(event, data.questionSubmitBox) and data.questionInput[0] != '' and data.questionInput[1] != '':
        dataEntryPrompt(data.selectedFunction, data.selectedLine, 'question', data.questionInput[0]+"$$$"+data.questionInput[1])
        data.lineType = ''
        data.lineSelected = False
        data.questionInput = ['','']
                
def lineCompletionExec(event, data):
    #if prompt is for students to complete the line of code
    if clickCheck(event, data.partialLine):
        data.currentInput = ''
        data.lineCompletionInput[0] = " "
        data.currentBox = 'partialLine'
    elif clickCheck(event, data.lineInstructionsBox):
        data.currentInput = ''
        data.lineCompletionInput[1] = " "
        data.currentBox = 'lineInstructions'
    elif clickCheck(event, data.questionSubmitBox) and data.lineCompletionInput[0] != '' and data.lineCompletionInput[1] != '':
        dataEntryPrompt(data.selectedFunction, data.selectedLine, 'lineCompletion', data.lineCompletionInput[0]+"$$$"+ data.lineCompletionInput[1])
        data.lineType = ''
        data.lineSelected = False
        data.lineCompletionInput = ['','']
                
def identifyErrorExec(event, data):
    #if prompt is for students to identify error with code
    if clickCheck(event, data.errorBox):
        data.currentInput = ''
        data.errorInput[0] = ' '
        data.currentBox = 'error'
    elif clickCheck(event, data.errorExpBox):
        data.currentInput = ''
        data.errorInput[1] = ' '
        data.currentBox = 'errorExp'
    elif clickCheck(event, data.questionSubmitBox) and data.errorInput[0] != '' and data.errorInput[1] != "":
        dataEntryPrompt(data.selectedFunction, data.selectedLine, 'identifyError', data.errorInput[0]+"$$$"+data.errorInput[1])
        data.lineType = ''
        data.lineSelected = False
        data.errorInput = ['','']

def linePromptsRedrawAll(canvas,data):
    canvas.create_rectangle(data.backButton2)
    canvas.create_text(centerOfRectangle(data.backButton2), text = "back")
    if data.lineSelected == False:
        canvas.create_line(data.width*3/4, 0, data.width*3/4, data.height)
        for line in range(data.numLines):
            canvas.create_rectangle(0, line*20, data.width*3/4, (line+1)*20)
            canvas.create_text(topLeftAlign((0, line*20, data.width*3/4, (line+1)*20)), text = str(line+1))
            if getLineCode(data.selectedFunction, line) != None:
                if getPrompt(data.selectedFunction, line) == None:
                    #line is red if prompt has not been written
                    color = 'red'
                else: color = 'green'
                canvas.create_text(30, (line-1)*20+3, text = getLineCode(data.selectedFunction, line)[0], anchor = 'nw', fill = color, font= ("Courier New", 10))
        canvas.create_text(data.width*7/8, data.height/8, text = "Select a line", anchor = 'center', font= ("Courier New", 10))
        canvas.create_text(data.width*7/8, data.height*4/24, text = "to write a prompt.", anchor = 'center', font= ("Courier New", 10))
        canvas.create_text(data.width*7/8, data.height*5/8, text = "Red lines do not", anchor = 'center', fill = 'red', font= ("Courier New", 10))
        canvas.create_text(data.width*7/8, data.height*16/24, text = "have prompts written.", anchor = 'center', fill = 'red', font= ("Courier New", 10))
        canvas.create_text(data.width*7/8, data.height*3/8, text = "Green lines have", anchor = 'center', fill = 'green', font= ("Courier New", 10))
        canvas.create_text(data.width*7/8, data.height*10/24, text = "prompts written.", anchor = 'center', fill = 'green', font= ("Courier New", 10))
    elif data.lineSelected:
        canvas.create_rectangle(0, (data.selectedLine-1)*20, data.width, data.selectedLine*20)
        canvas.create_text(topLeftAlign((0, (data.selectedLine-1)*20, data.width*3/4, data.selectedLine*20)), text = str(data.selectedLine), font= ("Courier New", 10))
        canvas.create_text(30, (data.selectedLine - 1)*20+3, text = getLineCode(data.selectedFunction, data.selectedLine)[0], anchor = 'nw', font= ("Courier New", 10))
        data.half = 1-data.selectedLine//(data.numLines//2)
        if data.lineType == '':
            promptTypeSelectionDraw(canvas, data)
        elif data.lineType == "lineCompletion":
            lineCompletionDraw(canvas, data)
        elif data.lineType == "question":
            questionDraw(canvas, data)
        elif data.lineType == "identifyError":
            identifyErrorDraw(canvas, data)
            
def promptTypeSelectionDraw(canvas, data):
    #once line selected, before prompt type is selected
    canvas.create_text(data.width/2, data.height/8+data.height*data.half/2, text = "Choose prompt type.", font = ("Courier New", 16, "bold"))
    data.lineCompletion = (data.width/16, data.height*3/16+data.height*data.half/2, data.width*5/16, data.height*5/16+data.height*data.half/2)
    data.question = (data.width*3/8, data.height*3/16+data.height*data.half/2, data.width*5/8, data.height*5/16+data.height*data.half/2)
    data.identifyError = (data.width*11/16, data.height*3/16+data.height*data.half/2, data.width*15/16, data.height*5/16+data.height*data.half/2)
    canvas.create_rectangle(data.lineCompletion)
    canvas.create_text(centerOfRectangle(data.lineCompletion), text = "Line Completion", font= ("Courier New", 10))
    canvas.create_rectangle(data.question)
    canvas.create_text(centerOfRectangle(data.question), text = "Question", font= ("Courier New", 10))
    canvas.create_rectangle(data.identifyError)
    canvas.create_text(centerOfRectangle(data.identifyError), text = "Error Identification", font= ("Courier New", 10))
            
def lineCompletionDraw(canvas, data):
    #if prompt is for students to complete the line
    data.partialLine = (data.width/16, data.height/8+data.height*data.half/2, data.width*15/16, data.height*3/16 + data.height*data.half/2)
    canvas.create_rectangle(data.partialLine)
    if data.lineCompletionInput[0] == '':
        canvas.create_text(leftAlign(data.partialLine), text = "Write partial line of code here", anchor = "w", font= ("Courier New", 10))
    else:
        canvas.create_text(leftAlign(data.partialLine), text = data.lineCompletionInput[0], anchor = "w", font= ("Courier New", 10))
    data.lineInstructionsBox = (data.width/16, data.height/4+data.height*data.half/2, data.width*15/16, data.height*5/16 + data.height*data.half/2)
    canvas.create_rectangle(data.lineInstructionsBox)
    if data.lineCompletionInput[1] == '':
        canvas.create_text(leftAlign(data.lineInstructionsBox), text = "Write instructions for completing line here", anchor = 'w', font= ("Courier New", 10))
    else:
        canvas.create_text(leftAlign(data.lineInstructionsBox), text = data.lineCompletionInput[1], anchor = "w", font= ("Courier New", 10))
    data.questionSubmitBox = (data.width*7/16, data.height*3/8 +data.height*data.half/2, data.width*9/16, data.height*7/16 + data.height*data.half/2)
    canvas.create_rectangle(data.questionSubmitBox)
    canvas.create_text(centerOfRectangle(data.questionSubmitBox), text = "Submit", font= ("Courier New", 10))
            
def questionDraw(canvas, data):
    #if prompt is a question
    data.questionBox = (data.width/16, data.height/8+data.height*data.half/2, data.width*15/16, data.height*3/16 + data.height*data.half/2)
    canvas.create_rectangle(data.questionBox)
    if data.questionInput[0] == '':
        canvas.create_text(leftAlign(data.questionBox), text = "Write desired question here", anchor = "w", font= ("Courier New", 10))
    else:
        canvas.create_text(leftAlign(data.questionBox), text = data.questionInput[0], anchor = "w", font= ("Courier New", 10))
    data.answerBox = (data.width/16, data.height/4+data.height*data.half/2, data.width*15/16, data.height*5/16 + data.height*data.half/2)
    canvas.create_rectangle(data.answerBox)
    if data.questionInput[1] == '':
        canvas.create_text(leftAlign(data.answerBox), text = "Write keywords in answer (comma-separated)", anchor = 'w', font= ("Courier New", 10))
    else:
        canvas.create_text(leftAlign(data.answerBox), text = data.questionInput[1], anchor = "w", font= ("Courier New", 10))
    data.questionSubmitBox = (data.width*7/16, data.height*3/8 +data.height*data.half/2, data.width*9/16, data.height*7/16 + data.height*data.half/2)
    canvas.create_rectangle(data.questionSubmitBox)
    canvas.create_text(centerOfRectangle(data.questionSubmitBox), text = "Submit", font= ("Courier New", 10))
            
def identifyErrorDraw(canvas, data):
    #if prompt is for students to identify error in code
    data.errorBox = (data.width/16, data.height/8+data.height*data.half/2, data.width*15/16, data.height*3/16 + data.height*data.half/2)
    canvas.create_rectangle(data.errorBox)
    if data.errorInput[0] == '':
        canvas.create_text(leftAlign(data.errorBox), text = "Write erroneous code here", anchor = "w", font= ("Courier New", 10))
    else:
        canvas.create_text(leftAlign(data.errorBox), text = data.errorInput[0], anchor = "w", font= ("Courier New", 10))
    data.errorExpBox = (data.width/16, data.height/4+data.height*data.half/2, data.width*15/16, data.height*5/16 + data.height*data.half/2)
    canvas.create_rectangle(data.errorExpBox)
    if data.errorInput[1] == '':
        canvas.create_text(leftAlign(data.errorExpBox), text = "Write keywords in explanation of error (comma-separated)", anchor = 'w', font= ("Courier New", 10))
    else:
        canvas.create_text(leftAlign(data.errorExpBox), text = data.errorInput[1], anchor = "w", font= ("Courier New", 10))
    data.questionSubmitBox = (data.width*7/16, data.height*3/8 +data.height*data.half/2, data.width*9/16, data.height*7/16 + data.height*data.half/2)
    canvas.create_rectangle(data.questionSubmitBox)
    canvas.create_text(centerOfRectangle(data.questionSubmitBox), text = "Submit", font= ("Courier New", 10))