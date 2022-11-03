import re
from Circle import Circle
from Line import Line
from plane import Plane

#--------------------- GENERAL FUNCTIONS ---------------------#

def getFloat(min = None,max = None,message = None):
    if (message is not None):
        print(message)
    string = input()
    match = re.search("\-?\d*\.?\d*", string)
    if (match):
        value = float(string)
        if min is not None:
            if (value < min):
                print("Number cannot be less than {}".format(min))
                return getFloat(min,max)
        if max is not None:
            if (value > max):
                print("Number cannot exceed {}".format(max))
                return getFloat(min,max)
        return value
    print("Please enter a valid number...")
    return getFloat(min,max,message)

def getBool(message = None):
    if (message is not None):
        print(message)
    string = input()
    match = re.search("([YyNn]|([Yy]es|[Nn]o))",string)
    if (match):
        if re.search("([Yy]|[Yy]es)",string):
            return True
        elif re.search("([Nn]|[Nn]o)",string):
            return False
    else:
        print("Please enter a valid response (yes|no)")
        return getBool(message)

#--------------------- MAIN ---------------------#

def getOrigin():
    print("Is the line being compared with the origin? (yes|no)")
    origin = getBool()
    comp = [0,0]
    if (origin):
        return comp
    else:
        print("Please enter comparison x-value")
        comp[0] = getFloat()
        print("Please enter comparison y-value")
        comp[1] = getFloat()
    return comp

def getAccuracy(circle,minPointsOfAccuracy = 10,maxPointsOfAccuracy = 2000):
    print("How accurate? (% between 0 and 100 inclusive)")
    accuracy = getFloat(min = 0,max = 100) / 100
    step = (circle.getMax() - circle.getMin()) / (minPointsOfAccuracy + (maxPointsOfAccuracy - minPointsOfAccuracy) * accuracy)
    print("step is: {}".format(step))
    pointsOfAccuracy = (circle.getMax() - circle.getMin()) / step
    print("Using {} points of accuracy".format(pointsOfAccuracy))
    return step

def main():
    # Start
    print("Welcome to the W3 Shear Strength of Soil Calculator, let get started shall we?")
    print("DISCLAIMER: This application uses step technique to find gradients.\n")

    # Object inits
    plane = Plane()
    line1 = Line(plane)
    circle1 = Circle(plane)

    # Origin?
    line1.addPoint(getOrigin())
        
    # Semi-Circle Values
    circle1.h = getFloat(message = "Please enter h value:")
    circle1.setR(getFloat(message = "Please enter r value:"))
    print("Min = {}".format(circle1.getMin()))
    print("Max = {}".format(circle1.getMax()))

    if (circle1.getMin() < line1.points[0][0] < circle1.getMax()):
        print("ERROR: comparison point is with the circle")
        return main()

    # Accuracy / Step
    step = getAccuracy(circle1)

    # Gradients
    line1.generateGradients(circle1,step)

    # Final Result
    print("Max Gradient is {}".format(line1.maxGrad))
    print("This forms an angle of {}°".format(line1.getMaxGradAngle()))
    if not line1.getYintercept() == 0:
        print("The rough equation for this tangent line is y = {}x + {}".format(line1.maxGrad,line1.c))
    else:
        print("The rough equation for this tangent line is y = {}x".format(line1.maxGrad))
    
    # Graph
    if (circle1.h < line1.points[0][0]): # Down Slope
        line1.addPoint([circle1.getMin(),line1.getY(circle1.getMin())])
        plane.graph(circle1.getMin(),line1.points[0][0],circle1.r,0)
    elif (circle1.h > line1.points[0][0]): # Up Slope
        line1.addPoint([circle1.getMax(),line1.getY(circle1.getMax())])
        plane.graph(line1.points[0][0],circle1.getMax(),circle1.r,0)

    # Pause - prompt for retry
    print("Would you like to run another calculation? (yes|no)")
    again = getBool()
    if (again):
        return main()
    else:
        return 0

if __name__ == "__main__":
    # execute only if run as a script
    main()
