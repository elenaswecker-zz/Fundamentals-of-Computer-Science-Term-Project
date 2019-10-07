#The student modes of the program: studentHome, practiceFunction, studentDescription, functionBuilder
#This file establishes the graphics for these modes as well as updating the appropriate tables with information about student progress and checking student responses as compared to teacher's desired responses

from tkinter import *
import string
import nltk
from nltk.corpus import wordnet
nltk.download('wordnet')

####################################
#checking answers
####################################

def checkTextAnswer(correctInput, studentInput):
    #checks student text answer by comparing to teacher's desired key words
    studentAnswer = studentInput.split(" ")
    matches = correctInput.split(",")
    for matchNum in range(len(matches)):
        matches[matchNum] = matches[matchNum].strip()
    while '' in matches:
        matches.remove('')
    for match in matches:
        if match in studentAnswer:
            continue
        matched = False
        synonyms = []
        for syn in wordnet.synsets(match):
            for l in syn.lemmas():
                synonyms.append(l.name())
        for potentialWord in synonyms:
            if potentialWord in studentAnswer:
                matched = True
                break
        if matched == False:
            return False
    return True
    
def checkCodeAnswer(correctFunction, lineNum, studentInput, testCase):
    #checks student code answer by comparing to teacher's desired key words
    testCase = testCase.split("$$$")
    correctFunction = correctFunction[:lineNum-1] + [studentInput] + correctFunction[lineNum:]
    functionText = """"""
    for line in correctFunction:
        functionText += line
        functionText += "\n"
    functionCall1 = correctFunction[0].split("def ")
    functionCall2 = functionCall1[1].split("(")
    functionCall3 = functionCall2[0] + "(" + testCase[0] + ")"
    try:
        exec(functionText)
        correct = eval(functionCall3)
        if correct == eval(testCase[1]):
            return True
        else: return False
    except: return False

####################################
#sqlite 3
####################################

import sqlite3

conn = sqlite3.connect('termproject.db')    
c = conn.cursor()
    
def readFunctionList(courseCode):
    #returns function list for a given course
    c.execute("""SELECT * FROM %s""" %("a" + str(courseCode)))
    data = c.fetchall()
    return data
    
def functionLines(functionName):
    #returns lines in sampleCode for a given function
    c.execute("""SELECT lineText FROM %s WHERE inputType = 'sampleCode'""" %(functionName))
    data = c.fetchall()
    return data
    
def getDescription(functionName):
    #returns the description of a particular function
    command = """SELECT lineText FROM %s WHERE inputType = 'description'""" %(functionName)
    c.execute(command)
    description = c.fetchone()
    return description
    
def getLineCode(functionName, lineNum):
    #returns code for a particular line in a given function
    command = """SELECT lineText from %s WHERE lineNum = %d AND inputType = 'sampleCode'""" %(functionName,lineNum)
    c.execute(command)
    code = c.fetchone()
    return code
    
def funcCompleted(functionName, username):
    #returns if user has finished constructing a particular function
    command = """SELECT completed FROM %s WHERE functionName = '%s'""" %(username+'Progress', functionName)
    c.execute(command)
    funcCompleted = c.fetchone()
    if funcCompleted[0] == 1:
        return True
    elif funcCompleted[0] == 0:
        return False
        
def getCurrentLine(functionName, username):
    #returns current line in progress for student and specified function
    command = """SELECT lineNum FROM %s WHERE functionName = '%s'""" %(username+"Progress", functionName)
    c.execute(command)
    currentLine = c.fetchone()
    return int(currentLine[0])
    
def getPromptType(functionName, lineNum):
    #returns type of prompt for specific line in given function
    command = """SELECT lineType FROM %s WHERE inputType = 'prompt' AND lineNum = %d""" %(functionName, lineNum)
    c.execute(command)
    promptType = c.fetchone()
    return promptType
    
def getPrompt(functionName, lineNum):
    #returns teacher prompt for a particular line in a given function
    command = """SELECT lineText from %s WHERE lineNum = %d AND inputType = 'prompt'""" %(functionName, lineNum)
    c.execute(command)
    code = c.fetchone()
    return code
    
def updateProgress(username, functionName, lineNum):
    #updates student progress in terms of line number for given function
    command = """UPDATE %s SET lineNum = %d WHERE functionName = '%s'""" %(username+"Progress", lineNum, functionName)
    c.execute(command)
    conn.commit()
    
def markComplete(username, functionName):
    #sets progress (complete?) for function and specific user as True
    command = """UPDATE %s SET completed = 1 WHERE functionName = '%s'""" %(username + "Progress", functionName)
    c.execute(command)
    command = """UPDATE %s SET lineNum = 1 WHERE functionName = '%s'""" %(username + "Progress", functionName)
    c.execute(command)
    conn.commit()
    
def resetProgress(username, functionName):
    #sets progress (complete?) for function and specified user as False
    command = """UPDATE %s SET completed = 0 WHERE functionName = '%s'""" %(username + "Progress", functionName)
    c.execute(command)
    command = """UPDATE %s SET lineNum = 1 WHERE functionName = '%s'""" %(username + "Progress", functionName)
    c.execute(command)
    conn.commit()
    
def getTestCase(functionName):
    #returns the test case for a particular function
    command = """SELECT lineText FROM %s WHERE inputType = 'testCase'""" %(functionName)
    c.execute(command)
    testCase = c.fetchone()
    return testCase

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
            if funcCompleted(function[0][0], data.username):
                #if function has already been completed, text should be green
                color = 'green'
            else:
                #if function has not bee completed, text should be red
                color ='red'
            canvas.create_rectangle(function[1:])
            canvas.create_text(leftAlign(function[1:]), text = function[0][0], anchor = 'w', fill = color, font= ("Courier New", 10))
            
####################################
# studentHome mode
####################################

def studentHomeKeyPressed(event, data):
    pass
    
def studentHomeMousePressed(event, data):
    if clickCheck(event, data.practiceButton) and data.selectedFunction != '' and not funcCompleted(data.selectedFunction, data.username):
        data.mode = "practiceFunction"
    elif clickCheck(event, data.resetButton) and data.selectedFunction != '':
        resetProgress(data.username, data.selectedFunction)
    for function in data.functions:
        #check if a function is selected
        if clickCheck(event, function[1:]):
            data.selectedFunction = function[0][0]
            data.functionText = []
            data.testCase = getTestCase(data.selectedFunction)
            lines = functionLines(data.selectedFunction)
            for line in lines:
                data.functionText.append(line[0])

def studentHomeRedrawAll(canvas, data):
    canvas.create_text(data.width/2, data.height/4, text = "STUDENT HOME PAGE", font= ("Courier New", 30, "bold"))
    canvas.create_rectangle(data.practiceButton)
    canvas.create_text(centerOfRectangle(data.practiceButton), text = "PRACTICE FUNCTION", font= ("Courier New", 10))
    canvas.create_rectangle(data.resetButton)
    canvas.create_text(centerOfRectangle(data.resetButton), text = "RESET FUNCTION", font= ("Courier New", 10))
    printFunctions(canvas, data, data.courseCode)

####################################
# practiceFunction mode
####################################

def practiceFunctionKeyPressed(event, data):
    pass
    
def practiceFunctionMousePressed(event, data):
    #dispatcher to the practicing modes
    if clickCheck(event, data.backButton2):
        data.selectedFunction = ''
        data.mode = "studentHome"
    elif clickCheck(event, data.functionDescription):
        description = getDescription(data.selectedFunction)[0]
        rows = len(description)//(data.width//10) + 1
        data.description = []
        for row in range(1,rows):
            data.description.append(description[(row-1)*(data.width//10):row*(data.width//10)])
        data.description.append(description[(rows-1)*(data.width//10):])
        data.mode = "studentDescription"
    elif clickCheck(event, data.functionBuilder):
        data.mode = "functionBuilder"

def practiceFunctionRedrawAll(canvas, data):
    canvas.create_text(data.width/2, data.height/8, text = data.selectedFunction, font= ("Courier New", 44, "bold"))
    canvas.create_rectangle(data.backButton2)
    canvas.create_text(centerOfRectangle(data.backButton2), text = "back", font= ("Courier New", 10))
    canvas.create_rectangle(data.studentDescription)
    canvas.create_text(centerOfRectangle(data.studentDescription), text = "Description of Function", font= ("Courier New", 10))
    canvas.create_rectangle(data.functionBuilder)
    canvas.create_text(centerOfRectangle(data.functionBuilder), text = "Function Building", font= ("Courier New", 10))

####################################
# studentDescription mode: view description of function
####################################

def studentDescriptionKeyPressed(event, data):
    pass

def studentDescriptionMousePressed(event, data):
    if clickCheck(event, data.backButton2):
        data.mode = "practiceFunction"
    elif clickCheck(event, data.submitButton2):
        data.mode = "practiceFunction"

def studentDescriptionRedrawAll(canvas, data):
    canvas.create_rectangle(data.backButton2)
    canvas.create_text(centerOfRectangle(data.backButton2), text = "back", font= ("Courier New", 10))
    canvas.create_text(data.width/2, data.height/8, text = "Description of Function", font= ("Courier New", 10))
    canvas.create_rectangle(data.descriptionBox)
    for description in range(len(data.description)):
        canvas.create_text(data.width/12 + 10, data.height/4 + 10+ 15*description, text = data.description[description], anchor = "nw", font= ("Courier New", 10))
    canvas.create_rectangle(data.submitButton2)
    canvas.create_text(centerOfRectangle(data.submitButton2), text = "Done", font= ("Courier New", 10))
    
####################################
# functionBuilder mode: responding to prompts to build function
####################################

def functionBuilderKeyPressed(event, data):
    if event.char in data.inputs:
        data.currentInput += event.char
    elif event.keysym == "space":
        data.currentInput += " "
    elif event.keysym == "Tab":
        data.currentInput += "    "
    elif event.keysym == "BackSpace" and len(data.currentInput) > 0:
        data.currentInput = data.currentInput[:len(data.currentInput)-1]
    if data.currentBox == 'question': data.studentQuestionResponse = data.currentInput
    elif data.currentBox == 'error': data.studentErrorResponse = data.currentInput
    elif data.currentBox == 'line': data.studentLineResponse = data.currentInput

def functionBuilderMousePressed(event, data):
    if clickCheck(event, data.backButton3) and funcCompleted(data.selectedFunction, data.username):
        data.selectedFunction = ''
        data.mode = "studentHome"
    elif clickCheck(event, data.backButton2):
        data.mode = "practiceFunction"
    elif funcCompleted(data.selectedFunction, data.username) and clickCheck(event, data.backButton3):
        data.mode = "studentHome"
    if data.studentLineType == 'question':
        questionExec(event, data)
    elif data.studentLineType == 'lineCompletion':
        lineCompletionExec(event, data)
    elif data.studentLineType == 'identifyError':
        identifyErrorExec(event, data)
        
def questionExec(event, data):
    #if prompt is question
    if clickCheck(event, data.answerBox):
        data.currentInput = ''
        data.studentQuestionResponse = " "
        data.currentBox = 'question'
    elif clickCheck(event, data.questionSubmitBox) and data.studentQuestionResponse != '' and checkTextAnswer(data.correctAnswer, data.studentQuestionResponse):
        updateProgress(data.username, data.selectedFunction, data.selectedLine + 1)
        data.studentQuestionResponse = ''
    elif clickCheck(event, data.questionSubmitBox) and data.studentQuestionResponse != '' and not checkTextAnswer(data.correctAnswer, data.studentQuestionResponse):
        data.wrong = True
        data.studentQuestionResponse = ' '
        
def lineCompletionExec(event, data):
    #if prompt is for students to complete the line of code
    if clickCheck(event, data.lineInstructionsBox):
        data.currentInput = ''
        data.studentLineResponse = " "
        data.currentBox = 'line'
    elif clickCheck(event, data.questionSubmitBox) and data.studentLineResponse != '' and checkCodeAnswer(data.functionText, data.selectedLine, data.studentLineResponse, data.testCase[0]):
        updateProgress(data.username, data.selectedFunction, data.selectedLine + 1)
        data.studentLineResponse = ''
    elif clickCheck(event, data.questionSubmitBox) and data.studentLineResponse != '' and not checkCodeAnswer(data.functionText, data.selectedLine, data.studentLineResponse, data.testCase[0]):
        data.wrong = True
        data.studentLineResponse = ' '
            
def identifyErrorExec(event, data):
    #if prompt is for students to identify error with code
    if clickCheck(event, data.errorExpBox):
        data.currentInput = ''
        data.studentErrorResponse = ' '
        data.currentBox = 'error'
    elif clickCheck(event, data.questionSubmitBox) and data.studentErrorResponse != '' and checkTextAnswer(data.correctAnswer, data.studentErrorResponse):
        updateProgress(data.username, data.selectedFunction, data.selectedLine + 1)
        data.studentErrorResponse = ''
    elif clickCheck(event, data.questionSubmitBox) and data.studentErrorResponse != '' and not checkTextAnswer(data.correctAnswer, data.studentErrorResponse):
        data.wrong = True
        data.studentErrorResponse = ' '

def functionBuilderRedrawAll(canvas, data):
    data.selectedLine = getCurrentLine(data.selectedFunction, data.username)
    if data.wrong:
        canvas.create_text(data.width/2, data.height*9/32 +data.height*data.half/2, text = "Incorrect. Please try again.", fill = "red", font= ("Courier New", 10))
        data.wrong = False
    if getLineCode(data.selectedFunction, data.selectedLine) == None:
        canvas.create_text(data.width/2, data.height/2, text = "Function Completed!", font = ("Courier New", 24, "bold"))
        canvas.create_rectangle(data.backButton3)
        canvas.create_text(centerOfRectangle(data.backButton3), text = "Go Home", font= ("Courier New", 10))
        markComplete(data.username, data.selectedFunction)
    else:
        canvas.create_rectangle(data.backButton2)
        canvas.create_text(centerOfRectangle(data.backButton2), text = "back", font= ("Courier New", 10))
        data.half = 1-data.selectedLine//(data.numLines//2)
        if data.selectedLine > 1:
            for line in range(1, data.selectedLine):
                #draw completed lines previous to current one
                if data.half == 1-line//(data.numLines//2):
                    canvas.create_rectangle(0, (line-1)*20, data.width, line*20, fill = "light blue")
                    canvas.create_text(topLeftAlign((0, (line-1)*20, data.width*3/4, line*20)), text = str(line), font= ("Courier New", 10), fill = "blue")
                    canvas.create_text(30, (line - 1)*20+3, text = getLineCode(data.selectedFunction, line)[0], anchor = 'nw', font= ("Courier New", 10), fill = "blue")
        data.studentLineType = getPromptType(data.selectedFunction, data.selectedLine)[0]
        if data.studentLineType == 'question':
            questionDraw(canvas, data)
        elif data.studentLineType == "lineCompletion":
            lineCompletionDraw(canvas, data)
        elif data.studentLineType == 'identifyError':
            identifyErrorDraw(canvas, data)
            
def questionDraw(canvas, data):
    #answering a question
    #Note: only for question is the current line drawn
    canvas.create_rectangle(0, (data.selectedLine-1)*20, data.width, data.selectedLine*20)
    canvas.create_text(topLeftAlign((0, (data.selectedLine-1)*20, data.width*3/4, data.selectedLine*20)), text = str(data.selectedLine), font= ("Courier New", 10))
    canvas.create_text(30, (data.selectedLine - 1)*20+3, text = getLineCode(data.selectedFunction, data.selectedLine)[0], anchor = 'nw', font= ("Courier New", 10))
    prompt = getPrompt(data.selectedFunction, data.selectedLine)[0]
    splitPrompt = prompt.split("$$$")
    data.correctAnswer = splitPrompt[1]
    data.questionBox = (data.width/16, data.height/8+data.height*data.half/2, data.width*15/16, data.height*3/16 + data.height*data.half/2)
    canvas.create_rectangle(data.questionBox)
    canvas.create_text(leftAlign(data.questionBox), text = splitPrompt[0], anchor = "w", font= ("Courier New", 10))
    data.answerBox = (data.width/16, data.height/4+data.height*data.half/2, data.width*15/16, data.height*5/16 + data.height*data.half/2)
    canvas.create_rectangle(data.answerBox)
    if data.studentQuestionResponse == '':
        canvas.create_text(leftAlign(data.answerBox), text = "Write your answer here", anchor = "w", font= ("Courier New", 10))
    else: canvas.create_text(leftAlign(data.answerBox), text = data.studentQuestionResponse, anchor = "w", font= ("Courier New", 10))
    data.questionSubmitBox = (data.width*7/16, data.height*3/8 +data.height*data.half/2, data.width*9/16, data.height*7/16 + data.height*data.half/2)
    canvas.create_rectangle(data.questionSubmitBox)
    canvas.create_text(centerOfRectangle(data.questionSubmitBox), text = "Submit", font= ("Courier New", 10))
        
def lineCompletionDraw(canvas, data):
    #completing the line
    prompt = getPrompt(data.selectedFunction, data.selectedLine)[0]
    splitPrompt = prompt.split("$$$")
    data.correctAnswer = splitPrompt[1]
    data.partialLine = (data.width/16, data.height/8+data.height*data.half/2, data.width*15/16, data.height*3/16 + data.height*data.half/2)
    canvas.create_rectangle(data.partialLine)
    canvas.create_text(leftAlign(data.partialLine), text = splitPrompt[1], anchor = "w", font= ("Courier New", 10))
    data.partialLine2 = (data.width/16, data.height/32+data.height*data.half/2, data.width*15/16, data.height*3/32 + data.height*data.half/2)
    canvas.create_rectangle(data.partialLine2)
    canvas.create_text(leftAlign(data.partialLine2), text = splitPrompt[0], anchor = "w", font= ("Courier New", 10))
    data.lineInstructionsBox = (data.width/16, data.height/4+data.height*data.half/2, data.width*15/16, data.height*5/16 + data.height*data.half/2)
    canvas.create_rectangle(data.lineInstructionsBox)
    if data.studentLineResponse == '':
        canvas.create_text(leftAlign(data.lineInstructionsBox), text = "Write completed line here", anchor = 'w', font= ("Courier New", 10))
    else:
        canvas.create_text(leftAlign(data.lineInstructionsBox), text = data.studentLineResponse, anchor = "w", font= ("Courier New", 10))
    data.questionSubmitBox = (data.width*7/16, data.height*3/8 +data.height*data.half/2, data.width*9/16, data.height*7/16 + data.height*data.half/2)
    canvas.create_rectangle(data.questionSubmitBox)
    canvas.create_text(centerOfRectangle(data.questionSubmitBox), text = "Submit", font= ("Courier New", 10))
            
def identifyErrorDraw(canvas, data):
    #identifying the error
    prompt = getPrompt(data.selectedFunction, data.selectedLine)[0]
    splitPrompt = prompt.split("$$$")
    data.correctAnswer = splitPrompt[1]
    data.errorBox = (data.width/16, data.height/8+data.height*data.half/2, data.width*15/16, data.height*3/16 + data.height*data.half/2)
    canvas.create_rectangle(data.errorBox)
    canvas.create_text(leftAlign(data.errorBox), text = splitPrompt[0], anchor = "w", font= ("Courier New", 10))
    data.errorExpBox = (data.width/16, data.height/4+data.height*data.half/2, data.width*15/16, data.height*5/16 + data.height*data.half/2)
    canvas.create_rectangle(data.errorExpBox)
    if data.studentErrorResponse == '':
        canvas.create_text(leftAlign(data.errorExpBox), text = "Describe the error in the above line here", anchor = 'w', font= ("Courier New", 10))
    else:
        canvas.create_text(leftAlign(data.errorExpBox), text = data.studentErrorResponse, anchor = "w", font= ("Courier New", 10))
    data.questionSubmitBox = (data.width*7/16, data.height*3/8 +data.height*data.half/2, data.width*9/16, data.height*7/16 + data.height*data.half/2)
    canvas.create_rectangle(data.questionSubmitBox)
    canvas.create_text(centerOfRectangle(data.questionSubmitBox), text = "Submit", font= ("Courier New", 10))