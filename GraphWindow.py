import pyglet
from pyglet.window import key
from pyglet.gl import *

class GraphWindow(pyglet.window.Window):
    def __init__(self,plane,zoom,padding,left,right,top,bottom):
        super(GraphWindow, self).__init__(1000,500,resizable = True)
        self.plane = plane

        # Input
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)

        joysticks = pyglet.input.get_joysticks()
        self.joystick = joysticks[0] if len(joysticks) > 0 else None
        if self.joystick is not None:
            self.joystick.open()
        self.joystickSensitivity = 50

        # Graph variables
        self.graph_width = right - left
        self.graph_height = top - bottom

        # Scaling variables
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.h_zoom = zoom
        self.v_zoom = zoom
        self.zoom_ratio = 1.1
        self.offset = [padding,padding]
        self.padding = padding

        # axes
        self.axes_step = 15

        # Graphics
        self.batch = pyglet.graphics.Batch()

        # Start the update loop
        pyglet.clock.schedule_interval(self.update, 1/60)

    #-----------------------------------Loops-----------------------------------#

    def update(self,dt):
        # calculating Scales
        self.h_scale = ((self.width - 2 * self.padding) / self.graph_width) * self.h_zoom
        self.v_scale = ((self.height - 2 * self.padding) / self.graph_height) * self.v_zoom
        self.scaled_left = self.left * self.h_scale
        self.scaled_bottom = self.bottom * self.v_scale
        if self.joystick is not None:
            self.controller_input()
    
    def on_draw(self):
        self.batch = pyglet.graphics.Batch()
        glClearColor(255,255,255,255)
        self.clear()

        self.draw_axis()

        for circle in self.plane.circles:
            circle.draw()

        for line in self.plane.lines:
            line.draw()

        self.batch.draw()

    #-----------------------------------Control Functions-----------------------------------#

    def zoomIn(self,x,y):
        self.h_zoom *= self.zoom_ratio
        self.v_zoom *= self.zoom_ratio
        self.offset[0] = (x - (x - self.offset[0]) * self.zoom_ratio)
        self.offset[1] = (y - (y - self.offset[1]) * self.zoom_ratio)

    def zoomOut(self,x,y):
        self.h_zoom /= self.zoom_ratio
        self.v_zoom /= self.zoom_ratio
        self.offset[0] = (x - (x - self.offset[0])/self.zoom_ratio)
        self.offset[1] = (y - (y - self.offset[1])/self.zoom_ratio)

    def transformX(self,pixel = None,point = None):
        if pixel is not None:
            return (pixel + self.scaled_left - self.offset[0])/self.h_scale
        elif point is not None:
            return point * self.h_scale - self.scaled_left + self.offset[0]

    def transformY(self,pixel = None,point = None):
        if pixel is not None:
            return (pixel + self.scaled_bottom - self.offset[1])/self.v_scale
        elif point is not None:
            return point * self.v_scale - self.scaled_bottom + self.offset[1]

    #-----------------------------------Input Functions-----------------------------------#
   
    def controller_input(self):
        # Left Stick
        x = self.joystick.x * self.joystickSensitivity
        y = self.joystick.y * self.joystickSensitivity
        if -0.12 < self.joystick.x < 0.12:
            x = 0
        if -0.12 < self.joystick.y < 0.12:
            y = 0
        z = round(self.joystick.z,1)

        if (not x == 0):
            self.offset[0] -= x
        if (not y == 0):
            self.offset[1] += y

        # Button presses
        i = 0
        while (i < len(self.joystick.buttons)):
            button = self.joystick.buttons[i]
            if button:
                print(i)
            i += 1

        # Triggers
        if (z > 0):
            self.zoomOut(self.width/2,self.height/2)
        elif (z < 0):
            self.zoomIn(self.width/2,self.height/2)

    def on_mouse_scroll(self,x, y, scroll_x, scroll_y):
        if scroll_y > 0:  # left
            # Move to centre of screen
            for _ in range(int(scroll_y)):
                if (self.keys[key.LCTRL] or self.keys[key.RCTRL]):
                    self.h_zoom *= self.zoom_ratio
                elif (self.keys[key.LALT] or self.keys[key.RALT]):
                    self.v_zoom *= self.zoom_ratio
                else:
                    self.zoomIn(x,y)
        elif (scroll_y < 0):
            # Move to centre of screen
            for _ in range(int(scroll_y * -1)):
                if (self.keys[key.LCTRL] or self.keys[key.RCTRL]):
                    self.h_zoom /= self.zoom_ratio
                elif (self.keys[key.LALT] or self.keys[key.RALT]):
                    self.v_zoom /= self.zoom_ratio
                else:
                    self.zoomOut(x,y)

    def on_mouse_motion(self,x, y, dx, dy):
        self._mouse_x = x
        self._mouse_y = y

    def on_mouse_drag(self,x,y,dx,dy,buttons,modifiers):
        if (buttons == 1):
            cursor = self.get_system_mouse_cursor(self.CURSOR_SIZE)
            self.set_mouse_cursor(cursor)
            self.offset[0] += dx
            self.offset[1] += dy

    def on_mouse_release(self,x, y, button, modifiers):
        if (button == 1):
            cursor = self.get_system_mouse_cursor(self.CURSOR_DEFAULT)
            self.set_mouse_cursor(cursor)

    def on_mouse_press(self,x, y, button, modifiers):
        graphX = self.transformX(pixel = x)
        if (button == 2): # Left Click
            for circle in self.plane.circles:
                graphY = circle.getY(graphX)
                circle.addSignificantPoint([graphX,graphY])

            for line in self.plane.lines:
                graphY = line.getY(graphX)
                line.addSignificantPoint([graphX,graphY])
        elif (button == 4): # Right Click
            for circle in self.plane.circles:
                circle.clearSignificantPoints()

            for line in self.plane.lines:
                line.clearSignificantPoints()


    #----------------------------Long functions----------------------------#

    def draw_axis(self):
        # x-axis
        self.batch.add(2, pyglet.gl.GL_LINES, None, 
            ('v2f', (0, self.offset[1] - self.scaled_bottom, self.width, self.offset[1] - self.scaled_bottom)),
            ('c3B', (0, 0, 0, 0, 0, 0))
        )

        # y-axis
        self.batch.add(2, pyglet.gl.GL_LINES, None, 
            ('v2f', (self.offset[0] - self.scaled_left, 0, self.offset[0] - self.scaled_left, self.height)),
            ('c3B', (0, 0, 0, 0, 0, 0))
        )
        

        # draw axis steps
        left_x_pixel = 0
        right_x_pixel = self.width
        bottom_y_pixel = 0
        top_y_pixel = self.height
        origin = [0,0]
        origin_pixel = [self.transformX(point = origin[0]),self.transformY(point = origin[0])]

        step_x_max = self.width / self.axes_step
        step_y_max = self.height / self.axes_step

        step_x_pixel = self.h_zoom * 50
        step_x_pixel = step_x_max if step_x_pixel < step_x_max else step_x_pixel
        
        step_y_pixel = self.v_zoom * 50
        step_y_pixel = step_y_max if step_y_pixel < step_y_max else step_y_pixel

        lineLength = 10

        x = origin_pixel[0]
        while (x < right_x_pixel):
            # get the graph point
            y = self.offset[1] - self.scaled_bottom
            graphX = self.transformX(pixel = x)
            # draw it
            #shapes.Line(x,y - lineLength,x,y+lineLength,color = (255,255,255), batch = self.batch).draw()
            self.plane.graphWindow.batch.add(2, pyglet.gl.GL_LINES, None, 
                ('v2f', (x, y - lineLength, x, y+lineLength)),
                ('c3B', (0, 0, 0, 0, 0, 0))
            )
            pyglet.text.Label("{}".format(round(graphX,2)),
                                        font_name='Times New Roman',
                                        font_size=10,
                                        x=x, y=y,
                                        color=(0, 0, 0, 255),
                                        batch = self.plane.graphWindow.batch)
            # add the horizonal step value
            x += step_x_pixel
        x = origin_pixel[0]
        while (x > left_x_pixel):
            # get the graph point
            y = self.offset[1] - self.scaled_bottom
            graphX = self.transformX(pixel = x)
            # draw it
            #shapes.Line(x,y - lineLength,x,y+lineLength,color = (255,255,255), batch = self.batch).draw()
            self.plane.graphWindow.batch.add(2, pyglet.gl.GL_LINES, None, 
                ('v2f', (x, y - lineLength, x, y+lineLength)),
                ('c3B', (0, 0, 0, 0, 0, 0))
            )
            pyglet.text.Label("{}".format(round(graphX,2)),
                                        font_name='Times New Roman',
                                        font_size=10,
                                        x=x, y=y,
                                        color=(0, 0, 0, 255),
                                        batch = self.plane.graphWindow.batch)
            # add the horizonal step value
            x -= step_x_pixel

        y = origin_pixel[1]
        while (y < top_y_pixel):
            # get the graph point
            x = self.offset[0] - self.scaled_left
            graphY = self.transformY(pixel = y)
            # draw it
            #shapes.Line(x - lineLength,y,x + lineLength,y,color = (255,255,255), batch = self.batch).draw()
            self.plane.graphWindow.batch.add(2, pyglet.gl.GL_LINES, None, 
                ('v2f', (x - lineLength, y, x + lineLength, y)),
                ('c3B', (0, 0, 0, 0, 0, 0))
            )
            pyglet.text.Label("{}".format(round(graphY,2)),
                                        font_name='Times New Roman',
                                        font_size=10,
                                        x=x, y=y,
                                        color=(0, 0, 0, 255),
                                        batch = self.plane.graphWindow.batch)
            # add the horizonal step value
            y += step_y_pixel
        y = origin_pixel[1]
        while (y > bottom_y_pixel):
            # get the graph point
            x = self.offset[0] - self.scaled_left
            graphY = self.transformY(pixel = y)
            # draw it
            #shapes.Line(x - lineLength,y,x + lineLength,y,color = (255,255,255), batch = self.batch).draw()
            self.plane.graphWindow.batch.add(2, pyglet.gl.GL_LINES, None, 
                ('v2f', (x - lineLength, y, x + lineLength, y)),
                ('c3B', (0, 0, 0, 0, 0, 0))
            )
            pyglet.text.Label("{}".format(round(graphY,2)),
                                        font_name='Times New Roman',
                                        font_size=10,
                                        x=x, y=y,
                                        color=(0, 0, 0, 255),
                                        batch = self.plane.graphWindow.batch)
            # add the horizonal step value
            y -= step_y_pixel