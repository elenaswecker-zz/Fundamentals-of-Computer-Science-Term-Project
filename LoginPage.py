#The first modes of the program: home page, student login, teacher login
#This file establishes the graphics for these modes as well as creating the associated database tables for information (login, courses, functions) storage

####################################
#sqlite3
####################################

import sqlite3

conn = sqlite3.connect('termproject.db')
c = conn.cursor()

def createLoginInfoTable():
    #establishes login info table whenever program is run
    c.execute("""CREATE TABLE IF NOT EXISTS logininfo (username TEXT, password TEXT, coursecode REAL)""")
    
createLoginInfoTable()

def dataEntryLoginInfo(username, password, coursecode):
    #adds specific login info to table
    c.execute("""INSERT INTO logininfo VALUES('%s', '%s', %d)""" % (username, password, int(coursecode)))
    conn.commit()

def createCourseTable(courseCode):
    #creates table to storage functions associated with a particular course
    c.execute("""CREATE TABLE IF NOT EXISTS %s(funcName TEXT)""" % ("a" + str(courseCode)))
    
def createProgressTable(username, courseCode):
    #creates table to record user's progress with their functions
    c.execute("""CREATE TABLE IF NOT EXISTS %s (functionName TEXT, lineNum REAL, completed REAL)""" %(username+ "Progress"))
    dataEntryFunctionProgress(username, courseCode)
    
def getProgress(function, username):
    #returns a user's current progress with a particular function
    command = """SELECT lineNum from %s WHERE functionName = '%s'""" %(username + "Progress", function)
    c.execute(command)
    progress = c.fetchone()
    return progress
    
def getPassword(username):
    #returns the correct password for a previously utilized username
    command = """SELECT password from logininfo WHERE username = '%s'""" %(username)
    c.execute(command)
    password = c.fetchone()
    return password
    
def dataEntryFunctionProgress(username, courseCode):
    #initializes function progress for a particular user
    c.execute("""SELECT * FROM %s""" %("a" + str(courseCode)))
    data = c.fetchall()
    for function in data:
        if getProgress(function[0], username) == None:
            c.execute("""INSERT INTO %s VALUES('%s', 1, 0)""" %(username + "Progress", function[0]))
            conn.commit()

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
    
def reset(data):
    #reinitializes login info
    data.username = 'username here'
    data.password = 'password here'
    data.courseCode = 'course code (#) here'
    
def clickCheck(event, box):
    #checks if a box is clicked in
    if event.x > box[0] and event.x < box[2] and event.y > box[1] and event.y < box[3]:
        return True
    else:
        return False

####################################
# startState mode
####################################

def startStateKeyPressed(event, data):
    pass
    
def startStateMousePressed(event, data):
    if clickCheck(event, data.studentTextBox):
        data.mode = "studentLogin"
    elif clickCheck(event, data.teacherTextBox):
        data.mode = "teacherLogin"

def startStateRedrawAll(canvas, data):
    canvas.create_text(data.width/2, data.height/4, text = "Interactive Python Trainer", font= ("Courier New", 30, "bold"))
    canvas.create_rectangle(data.studentTextBox)
    canvas.create_text(centerOfRectangle(data.studentTextBox), text = "STUDENT", font= ("Courier New", 10))
    canvas.create_rectangle(data.teacherTextBox)
    canvas.create_text(centerOfRectangle(data.teacherTextBox), text = "TEACHER", font= ("Courier New", 10))
        
####################################
# studentLogin mode
####################################

def studentLoginKeyPressed(event, data):
    if data.currentBox == 'password' or data.currentBox == 'username' or data.currentBox == 'courseCode':
        if event.char in data.inputs:
            data.current += event.char
        elif event.keysym == "space":
            data.current += " "
        elif event.keysym == "Tab":
            data.current += "    "
        elif event.keysym == "BackSpace":
            data.current = data.current[:len(data.current)-1]
        if data.currentBox == 'username':
            data.username = data.current
        elif data.currentBox == 'password':
            data.password = data.current
        elif data.currentBox == 'courseCode':
            data.courseCode = data.current
    
def studentLoginMousePressed(event, data):
    data.notACourseCode = False
    data.wrongPassword = False
    if clickCheck(event, data.backButton):
        #back to startState
        reset(data)
        data.mode = "startState"
    if clickCheck(event, data.submitButton) and data.username != 'username here' and data.password != 'password here' and data.courseCode != 'course code (#) here':
        #submitting login info
        if getPassword(data.username) != None:
            #if password has been set before for given username
            if getPassword(data.username)[0] == data.password:
                #if inputted password is correct
                try:
                    #try to see if courseCode has associated functions
                    createProgressTable(data.username, data.courseCode)
                    data.mode = 'studentHome'
                except:
                    #if courseCode has no associated functions
                    data.notACourseCode = True
            else:
                #if password is wrong
                data.wrongPassword = True
        else:
            #if new user
            try:
                #try to see if courseCode has associated functions
                createProgressTable(data.username, data.courseCode)
                dataEntryLoginInfo(data.username, data.password, data.courseCode)
                data.mode = 'studentHome'
            except:
                #if courseCode has no associated functions
                data.notACourseCode = True
    if clickCheck(event, data.usernameBox):
        data.current = ''
        data.currentBox = 'username'
        if data.password == '': data.password = 'password here'
        if data.courseCode == '': data.courseCode = 'course code (#) here'
        if data.username == "username here": data.username = ''
    elif clickCheck(event, data.passwordBox):
        data.current = ''
        data.currentBox = 'password'
        if data.username == '': data.username = 'username here'
        if data.courseCode == '': data.courseCode = 'course code (#) here'
        if data.password == "password here": data.password = ''
    elif clickCheck(event, data.courseCodeBox):
        data.currentBox = 'courseCode'
        data.current = ''
        if data.username == '': data.username = 'username here'
        if data.password == '': data.password = 'password here'
        if data.courseCode == "course code (#) here": data.courseCode = ''
    else:
        if data.username == '': data.username = 'username here'
        if data.password == '': data.password = 'password here'
        if data.courseCode == '': data.courseCode = 'course code (#) here'

def studentLoginRedrawAll(canvas, data):
    if data.notACourseCode:
        #courseCode error message
        canvas.create_text(centerOfRectangle(data.courseCodeBox), text = "Course does not exist", fill = "red", font= ("Courier New", 10))
        data.courseCode = ''
        data.current = ''
    if data.wrongPassword:
        #password error message
        canvas.create_text(centerOfRectangle(data.passwordBox), text = "Incorrect password", fill = 'red', font= ("Courier New", 10))
        data.password = ''
        data.current = ''
    canvas.create_text(data.width/2, data.height/4, text = "Student Login", font= ("Courier New", 30, "bold"))
    canvas.create_rectangle(data.usernameBox)
    canvas.create_text(leftAlign(data.usernameBox), text = data.username, anchor = 'w', font= ("Courier New", 10))
    canvas.create_rectangle(data.passwordBox)
    canvas.create_text(leftAlign(data.passwordBox), text = data.password, anchor = 'w', font= ("Courier New", 10))
    canvas.create_rectangle(data.courseCodeBox)
    canvas.create_text(leftAlign(data.courseCodeBox), text = data.courseCode, anchor = 'w', font= ("Courier New", 10))
    canvas.create_rectangle(data.backButton)
    canvas.create_text(centerOfRectangle(data.backButton), text = "back", font= ("Courier New", 10))
    canvas.create_rectangle(data.submitButton)
    canvas.create_text(centerOfRectangle(data.submitButton), text = "SUBMIT", font= ("Courier New", 10))

####################################
# teacherLogin mode
####################################

def teacherLoginKeyPressed(event, data):
    if data.currentBox == 'password' or data.currentBox == 'username' or data.currentBox == 'courseCode':
        if event.char in data.inputs:
            data.current += event.char
        elif event.keysym == "space":
            data.current += " "
        elif event.keysym == "Tab":
            data.current += "    "
        elif event.keysym == "BackSpace" and len(data.current) > 0:
            data.current = data.current[:len(data.current)-1]
        if data.currentBox == 'username':
            data.username = data.current
        elif data.currentBox == 'password':
            data.password = data.current
        elif data.currentBox == 'courseCode':
            data.courseCode = data.current
    
def teacherLoginMousePressed(event, data):
    data.courseCodeNotNumbers = False
    data.wrongPassword = False
    if clickCheck(event, data.backButton):
        #back to startState
        reset(data)
        data.mode = "startState"
    if clickCheck(event, data.submitButton) and data.username != 'username here' and data.password != 'password here' and data.courseCode != 'course code (#) here':
        #submitting login info
        if getPassword(data.username) != None:
            #if password has been set before for given username
            if getPassword(data.username)[0] == data.password:
                #if inputted password is correct
                try:
                    #try to see if courseCode is just numbers
                    for letter in data.inputs:
                        if letter not in "1234567890":
                            if letter in data.courseCode:
                                assert(True == False)
                    createCourseTable(str(data.courseCode))
                    data.mode = 'functionSelection'
                except:
                    #if courseCode has non-numerical characters
                    data.courseCodeNotNumbers = True
                    data.current = ''
                    data.courseCode = ' '
            else:
                #if password is wrong
                data.wrongPassword = True
        else:
            #if new user
            try: 
                #try to see if courseCode is just numbers
                for letter in data.inputs:
                    if letter not in "1234567890":
                        if letter in data.courseCode:
                            assert(True == False)
                createCourseTable(str(data.courseCode))
                dataEntryLoginInfo(data.username, data.password, data.courseCode)
                data.mode = 'functionSelection'
            except:
                #if courseCode has non-numerical characters
                data.courseCodeNotNumbers = True
                data.current = ''
                data.courseCode = ' '
    if clickCheck(event, data.usernameBox):
        data.current = ''
        data.currentBox = 'username'
        if data.password == '': data.password = 'password here'
        if data.courseCode == '': data.courseCode = 'course code (#) here'
        if data.username == "username here": data.username = ''
    elif clickCheck(event, data.passwordBox):
        data.current = ''
        data.currentBox = 'password'
        if data.username == '': data.username = 'username here'
        if data.courseCode == '': data.courseCode = 'course code (#) here'
        if data.password == "password here": data.password = ''
    elif clickCheck(event, data.courseCodeBox):
        data.currentBox = 'courseCode'
        data.current = ''
        if data.username == '': data.username = 'username here'
        if data.password == '': data.password = 'password here'
        if data.courseCode == "course code (#) here": data.courseCode = ''
    else:
        if data.username == '': data.username = 'username here'
        if data.password == '': data.password = 'password here'
        if data.courseCode == '': data.courseCode = 'course code (#) here'

def teacherLoginRedrawAll(canvas, data):
    if data.courseCodeNotNumbers:
        #courseCode error message
        canvas.create_text(centerOfRectangle(data.courseCodeBox), text = "Only use numbers for course code", fill = 'red', font= ("Courier New", 9))
    if data.wrongPassword:
        #password error message
        canvas.create_text(centerOfRectangle(data.passwordBox), text = "Incorrect password", fill = 'red', font= ("Courier New", 10))
        data.password = ''
        data.current = ''
    canvas.create_text(data.width/2, data.height/4, text = "Teacher Login", font= ("Courier New", 30, "bold"))
    canvas.create_rectangle(data.usernameBox)
    canvas.create_text(leftAlign(data.usernameBox), text = data.username, anchor = 'w', font= ("Courier New", 10))
    canvas.create_rectangle(data.passwordBox)
    canvas.create_text(leftAlign(data.passwordBox), text = data.password, anchor = 'w', font= ("Courier New", 10))
    canvas.create_rectangle(data.courseCodeBox)
    canvas.create_text(leftAlign(data.courseCodeBox), text = data.courseCode, anchor = 'w', font= ("Courier New", 10))
    canvas.create_rectangle(data.backButton)
    canvas.create_text(centerOfRectangle(data.backButton), text = "back", font= ("Courier New", 10))
    canvas.create_rectangle(data.submitButton)
    canvas.create_text(centerOfRectangle(data.submitButton), text = "SUBMIT", font= ("Courier New", 10))