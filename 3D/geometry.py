import numpy as np
from repr_mixin import ReprMixin

class Triangle(ReprMixin):
    def __init__(self,points):
        self.points = points

    def get_lines(self):
        l = []
        l.append(self.points[0])

class Point3D(ReprMixin):
    def __init__(self,pos:np.array):
        """Point in a projective 3D space

        Args:
            pos (np.array): Homogeneous coordinates in 3D
        """
        self.pos = np.array(pos)

class Point2D(Point3D):
    def __init__(self,pos:np.array):
        """Point in a projective 2D space

        Args:
            pos (np.array): Homogeneous coordinates in 2D
        """
        self.pos = np.array(pos)

    def get_line(self,other_point:"Point2D"):
        if isinstance(other_point,Point2D):
            return np.cross(self.pos, other_point.pos)
        elif isinstance(other_point,np.array) and other_point.shape == (3,1):
            return np.cross(self.pos, other_point)
        else :
            raise TypeError("Cannot find a line with this type")
        
class Polygon(ReprMixin):
    def __init__(self,points):
        self.points = points
    
    def get_plottable(self,projection):
        poly_2D = []

        for p in self.points:
            poly_2D.append(projection.project(p))
        
        x = []
        y = []
        
        for p2 in poly_2D:
            if p2.pos[2] != 0:
                xx,yy = p2.pos[:2]/p2.pos[2]
                x.append(xx)
                y.append(yy)
        x.append(x[0])
        y.append(y[0])

        return x,y

        
class Projection(ReprMixin):
    def __init__(self,matrix=None,**kwargs):
        if matrix is None:
            self._build_matrix(**kwargs)
        elif isinstance(matrix,np.array) and matrix.shape == (3,4):
            self.matrix = matrix

        else :
            raise TypeError("Invalid matrix provided")
    
    def _build_matrix(self,
                      opt_center=None,
                      f=2,
                      rotation=None,
                      translation=None,
                      orthographic=False):

        """
        Build projection matrix from parameters
        """
        if opt_center is None:
            opt_center = np.zeros(2)
        if rotation is None:
            rotation = np.eye(3)
        if translation is None:
            translation = np.zeros(3)
        
        rot_trans= np.zeros((3,4))
        rot_trans[:,:3] = rotation
        rot_trans[:,3] = translation


        K = np.eye(3)
        K[0,0],K[1,1] = f,f
        K[:2,2] = opt_center

        self.matrix = K@rot_trans

        if orthographic:
            # no influence of z coordinate
            self.matrix[:,2] = 0
            # keep same w in the projection
            self.matrix[2,3] = 1

    def rotate(self,new_rotation_matrix):
        rotator = np.eye(4)
        rotator[:3,:3] = new_rotation_matrix
        self.matrix = self.matrix @ rotator

    def project(self,point_3d:Point3D) -> Point2D:
        return Point2D(self.matrix@point_3d.pos)

