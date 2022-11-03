import pyglet

class Circle(object):
    """the semi-circle which contains the points and gradients and other related variables. 
    Keep in mind, the points are created from the line when gradients are formed. 
    This avoids looping unnecessarily"""
    def __init__(self,plane):
        self.plane = plane
        self.plane.circles.append(self)
        self.points = []
        self.significantPoints = []
        self.r = None
        self.h = None
        self.color = (255, 0, 0)

    def draw(self):
        i = 0
        while (i < len(self.points) - 1):
            x1 = self.plane.graphWindow.transformX(point = self.points[i][0])
            y1 = self.plane.graphWindow.transformY(point = self.points[i][1])
            x2 = self.plane.graphWindow.transformX(point = self.points[i + 1][0])
            y2 = self.plane.graphWindow.transformY(point = self.points[i + 1][1])
            #shapes.Line(x1,y1,x2,y2, color = self.color, batch = self.plane.graphWindow.batch).draw()
            self.plane.graphWindow.batch.add(2, pyglet.gl.GL_LINES, None, 
                ('v2f', (x1, y1, x2, y2)),
                ('c3B', (255, 0, 0, 255, 0, 0))
            )
            i += 1
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

    def getY(self,x):
        # y = sqrt ( r^2 - ( x - h )^2 )
        return (self.r**2-(x-self.h)**2)**(1/2)

    def addPoint(self,pt):
        self.points.append(pt)

    def addSignificantPoint(self,pt):
        if not isinstance(pt[1],complex):
            self.significantPoints.append(pt)

    def clearSignificantPoints(self):
        self.significantPoints = []

    def setR(self,r):
        if (r < 0):
            r *= -1
        self.r = r

    def getMin(self):
        return self.h - self.r

    def getMax(self):
        return self.h + self.r


