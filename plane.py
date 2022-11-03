import pyglet
from GraphWindow import GraphWindow

class Plane(object):
    """Plane for the graphical interface"""
    def __init__(self):
        self.circles = []
        self.lines = []
        self.graphWindow = None

    def graph(self,left,right,top,bottom):
        window = GraphWindow(self,1,50,left,right,top,bottom)
        self.graphWindow = window
        pyglet.app.run()