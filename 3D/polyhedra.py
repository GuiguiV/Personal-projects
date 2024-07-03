from geometry import Point2D,Point3D,Projection,Polygon

class Cube:
    def __init__(self, p1:Point3D, p2:Point3D):
        p1x = Point3D(p1.pos)
        p1x.pos[0] = p2.pos[0]
        p1y = Point3D(p1.pos)
        p1y.pos[1] = p2.pos[1]
        p1z = Point3D(p1.pos)
        p1z.pos[2] = p2.pos[2]

        p1xy = Point3D(p2.pos)
        p1xy.pos[2] = p1.pos[2]
        p1yz = Point3D(p2.pos)
        p1yz.pos[0] = p1.pos[0]
        p1zx = Point3D(p2.pos)
        p1zx.pos[1] = p1.pos[1]

        lp1 = [p1x,p1y,p1z]
        lp2 = [p1yz,p1zx,p1xy]
        print(f"{lp1=}{lp2=}")
        
        self.sides = []
        for i in range(3):
            j,k = (i+1)%3,(i+2)%3
            side1 = Polygon([p1,lp1[j],lp2[i],lp1[k]])
            self.sides.append(side1)
            side2 = Polygon([p2,lp2[j],lp1[i],lp2[k]])
            self.sides.append(side2)
