import numpy as np
import math
import time

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def puck_movement(circleposition):
    l = [[1,1],[1,1],[1,1]]
    for circle in circleposition():
        time1 = time.clock()
        l.append(circle)
        l=l[1:]
        
        u=[l[2][0]-l[1][0],l[2][1]-l[1][1]]
        v=[l[1][0]-l[0][0],l[1][1]-l[0][1]]
        #print "vector u:",u
        #print "vector v:",v
        a= angle_between(u,v)
        #if not math.isnan(a):
        #    print "######## angle:",a
        
        if a > 0.5*np.pi and a < 1.5*np.pi:
            dirchange= True
        else:    
            dirchange = False
            
        time2 = time.clock()
        print('puck_movement clocktime %0.6f' % (time2-time1))
    
        yield [l,dirchange]
        
