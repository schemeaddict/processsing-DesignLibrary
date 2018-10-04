class Dobject:
    def  __init__(self, x = None, y = None, scle = None, obj = None):
        self.Color = color(255,255,255)
        self.radius = 1
        self.Rotation = 0
        self.contains = []
        if x is None:
            self.x = 0
        else:
            self.x = x
        if y is None:
            self.y = 0
        else:
            self.y = y
        if scle is None:
            self.Scale = 1
        else:
            self.Scale = scle
        if obj is not None:
            if type(obj) is list:
                for original in obj:
                    self.add(original.copy())
            else :
                self.add(obj.copy())
    def copy(self):
        obj = Dobject(self.x,self.y,self.Scale,self.contains)
        obj.position(self.Rotation)
        obj.radius = self.radius
        return obj
    def reShape(self, points, radius = None):
        self.sides = points
        self.angle  = 2*PI/points
        if radius is not None:
            self.radius = radius
        else:
            self.radius = self.radius
        # points for half the triangle
        self.ops = self.radius*sin(self.angle/2)
        self.adj = self.radius*cos(self.angle/2)
        self.generate()
    def generate(self):
        obj = self.contains[0].copy()
        self.empty()
        obj.position(0,0)
        self.add(obj.copy())
        self.contains[0].position(0,0)
        for temp in range(0,self.sides):
            obj.position(temp*self.angle)
            obj.position(self.radius*cos(temp*self.angle-PI/2),self.radius*sin(temp*self.angle-PI/2))
            self.add( obj.copy())
    def changeColor(color):
        self.Color = color
    def add(self,obj):
        if type(obj) is list:
            self.contains = self.contains + obj
        else:
                self.contains.append(obj)
    def reSize(self,scle):
        self.Scale=scle*self.Scale
    def resetSize(self):
            self.Scale=1
    def position(self,x,y=None):
        if y is not None:
            self.x = x
            self.y = y
        else:
            self.Rotation = x
    def move(self,x,y):
        self.x = x + self.x
        self.y = y + self.y
    #handle the position and size of the the objects being drawn by draws
    def draw(self,X=None,Y=None,Scale=None):
            if X is not None:
                if Scale is None:
                    pushMatrix()
                    translate(X,Y)
                    rotate(self.Rotation)
                    scale(self.Scale)
                    self.draws()
                    popMatrix()
                else:
                    pushMatrix()
                    translate(X,Y)
                    rotate(self.Rotation)
                    scale(Scale)
                    self.draws()
                    popMatrix()
            else:
                pushMatrix()
                translate(self.x,self.y)
                rotate(self.Rotation)
                scale(self.Scale)
                self.draws()
                popMatrix()
    def empty(self):
        self.contains=[]

# draws will be over written by child to draw its specific drawing
    # draw all the objects this object contains if not overwriten by child
    def draws(self,X=None,Y=None,Scale=None):
        #print(self)
        #print('draw')
        #print(len(self.contains))
        for obj in self.contains:
            obj.draw()
class Triangle(Dobject):
    def __init__(self, x1 , y1, x2, y2, x3, y3):
        Dobject.__init__(self,-(x1+x2+x3)/3,-(y1+y2+y3)/3,1)
        self.point = [[x1,y1],[x2,y2],[x3,y3]]
    def copy(self):
        tri = Triangle(self.point[0][0], self.point[0][1], self.point[1][0],self.point[1][1],self.point[2][0],self.point[2][1])
        tri.x = self.x
        tri.y = self.y
        tri.Rotation = self.Rotation
        return tri
    def centerPoint(self, x1 = None,  x2 = None, x3 = None):
        return (x1+x2+x3)/3
    def draws(self,X=None,Y=None,Scale=None):
        triangle(self.point[0][0], self.point[0][1], self.point[1][0],self.point[1][1],self.point[2][0],self.point[2][1])
class Diamond(Dobject):
    def __init__(self, x = None, y = None, hgt = None, wdth = None, scle = None):
        Dobject.__init__(self,x,y,scle)
        if hgt is None:
            self.hgt  = 1
        else:
            self.hgt = hgt
        if wdth is None:
            self.wdth = 1
        else:
            self.wdth = wdth
    def draws(self,X=None,Y=None,Scale=None):
        quad(-(self.wdth/2), 0 , 0, (self.hgt/2), (self.wdth/2), 0, 0, -(self.hgt/2))
class Polygon(Dobject):
    def __init__(self, sides = None , radius = None , x = None, y = None, scle = None):
        #shift
        Dobject.__init__(self,x,y,scle)
        if radius is not None:
            self.radius = radius
        if sides is None:
            self.sides = 3
        else:
            self.sides =sides
        # angle to rotate triangles for specified polygon
        self.shift = 0
        self.reShape(self.sides,self.radius)
    def copy(self):
        obj = Polygon(self.sides,self.radius,self.x,self.y,self.Scale)
        obj.position(self.Rotation)
        obj.radius = self.radius
        return obj
    # generate and add triangle objects to this polygons
    def generate(self):
        self.empty()
        for tri in range(0,self.sides):
            tempTri = Triangle(0, 0, self.adj, self.ops, self.adj, -self.ops)
            tempTri.position(0,0)
            tempTri.position(tri*self.angle+PI/2)
            self.add(tempTri)
