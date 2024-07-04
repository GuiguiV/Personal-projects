import matplotlib.pyplot as plt
import numpy as np
from geometry import Point2D,Point3D,Projection,Polygon
import matplotlib.animation as animation
# poly = Polygon([Point3D(np.array([1,2,1,1])),
#             Point3D(np.array([0,2,1,1])),
#             Point3D(np.array([0,2,2,1])),
#             Point3D(np.array([1,2,2,1])),
#             ])

# poly2 = Polygon([Point3D(np.array([2,1,1,1])),
#             Point3D(np.array([2,1,3,1])),
#             Point3D(np.array([2,2,3,1])),
#             Point3D(np.array([2,2,1,1])),
#             ])
from polyhedra import Cube
c = Cube(Point3D(np.array([-1.,1,3,1])),Point3D(np.array([2.,2,4,1])))
print(c.sides)
proj = Projection()
xmin,xmax = -2,2
ymin,ymax =  -2,2
from  scipy.spatial.transform import Rotation as R

intrinsic_rotc = R.from_quat([ 1*np.sin(np.pi/100),0.5*np.sin(np.pi/100),0, np.cos(np.pi/100)])
fig = plt.figure()
def update(num, proj):
    theta = np.pi*num/30
    rot = R.from_quat([0, 0, 1*np.sin(theta/2), np.cos(theta/2)]).as_matrix()
    proj= Projection(translation=num*1e-1*np.array([0.1,0.1,0.1]),rotation=rot)
    plt.clf()
    ls= []
    c.rotate(intrinsic_rotc)
    for s in c.sides:
        ls.append(plt.plot(*s.get_plottable(proj),color="r"))
        ax = plt.gca()
        ax.set_xlim([xmin, xmax])  
        ax.set_ylim([ymin, ymax])

    return ls


ani = animation.FuncAnimation(fig, update, 60, interval=100, 
                              fargs=[proj])
plt.show()