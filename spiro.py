import turtle
import math
import random
import sys, argparse
import numpy as np
from PIL import Image # type: ignore
from datetime import datetime
from math import gcd

class Spiro:
    # Constructor
    def __init__(self, xc, yc, col, R, r, l):
        # Create a turtle object
        self.t = turtle.Turtle()
        # Set the cursor shape
        self.t.shape('turtle')
        # Set the step in degrees
        self.step = 5
        # Set the drawing complete flag
        self.drawingComplete = False
        
        # Set the parameters
        self.setparams(xc, yc, col, R, r, l)
        
        # Initialize the drawing
        self.restart()
    def setparams(self, xc, yc, col, R, r, l):
        self.xc = xc
        self.yc = yc
        self.col = col
        self.R = int(R)
        self.r = int(r)
        self.l = l
        # Reducing r/R to the smallest factor using their GCD
        gcdVal = gcd(self.r, self.R)
        self.nRot = self.r//gcdVal
        # Get ratio of radii
        self.k = r/float(R)
        # Set the color
        self.t.color(*col)
        # Store the current angle
        self.a = 0
    def restart(self):
        # Set the flag
        self.drawingComplete = False
        # Show the turle
        self.t.showturtle()
        # Go to first point
        self.t.up()
        R, k, l = self.R, self.k, self.l
        a = 0.0
        x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
        self.t.setpos(self.xc + x, self.yc + y)
        self.t.down()
    # Draws the whole thing
    def draw(self):
        R, k, l = self.R, self.k, self.l
        for i in range(0, 360*self.nRot + 1, self.step):
            a = math.radians(i)
            x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
            y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
            self.t.setpos(self.xc + x, self.yc + y)
        self.t.hideturtle()
    def update(self):
        if self.drawingComplete:
            return
        self.a += self.step
        R, k, l = self.R, self.k, self.l
        # Set the angle
        a = math.radians(self.a)
        x = self.R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = self.R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
        # If drawing is complete, set the flag
        if self.a == 360*self.nRot:
            self.drawingComplete = True
            self.t.hideturtle()

# For random spirographs
class SpiroAnimator:
    def __init__(self, N):
        # Set the timer value in milliseconds
        self.deltaT = 10
        self.width = turtle.window_width()
        self.height = turtle.window_height()
        # Create spiro objects
        self.spiros = []
        for i in range(N):
            # Generate random parameters
            rparams = self.genRandomParams()
            # Set the spiro params
            spiro = Spiro(*rparams)
            self.spiros.append(spiro)
            # Call the timer
            turtle.ontimer(self.update, self.deltaT)
    def genRandomParams(self):
        width, height = self.width, self.height
        R = random.randint(50, min(width, height)//2)
        r = random.randint(10, 9*R//10)
        l = random.uniform(0.1, 0.9)
        xc = random.randint(-width//2,width//2)
        yc = random.randint(-height//2, height//2)
        col = (random.random(),
               random.random(),
               random.random())
        return (xc, yc, col, R, r, l)
    def restart(self):
        for spiro in self.spiros:
            spiro.clear()
            rparams = self.genRandomParams()
            spiro.setparams(*rparams)
            spiro.restart()
    def update(self):
        nComplete = 0 
        for spiro in self.spiros:
            spiro.update()
            if spiro.drawingComplete:
                nComplete +=1
        if nComplete == len(self.spiros):
            self.restart()
        #Call the timer
        turtle.ontimer(self.update, self.deltaT)
        
    def toggleTurtles(self):
        for spiro in self.spiros:
            if spiro.t.isvisible():
                spiro.t.hideturtle()
            else:
                spiro.t.showtutle()
def saveDrawing():
    turtle.hideturtle()
    dateStr = (datetime.now()).strftime("%d%b%Y-%H%M%S")
    fileName = 'spiro' + dateStr
    print('Saving drawing')
    canvas = turtle.getcanvas()
    canvas.postscript(file = fileName + '.eps')
    img = Image.open(fileName + '.eps')
    img.save(fileName + '.png', 'png')
    turtle.showturtle()
def main():
    print('Generating spirograph...')
    parser = argparse.ArgumentParser()
    parser.add_argument('--sparams', nargs = 3, dest = 'sparams', required = False,
                        help = "The three arguments in sparams: R, r, l")
    args = parser.parse_args()
    turtle.setup(width=0.8)
    turtle.shape('turtle')
    turtle.title("Spirograpgh!")
    turtle.onkey(saveDrawing, "s")
    turtle.listen()
    turtle.hideturtle()
    if args.sparams:
        params = [float(x) for x in args.sparams]
        col = (0.0, 0.0, 0.0)
        spiro = Spiro(0, 0, col, *params)
        spiro.draw()
    else:
        spiroAnim = SpiroAnimator(4)
        turtle.onkey(spiroAnim.toggleTurtles, "t")
        turtle.onkey(spiroAnim.restart, "space")
    turtle.mainloop()
if __name__ == '__main__':
    main()