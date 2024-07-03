import matplotlib.pyplot as plt
import numpy as np
from geometry import Point2D,Point3D,Projection,Polygon

poly = Polygon([Point3D(np.array([1,2,1,1])),
            Point3D(np.array([0,2,1,1])),
            Point3D(np.array([0,2,2,1])),
            Point3D(np.array([1,2,2,1])),
            ])

poly2 = Polygon([Point3D(np.array([2,1,1,1])),
            Point3D(np.array([2,1,3,1])),
            Point3D(np.array([2,2,3,1])),
            Point3D(np.array([2,2,1,1])),
            ])

proj = Projection()
plt.plot(*poly.get_plottable(proj),color="r")
plt.plot(*poly2.get_plottable(proj))
from  scipy.spatial.transform import Rotation as R
rot = R.from_quat([0, 0, np.sin(np.pi/4), np.cos(np.pi/4)])
proj.rotate(rot.as_matrix())
plt.plot(*poly.get_plottable(proj),color="r")
plt.plot(*poly2.get_plottable(proj))


plt.show()