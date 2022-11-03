import pyglet
from pyglet.gl import *

class Line(object):
    """The Line which store start point and end point : these are to be created from user input in Main.
    Gradients also store the points of the circle where the gradient was found. Index 2 store the gradient."""
    def __init__(self,plane):
        self.plane = plane
        self.plane.lines.append(self)
        self.c = None
        self.points = []
        self.significantPoints = []
        self.maxGrad = None
        self.gradients = []
        self.color = (0, 255, 0)

    def draw(self):
        x1 = self.plane.graphWindow.transformX(point = self.points[0][0])
        y1 = self.plane.graphWindow.transformY(point = self.points[0][1])
        x2 = self.plane.graphWindow.transformX(point = self.points[1][0])
        y2 = self.plane.graphWindow.transformY(point = self.points[1][1])
        #shapes.Line(x1,y1,x2,y2, color = self.color, batch = self.plane.graphWindow.batch).draw()
        self.plane.graphWindow.batch.add(2, pyglet.gl.GL_LINES, None, 
            ('v2f', (x1, y1, x2, y2)),
            ('c3B', (0, 0, 255, 0, 0, 255))
        )
        self.drawSignificantPoints()
        self.hover()

    def drawSignificantPoints(self):
        for pt in self.significantPoints:
            x = self.plane.graphWindow.transformX(point = pt[0])
            y = self.plane.graphWindow.transformY(point = pt[1])
            #shapes.Circle(x = x,y = y,radius = 8,color = (0,0,255),batch = self.plane.graphWindow.batch).draw()
            pyglet.text.Label("({},{})".format(round(pt[0],2),round(pt[1],2)),
                          font_name='Times New Roman',
                          font_size=10,
                          x=x, y=y,
                          color=(0, 0, 0, 255),
                          batch = self.plane.graphWindow.batch)

    def hover(self):
        x = self.plane.graphWindow._mouse_x
        graphX = self.plane.graphWindow.transformX(pixel = x)
        graphY = self.getY(graphX)
        if not isinstance(graphY, complex):
            y = self.plane.graphWindow.transformY(point = graphY)
            #shapes.Circle(x = x,y = y,radius = 8,color = (0,0,255),batch = self.plane.graphWindow.batch).draw()
            pyglet.text.Label("({},{})".format(round(graphX,2),round(graphY,2)),
                          font_name='Times New Roman',
                          font_size=10,
                          x=x, y=y,
                          color=(0, 0, 0, 255),
                          batch = self.plane.graphWindow.batch)

    def calcGradient(self,x1,y1,x2,y2):
        return ((y2-y1)/(x2-x1))

    def generateGradients(self,circle,step):
        print("Calculating All Gradients....")
        gradients = []
        x = circle.getMin()
        max = circle.getMax()
        while (x <= max):
            y = circle.getY(x)
            if not isinstance(y, complex):
                grad = self.calcGradient(self.points[0][0],self.points[0][1],x,y)
                gradients.append([x,y,grad])
                x+=step
        grad = self.calcGradient(self.points[0][0],self.points[0][1],max,circle.getY(max))
        gradients.append([max,circle.getY(max),grad])
        print("Done!")
        self.gradients = gradients
        circle.points = gradients
        self.setMaxGradient(circle)
        return self.gradients

    def setMaxGradient(self,circle):
        if (circle.h < self.points[0][0]): # Down Slope
            self.maxGrad = min(self.gradients,key = lambda x: x[2])[2]
        elif (circle.h > self.points[0][0]): # Up Slope
            self.maxGrad = max(self.gradients,key = lambda x: x[2])[2]

    def getMaxGradAngle(self):
        return self.maxGrad

    def getYintercept(self):
        # y=mx + c
        x = self.points[0][0]
        y = self.points[0][1]
        self.c = y - self.maxGrad * x
        return self.c

    def getY(self,x):
        return self.maxGrad*x + self.c

    def getX(self,y):
        return (y - self.c) / self.maxGrad

    def addPoint(self,pt):
        self.points.append(pt)

    def addSignificantPoint(self,pt):
        self.significantPoints.append(pt)

    def clearSignificantPoints(self):
        self.significantPoints = []

