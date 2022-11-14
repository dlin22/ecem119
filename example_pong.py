from tkinter import *
import random
import time
from tkinter import messagebox
import serial

arduino_port = "/dev/cu.usbmodem14101" #serial port of Arduino
baud = 9600 #arduino uno runs at 9600 baud

ser = serial.Serial(arduino_port, baud)
print("Connected to Arduino port:" + arduino_port)
sensor_data = [] #store data

# what: having a basic Pong Game for one player in python
# where: https://github.com/kidscancode/intro-python-code/blob/master/pong%20game.py
# why: build a simple pong game, now it's being modified so the paddle can
# be control by the data from the adriuno 33 iot sensor and additional paddle for 
# for potential 2 player game

# Define ball properties and functions
class Ball:
    def __init__(self, canvas, color, size, paddle):
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, size, size, fill=color)
        self.canvas.move(self.id, 245, 300) # initialize pos
        self.xspeed = random.randrange(-3,3)
        self.yspeed = -1
        self.hit_bottom = False
        self.score = 3

    def draw(self):
        # check to see if the ball is not hitting bottom
        

        self.canvas.move(self.id, self.xspeed, self.yspeed)
        pos = self.canvas.coords(self.id)

        if pos[1] <= 0:
            self.yspeed = 3
        
        if self.hit_bottom == True and self.score >=0:
            self.score -= 1
            self.hit_bottom = False
 
        else:  # check the bound for hitting
            if pos[3] >= 400 :   # horizontal upper bound
                # mark the condition
                self.hit_bottom = True
                self.yspeed = -3
            
        if pos[0] <= 0:
            self.xspeed = 3
        if pos[2] >= 500:
            self.xspeed = -3
        if self.hit_paddle(pos) == True:
            self.yspeed = -3
            self.xspeed = random.randrange(-3,3) # randomize the x dir 
            self.score += 1

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False

# Define paddle properties and functions
class Paddle:
    def __init__(self, canvas, color, hor, ver, sensor_pos):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, hor, ver, fill=color)
        self.canvas.move(self.id, 200, 350)
        self.xspeed = 0
        #self.canvas.bind_all('<KeyPress-Left>', self.move_left)
        #self.canvas.bind_all('<KeyPress-Right>', self.move_right)
        self.sensor_pos = float(sensor_pos)

    def check(self, next_pos):
        next_move = float(next_pos)
        print("Current: ", self.sensor_pos)
        print("Next: ", next_move)

        # check for sensor movement
        if (next_move > 1):
            self.move_right(None)
        elif (next_move < -1):
            self.move_left(None)
        elif (next_move > self.sensor_pos and 
            abs(next_move - self.sensor_pos) > 0.05):
            self.move_left(None)
            self.sensor_pos = next_move
        elif (next_move < self.sensor_pos and 
              abs(next_move - self.sensor_pos) > 0.05):
            self.move_right(None)
            self.sensor_pos = next_move

    def draw(self):
        
        self.canvas.move(self.id, self.xspeed, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.xspeed = 1
        if pos[2] >= 500:
            self.xspeed = -1

    def move_left(self, evt):
        self.xspeed = -3
    def move_right(self, evt):
        self.xspeed = 3

class PaddleUp:
    def __init__(self, canvas, color, hor, ver):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, hor, ver, fill=color)
        self.canvas.move(self.id, 200, 50)
        self.xspeed = 0
  

    def draw(self):
        self.canvas.move(self.id, self.xspeed, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.xspeed = 0
        if pos[2] >= 500:
            self.xspeed = 0

    def move_left(self, evt):
        self.xspeed = -2
    def move_right(self, evt):
        self.xspeed = 2



# Create window and canvas to draw on
tk = Tk()
tk.title("Pong Game")
canvas = Canvas(tk, width=500, height=400, bd=0, bg='LavenderBlush1')
canvas.pack()
label = canvas.create_text(5, 5, anchor=NW, text="Score: 0",
                           font="Times 17 italic bold")
tk.update()

# create objects
getData=ser.readline()
dataString = getData.decode('utf-8')
data=dataString[0:][:-2]  # get rid of the endline characters "\r\n"
print(data)

readings = data.split(",") # list of sensor coord (x)
paddle = Paddle(canvas, 'blue', 100, 10, readings[0])
paddle_top = PaddleUp(canvas, 'yellow', 100, 10)
ball = Ball(canvas, 'red', 25, paddle)

# Animation loop and getting data from adriuno
while ball.score >= 0:
    getData=ser.readline()
    dataString = getData.decode('utf-8')
    data=dataString[0:][:-2]  # get rid of the endline characters "\r\n"

    readings = data.split(",") # list of sensor coord (x)
    ball.draw()
    #canvas.bind_all(readings[0], paddle.check)
    paddle.check(readings[0])
    paddle.draw()
    paddle_top.draw()
    canvas.itemconfig(label, text="Score: "+str(ball.score))
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)

# Game Over
messagebox.showinfo("Message","Game Over! Come and Play next time!")
tk.update()