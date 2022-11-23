from tkinter import *
import random
import time
from tkinter import messagebox
import serial
import requests

arduino_port = "/dev/cu.usbmodem14101" #serial port of Arduino
baud = 115200 #arduino uno runs at 9600 baud
WIRELESS = True
PLAYER_2_IMU = True
INIT_SCORE = 3
http_req_url = "http://192.168.1.224/L"

if not WIRELESS:
    ser = serial.Serial(arduino_port, baud)
    print("Connected to Arduino port:" + arduino_port)

# Game: PONG GAME FOR IMUs
# Author/Editor: Dacheng Lin

# Resource(s):
# what: having a basic Pong Game for one player in python
# where: https://github.com/kidscancode/intro-python-code/blob/master/pong%20game.py
# why: build a simple pong game, now it's being modified so the paddle can
# be control by the data from the adriuno 33 iot sensor and additional paddle for
# for potential 2 player game

# Define ball properties and functions
class Ball:
    def __init__(self, canvas, color, size, paddle, paddle2):
        self.canvas = canvas
        self.paddle = paddle
        self.paddle2 = paddle2
        self.id = canvas.create_oval(10, 10, size, size, fill=color)
        self.canvas.move(self.id, 245, 300) # initialize pos
        self.xspeed = random.randrange(-25,25)
        self.yspeed = -15
        self.hit_bottom = False
        self.hit_top = False
        self.score = INIT_SCORE
        self.score_2 = INIT_SCORE

    def draw(self):
        # check to see if the ball is not hitting bottom/top
        self.canvas.move(self.id, self.xspeed, self.yspeed)
        pos = self.canvas.coords(self.id)

        if self.hit_top == True and self.score_2 >= 0:
            self.score_2 -= 1
            self.hit_top = False
        else:  # check the bound for hitting top
            if pos[1] <= 0:         # TOP UPPER BOUND
                self.hit_top = True
                self.yspeed = 15
        
        if self.hit_bottom == True and self.score >=0:
            self.score -= 1
            self.hit_bottom = False
 
        else:  # check the bound for hitting bottom
            if pos[3] >= 400 :   # BOTTOM UPPER BOUND
                # mark the condition
                self.hit_bottom = True
                self.yspeed = -15
            
        
        if pos[0] <= 0:         # LEFT LOWER BOUND
            self.xspeed = 15
                
        if pos[2] >= 500:       # RIGHT UPPER BOUND
            self.xspeed = -15
        if self.hit_paddle(pos) == True and self.yspeed >= 0: # check hit from top
            self.yspeed = -15
            self.xspeed = random.randrange(-25,25) # randomize the x dir
            self.score += 1
        if self.hit_paddle2(pos) == True and self.yspeed < 0: # check from bottem
            self.yspeed = 15
            self.xspeed = random.randrange(-25,25) # randomize the x dir
            self.score_2 += 1

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False
    
    def hit_paddle2(self, pos):
        paddle_pos = self.canvas.coords(self.paddle2.id)
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
        self.left_move = False
        self.right_move = False

    def check(self, next_pos):
        next_move = float(next_pos)

        # check for sensor movement for az IMU
        if abs(self.sensor_pos - next_move) < 0.05 :  # hold still
            if self.left_move:
                self.move_left(None)
            else:
                self.move_right(None)
                
        elif next_move >= 0 : # postive az IMU for moving right for IoT face up
            self.right_move = True
            self.left_move = False
            self.move_right(None)
        else:                # negative az IMU for IoT face down
            self.left_move = True
            self.right_move = False
            self.move_left(None)
           
        self.sensor_pos = next_move
        
    def draw(self):
        self.canvas.move(self.id, self.xspeed, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.xspeed = 5
        if pos[2] >= 500:
            self.xspeed = -5

    def move_left(self, evt):
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.xspeed = 0
        else:
            self.xspeed = -20
    def move_right(self, evt):
        pos = self.canvas.coords(self.id)
        if pos[2] >= 500:
            self.xspeed = 0
        else:
            self.xspeed = 20

class PaddleUp:
    def __init__(self, canvas, color, hor, ver, sensor_pos):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, hor, ver, fill=color)
        self.canvas.move(self.id, 200, 50)
        self.xspeed = 0
        self.sensor_pos = sensor_pos
        self.left_move = False
        self.right_move = False
        
        if not PLAYER_2_IMU:
            self.canvas.bind_all('<KeyPress-Left>', self.move_left)
            self.canvas.bind_all('<KeyPress-Right>', self.move_right)
    
    def check(self, next_pos):
        next_move = float(next_pos)
#        print("Current2: ", self.sensor_pos)
#        print("Next2: ", next_move)

        # check for sensor movement for az IMU
        if abs(self.sensor_pos - next_move) < 0.05 :  # hold still
            if self.left_move:
                self.move_left(None)
            else:
                self.move_right(None)
                
        elif next_move >= 0 : # postive az IMU for moving right for IoT face up
            self.right_move = True
            self.left_move = False
            self.move_right(None)
        else:                # negative az IMU for IoT face down
            self.left_move = True
            self.right_move = False
            self.move_left(None)
           
        self.sensor_pos = next_move

    def draw(self):
        self.canvas.move(self.id, self.xspeed, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.xspeed = 5
        if pos[2] >= 500:
            self.xspeed = -5

    def move_left(self, evt):
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.xspeed = 0
        else:
            self.xspeed = -20
    def move_right(self, evt):
        pos = self.canvas.coords(self.id)
        if pos[2] >= 500:
            self.xspeed = 0
        else:
            self.xspeed = 20

def parsed_num_list(url):
    try:
        r = requests.get(url,verify=False)
        lines = r.text.split('\n')
        parsed_nums = []
        for item in lines:
            num = item[0:][:-1] # get rid of the end line char
            
            #check the type
            isFloat=True

            try:
                num = float(num)
            except ValueError:
                isFloat=False

            if isFloat:
                parsed_nums.append(num)
        
        return parsed_nums
    except requests.exceptions.ConnectionError:
        return [0]


# Create window and canvas to draw on
tk = Tk()
tk.title("Pong Game")
canvas = Canvas(tk, width=500, height=400, bd=0, bg='LavenderBlush1')
canvas.pack()
label = canvas.create_text(5, 5, anchor=NW, text="Score: 0",
                           font="Times 17 italic bold")
label_2 = canvas.create_text(5, 380, anchor=NW, text="Score: 0",
                             font="Times 17 italic bold")
tk.update()

# create objects for the IMU data [id,ax,ay,az,gx,gy,gz]
readings = []

if not WIRELESS:
    getData=ser.readline()
    dataString = getData.decode('utf-8')
    data=dataString[0:][:-2]  # get rid of the endline characters "\r\n"
    print(data)
    readings = data.split(",") # list of sensor coord (x)
else:
    readings = parsed_num_list(http_req_url)
    
paddle = Paddle(canvas, 'blue', 100, 10, readings[3])
paddle_top = PaddleUp(canvas, 'yellow', 100, 10, readings[3])
ball = Ball(canvas, 'red', 25, paddle, paddle_top)

# Animation loop and getting data from adriuno
while ball.score >= 0:
    
    if not WIRELESS:
        getData=ser.readline()
        dataString = getData.decode('utf-8')
        data=dataString[0:][:-2]  # get rid of the endline characters "\r\n"

        readings = data.split(",") # list of sensor coord (x)
    else:
        readings = parsed_num_list(http_req_url)
    ball.draw()
    #canvas.bind_all(readings[0], paddle.check)
    if readings[0] == 0:   # player 1 ID is 0
        paddle.check(readings[3])
    if readings[0] == 1:   # player 2 ID is 1
        paddle_top.check(readings[3])
    paddle.draw()
    paddle_top.draw()
    canvas.itemconfig(label, text="Score: "+str(ball.score_2))
    canvas.itemconfig(label_2, text="Score: "+str(ball.score))
    tk.update_idletasks()
    tk.update()
    time.sleep(0.1)

# Game Over
messagebox.showinfo("Message","Game Over! Come and Play next time!")
tk.update()


