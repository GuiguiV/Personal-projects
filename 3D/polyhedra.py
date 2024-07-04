from geometry import Point2D,Point3D,Projection,Polygon
from  scipy.spatial.transform import Rotation

class Cube:
    def __init__(self, p1:Point3D, p2:Point3D):
        self.p1 = p1
        self.p2 = p2
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

        self.lp1 = [p1x,p1y,p1z]
        self.lp2 = [p1yz,p1zx,p1xy]

        self._make_sides()

    def _make_sides(self):
        p1,p2 = self.p1,self.p2
        lp1,lp2 = self.lp1,self.lp2

        self.sides = []
        for i in range(3):
            j,k = (i+1)%3,(i+2)%3
            side1 = Polygon([p1,lp1[j],lp2[i],lp1[k]])
            self.sides.append(side1)
            side2 = Polygon([p2,lp2[j],lp1[i],lp2[k]])
            self.sides.append(side2)

    def rotate(self,r:Rotation):
        baryc = 0.5*(self.p1.pos[:3] + self.p2.pos[:3])
        self.p1.pos[:3] = baryc+ r.apply(self.p1.pos[:3]-baryc)
        self.p2.pos[:3] = baryc + r.apply(self.p2.pos[:3]-baryc)

        for pt in self.lp1:
            pt.pos[:3] = baryc+ r.apply(pt.pos[:3]-baryc)
        for pt in self.lp2:
            pt.pos[:3] = baryc+ r.apply(pt.pos[:3]-baryc)

        self._make_sides()


