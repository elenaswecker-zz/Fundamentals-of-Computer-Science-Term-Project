from tkinter import *

####################################
#setting up sql
####################################

import sqlite3

conn = sqlite3.connect('termproject.db')
c = conn.cursor()

def createTable(tableName):
    c.execute('CREATE TABLE IF NOT EXISTS %s(teacher REAL, username TEXT,    password TEXT, coursecode REAL)' % (tableName))
    
def dataEntryLoginInfo(teacher, username, password, coursecode):
    c.execute('INSERT INTO logininfo VALUES(%d, %s, %s, %d)' % (teacher, username, password, coursecode))
    conn.commit()
    c.close()
    conn.close()

####################################
#adapted model from course notes
####################################

def init(data):
    data.mode = "startState"
    data.studentTextBox = [data.width*6/16, data.height*7/16, \
        data.width*10/16, data.height*9/16]
    data.teacherTextBox = [data.width*6/16, data.height*10/16, \
        data.width*10/16, data.height*12/16]
    data.backButton = [data.width*14/16, data.height*14/16, data.width*15/16, \
        data.height*15/16]
    
####################################
# mode dispatcher
####################################

def mousePressed(event, data):
    if (data.mode == "startState"): startStateMousePressed(event, data)
    elif (data.mode == "studentLogin"): studentLoginMousePressed(event,data)
    elif (data.mode == "teacherLogin"): teacherLoginMousePressed(event,data)

def keyPressed(event, data):
    if (data.mode == "startState"): startStateKeyPressed(event, data)
    elif (data.mode == "studentLogin"): studentLoginKeyPressed(event, data)
    elif (data.mode == "teacherLogin"): teacherLoginMousePressed(event, data)

def redrawAll(canvas, data):
    if (data.mode == "startState"): startStateRedrawAll(canvas, data)
    elif (data.mode == "studentLogin"): studentLoginRedrawAll(canvas, data)
    elif (data.mode == "teacherLogin"): teacherLoginRedrawAll(canvas, data)

####################################
# startState mode
####################################

def startStateKeyPressed(event, data):
    pass
    
def startStateMousePressed(event, data):
    if event.x > data.studentTextBox[0] and event.x < \
        data.studentTextBox[2] and event.y > data.studentTextBox[1] and \
        event.y < data.studentTextBox[3]:
        data.mode = "studentLogin"
    elif event.x > data.teacherTextBox[0] and event.x < \
        data.teacherTextBox[2] and event.y > data.teacherTextBox[1] and \
        event.y < data.teacherTextBox[3]:
        data.mode = "teacherLogin"

def startStateRedrawAll(canvas, data):
    canvas.create_text(data.width/2, data.height/4, text = "NAME", font=\
        ("Courier", 44))
    sx1, sy1, sx2, sy2 = data.studentTextBox
    tx1, ty1, tx2, ty2 = data.teacherTextBox
    canvas.create_rectangle(sx1, sy1, sx2, sy2)
    canvas.create_text((sx1+sx2)/2, (sy1+sy2)/2, text = "STUDENT")
    canvas.create_rectangle(tx1, ty1, tx2, ty2)
    canvas.create_text((tx1+tx2)/2, (ty1+ty2)/2, text = "TEACHER")
        
####################################
# studentLogin mode
####################################

def studentLoginKeyPressed(event, data):
    pass
    
def studentLoginMousePressed(event, data):
    if event.x > data.backButton[0] and event.x < \
        data.backButton[2] and event.y > data.backButton[1] and \
        event.y < data.backButton[3]:
        data.mode = "startState"

def studentLoginRedrawAll(canvas, data):
    canvas.create_text(data.width/2, data.height/4, text = "Student Login", \
        font= ("Courier", 44))
    bx1, by1, bx2, by2 = data.backButton
    canvas.create_rectangle(bx1, by1, bx2, by2)
    canvas.create_text((bx1+bx2)/2, (by1+by2)/2, text = "back")
        
####################################
# teacherLogin mode
####################################

def teacherLoginKeyPressed(event, data):
    pass
    
def teacherLoginMousePressed(event, data):
    if event.x > data.backButton[0] and event.x < \
        data.backButton[2] and event.y > data.backButton[1] and \
        event.y < data.backButton[3]:
        data.mode = "startState"

def teacherLoginRedrawAll(canvas, data):
    canvas.create_text(data.width/2, data.height/4, text = "Teacher Login", \
        font= ("Courier", 44))
    bx1, by1, bx2, by2 = data.backButton
    canvas.create_rectangle(bx1, by1, bx2, by2)
    canvas.create_text((bx1+bx2)/2, (by1+by2)/2, text = "back")

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
