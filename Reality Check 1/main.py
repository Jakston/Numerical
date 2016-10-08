from function_theta import stewart
import math
import numpy as np
from scipy.optimize import fsolve

#init the stalwart object with the following
part1 = stewart(2, math.sqrt(2), math.sqrt(2), (math.pi/2), math.sqrt(5),
                    math.sqrt(5), math.sqrt(5), 4, 0, 4)

#Plot for #2
part1.plot_theta( (-1*math.pi/4), (math.pi/4), "2. Plot of f(theta) from -pi/4 to pi/4")

#Plots for #3
part1.plot_pose_at(-1*math.pi/4, "3. Reproduce Figure 1.15(a)")
part1.plot_pose_at(math.pi/4, "3. Reproduce Figure 1.15(b)")

#Plots for #4
#Setup a new stewart platform
                #L1, L2, L3, Gamma, P1, P2, P3, X1, X2, Y2
prob4 = stewart(3, (3*math.sqrt(2)) , 3, (math.pi/4), 5, 5, 3, 5, 0, 6)
prob4.plot_theta( (-1*math.pi), (math.pi), "4. Plot of f(theta) from -pi to pi")
prob4.root_and_pose("4.")

#Plots for #5
prob5 = stewart(3, (3*math.sqrt(2)) , 3, (math.pi/4), 5, 7, 3, 5, 0, 6)
prob5.plot_theta( (-1*math.pi), (math.pi), "5. Plot of f(theta) from -pi to pi")
prob5.root_and_pose("5.")

#Plots for #6
prob6 = stewart(3, (3*math.sqrt(2)) , 3, (math.pi/4), 5, 9, 3, 5, 0, 6)
prob6.plot_theta( (-1*math.pi), (math.pi), "6. Plot of f(theta) from -pi to pi")
prob6.root_and_pose("6. p2 = 9")

#Number 7
#get ranges for 0, 2, 4, and 6 poses
#set up the stewart object being used
prob7 = stewart(3, (3*math.sqrt(2)), 3, (math.pi/4), 5, 0, 3, 5, 0, 6)

#dirty root comparison checker for 7
prev_count = 0
value_range_s = 0
value_range_e = 0
for i in range(0, 10):
    prob7.set_p_2(i)
    count = prob7.root_count()
    value_range_e = i
    if count != prev_count:
        print "The range for", prev_count, "poses is from p2 =",value_range_s, "to p2 =",value_range_e
        prev_count = count
        value_range_s = i
    







