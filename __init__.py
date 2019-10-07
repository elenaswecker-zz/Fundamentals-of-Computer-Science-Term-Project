#The main file, __init__.py
#This file runs the program by calling the run() function and the mode dispatcher

from tkinter import *
import string
from LoginPage import *
from TeacherInterface import *
from FunctionEditor import *
from StudentInterface import *

####################################
#init: initializes values for all modes of program
####################################
     
def init(data):
    #initial mode
    data.mode = "startState"
    #dimensions for buttons/text boxes
    data.studentTextBox = (data.width*6/16, data.height*7/16, data.width*10/16, data.height*9/16)
    data.teacherTextBox = (data.width*6/16, data.height*10/16, data.width*10/16, data.height*12/16)
    data.backButton = (data.width*14/16, data.height*14/16, data.width*15/16, data.height*15/16)
    data.usernameBox = (data.width*8/24, data.height*9/24, data.width*16/24, data.height*11/24)
    data.passwordBox = (data.width*8/24, data.height*12/24, data.width*16/24, data.height*14/24)
    data.courseCodeBox = (data.width*8/24, data.height*15/24, data.width*16/24, data.height*17/24)
    data.submitButton = (data.width*10/24, data.height*39/48, data.width*14/24, data.height*43/48)
    data.createButton = (data.width*7/12, data.height*15/24, data.width*11/12, data.height*17/24)
    data.editButton = (data.width*7/12, data.height*11/24, data.width*11/12, data.height*13/24)
    data.removeButton = (data.width*7/12, data.height*19/24, data.width*11/12, data.height*21/24)
    data.practiceButton = (data.width*7/12, data.height*11/24, data.width*11/12, data.height*15/24)
    data.resetButton = (data.width*7/12, data.height*17/24, data.width*11/12, data.height*21/24)
    data.functionList = (data.width*1/12, data.height*11/24, data.width*5/12, data.height*21/24)
    data.submitButton2 = (data.width*7/16, data.height*13/16, data.width*9/16, data.height*14/16)
    data.backButton2 = (data.width*14/16, data.height*14/16, data.width*15/16,data.height*15/16)
    data.functionNameBox = (data.width*8/24, data.height*11/24, data.width*16/24, data.height*13/24)
    data.functionDescription = (data.width/4, data.height/4, data.width*3/4, data.height*5/12)
    data.studentDescription = (data.width/4, data.height/4, data.width*3/4, data.height*5/12)
    data.sampleCode = (data.width/4, data.height/2, data.width*3/4, data.height*8/12)
    data.functionBuilder = (data.width/4, data.height/2, data.width*3/4, data.height*8/12)
    data.linePrompts = (data.width/4, data.height*3/4, data.width*3/4, data.height*11/12)
    data.addTestCaseButton = (data.width*13/16, data.height/2, data.width*15/16, data.height*2/3)
    data.descriptionBox = (data.width/12, data.height/4, data.width*11/12, data.height*3/4)
    data.submitLine = (data.width*13/16, data.height*3/8, data.width*15/16, data.height/2)
    data.inputBox = (data.width/4, data.height/4, data.width*3/4, data.height*7/16)
    data.outputBox = (data.width/4, data.height*9/16, data.width*3/4, data.height*3/4)
    data.backButton3 = (data.width*3/8, data.height*14/16, data.width*5/8, data.height*15/16)
    #log in initial values
    data.username = 'username here'
    data.password = 'password here'
    data.courseCode = 'course code (#) here'
    data.current = ''
    inputs = string.ascii_letters + string.digits + string.punctuation + "    "
    data.inputs = inputs.replace("'", "")
    data.functionInputs = string.ascii_letters + string.digits
    #teacher side initial values
    data.readyForName = False
    data.functionNameInput = 'function name here'
    data.current2 = ''
    data.functions = []
    data.selectedFunction = ''
    data.lineNumber = 0
    data.chooseType = "choose prompt type"
    data.descriptionCheck = False
    data.description = ['']
    data.descriptionLine = 0
    data.numLines = data.height//20
    data.lines = []
    for line in range(data.numLines):
        data.lines.append((0, line*20, data.width*3/4, (line+1)*20))
    data.selectedLine = -1
    data.sampleLine = ''
    data.lineSelected = False
    data.lineType = ''
    data.readyForInput = False
    data.currentInput = ''
    data.currentBox = ''
    data.testInput = ''
    data.testOutput = ''
    data.testCaseWords = ''
    data.courseCodeNotNumbers = False
    #student side initial values
    data.questionInput = ['', '']
    data.lineCompletionInput = ['', '']
    data.errorInput = ['', '']
    data.studentQuestionResponse = ''
    data.studentErrorResponse = ''
    data.studentLineResponse = ''
    data.correctAnswer = ''
    data.studentLineType = ''
    data.testCaseCheck = False
    data.wrong = False
    data.notACourseCode = False
    data.wrongPassword = False
    
####################################
# mode dispatcher
####################################

def mousePressed(event, data):
    if (data.mode == "startState"): startStateMousePressed(event, data)
    elif (data.mode == "studentLogin"): studentLoginMousePressed(event,data)
    elif (data.mode == "teacherLogin"): teacherLoginMousePressed(event,data)
    elif (data.mode == "functionSelection"): functionSelectionMousePressed(event, data)
    elif (data.mode == "editFunction"): editFunctionMousePressed(event,data)
    elif (data.mode == "createFunction"): createFunctionMousePressed(event,data)
    elif (data.mode == "functionDescription"): functionDescriptionMousePressed(event, data)
    elif (data.mode == "linePrompts"): linePromptsMousePressed(event, data)
    elif (data.mode == "sampleCode"): sampleCodeMousePressed(event, data)
    elif (data.mode == "studentHome"): studentHomeMousePressed(event, data)
    elif (data.mode == "practiceFunction"): practiceFunctionMousePressed(event, data)
    elif (data.mode == "studentDescription"): studentDescriptionMousePressed(event, data)
    elif (data.mode == "functionBuilder"): functionBuilderMousePressed(event, data)
    elif (data.mode == 'testCase'): testCaseMousePressed(event, data)
    elif (data.mode == 'recursionVisualizer'): recursionVisualizerMousePressed(event, data)
    elif (data.mode == 'list2dVisualizer'): list2dVisualizerMousePressed(event, data)

def keyPressed(event, data):
    if (data.mode == "startState"): startStateKeyPressed(event, data)
    elif (data.mode == "studentLogin"): studentLoginKeyPressed(event, data)
    elif (data.mode == "teacherLogin"): teacherLoginKeyPressed(event, data)
    elif (data.mode == "functionSelection"): functionSelectionKeyPressed(event, data)
    elif (data.mode == "editFunction"): editFunctionKeyPressed(event, data)
    elif (data.mode == "createFunction"): createFunctionKeyPressed(event, data)
    elif (data.mode == "functionDescription"): functionDescriptionKeyPressed(event, data)
    elif (data.mode == "linePrompts"): linePromptsKeyPressed(event, data)
    elif (data.mode == "sampleCode"): sampleCodeKeyPressed(event, data)
    elif (data.mode == "studentHome"): studentHomeKeyPressed(event, data)
    elif (data.mode == "practiceFunction"): practiceFunctionKeyPressed(event, data)
    elif (data.mode == "studentDescription"): studentDescriptionKeyPressed(event, data)
    elif (data.mode == "functionBuilder"): functionBuilderKeyPressed(event, data)
    elif (data.mode == 'testCase'): testCaseKeyPressed(event, data)
    elif (data.mode == 'recursionVisualizer'): recursionVisualizerKeyPressed(event, data)
    elif (data.mode == 'list2dVisualizer'): list2dVisualizerKeyPressed(event, data)

def redrawAll(canvas, data):
    if (data.mode == "startState"): startStateRedrawAll(canvas, data)
    elif (data.mode == "studentLogin"): studentLoginRedrawAll(canvas, data)
    elif (data.mode == "teacherLogin"): teacherLoginRedrawAll(canvas, data)
    elif (data.mode == "functionSelection"): functionSelectionRedrawAll(canvas, data)
    elif (data.mode == "editFunction"): editFunctionRedrawAll(canvas, data)
    elif (data.mode == "createFunction"): createFunctionRedrawAll(canvas, data)
    elif (data.mode == "functionDescription"): functionDescriptionRedrawAll(canvas, data)
    elif (data.mode == "linePrompts"): linePromptsRedrawAll(canvas, data)
    elif (data.mode == "sampleCode"): sampleCodeRedrawAll(canvas, data)
    elif (data.mode == "studentHome"): studentHomeRedrawAll(canvas, data)
    elif (data.mode == "practiceFunction"): practiceFunctionRedrawAll(canvas, data)
    elif (data.mode == "studentDescription"): studentDescriptionRedrawAll(canvas, data)
    elif (data.mode == "functionBuilder"): functionBuilderRedrawAll(canvas, data)
    elif (data.mode == 'testCase'): testCaseRedrawAll(canvas, data)
    elif (data.mode == 'recursionVisualizer'): recursionVisualizerRedrawAll(canvas, data)
    elif (data.mode == 'list2dVisualizer'): list2dVisualizerRedrawAll(canvas, data)

####################################
# RUN FUNCTION
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    root = Tk()
    root.resizable(width=False, height=False)
    init(data)
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    redrawAll(canvas, data)
    root.mainloop()

run(700, 400)
