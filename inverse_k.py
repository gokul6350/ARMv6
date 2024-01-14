

import math


def inverse_k2dof(x,y,l1=11,l2=12):


    upper = x**2 + y**2 - l1**2 - l2**2
    lower = 2 * l1 * l2

    try:
        temp = math.acos(upper/lower) 
    except:
        return (False,0,0)
    
    q2 = math.degrees(temp)
    
   
    if x == 0:
        a = 1.57079633 
    else:
        a = math.atan(y/x)
    
    a1 = (l2 * math.sin(math.radians(q2)))
    b1 = l1 + (l2 * math.cos(math.radians(q2)))
    c = math.radians(a1)/math.radians(b1)

    b= math.atan(c)
    q1 = math.degrees(a-b)
    print(f"Angle A {int(q1)} B: {int(q2)}")
    return True,int(q1),int(q2)


