import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.optimize import brentq

debug = 0

class stewart:
    def __init__(self, L_1, L_2, L_3, gamma, p_1, p_2, p_3, x_1, x_2, y_2):
        #All given values and initializing some needed derived values    
        self.L_1 = L_1
        self.L_2 = L_2
        self.L_3 = L_3
        self.gamma =  gamma
        self.p_1 = p_1
        self.p_2 = p_2
        self.p_3 = p_3    
        self.p_1_2 = math.pow(p_1, 2)
        self.p_2_2 = math.pow(p_2, 2)
        self.p_3_2 = math.pow(p_3, 2)    
        self.x_1 = x_1
        self.x_2 = x_2
        self.y_2 = y_2
    
    def function_theta(self, theta):
        #Do the equations as given from the book
        A2 = self.L_3 * np.cos(theta) - self.x_1
        B2 = self.L_3 * np.sin(theta)       
        
        A3 = self.L_2 * np.cos(theta + self.gamma) - self.x_2
        B3 = self.L_2 * np.sin(theta + self.gamma) - self.y_2
        
        #so the functions are cleaner
        B2_2 = B2 * B2
        B3_2 = B3 * B3
        A2_2 = A2 * A2
        A3_2 = A3 * A3       

        N1 = B3*(self.p_2_2 - self.p_1_2 - A2_2 - B2_2) - B2*(self.p_3_2 - self.p_1_2 - A3_2 - B3_2)
        N2 = (-1*A3*(self.p_2_2 - self.p_1_2 - A2_2 - B2_2)) + (A2*(self.p_3_2 - self.p_1_2 - A3_2 - B3_2))
        D = 2*((A2*B3)-(B2*A3))
        
        #used in graphing
        self.x = N1 / D
        self.y = N2 / D
        
        N1_2 = N1*N1
        N2_2 = N2*N2
        D_2 = D*D
        
        f = N1_2 + N2_2 - (self.p_1_2 * D_2) 
        return f
    
    def plot_theta(self, theta_min, theta_max, title):
        theta = np.linspace(theta_min, theta_max, 100)
        f_theta = self.function_theta(theta)
        
        #Plot
        figure = plt.figure()
        figure.canvas.set_window_title(title)
        line = plt.plot(theta, f_theta)        
        plt.show()

    def plot_pose_at(self, theta, title):
        self.function_theta(theta)
        
        #Points needed to graph everything
        u1 = self.x + self.L_2 * np.cos(theta+self.gamma)
        v1 = self.y + self.L_2 * np.sin(theta+self.gamma)
        
        u2 = self.x + self.L_3 * np.cos(theta)
        v2 = self.y + self.L_3 * np.sin(theta)
        
        #Plot
        figure = plt.figure()
        figure.canvas.set_window_title(title)
        
        #Cleaner axes sizes by limiting to the max of y and x of p3 and p2 respectively
        xmax = math.ceil(self.x_1)
        ymax = math.ceil(self.y_2)
        xmin = 0
        ymin = 0 
        if (self.x_2 < xmin):
            xmin = self.x_2
        if (self.x < xmin):
            xmin = self.x
        if (u1 < xmin):
            xmin = u1
        
        
        if (u2 > xmax):
            xmax = math.ceil(u2)
        if (v2 > ymax):
            ymax = math.ceil(v2)
        if (u1 > xmax):
            xmax = math.ceil(u1)
        if (v1 > ymax):
            ymax = math.ceil(v1)
        if (self.y_2 > ymax):
            ymax = self.y_2
        
        axes = plt.axes(xlim=(xmin, xmax), ylim=(ymin, ymax))
        
        #1st set is x coords, 2nd set is y coords
        #set of struts for stalwart platform
        strut1 = plt.Line2D( (0, self.x), (0, self.y), lw=2)  
        strut2 = plt.Line2D( (u2, self.x_1),  ( v2, 0), lw=2)  
        strut3 = plt.Line2D( (self.x_2, u1), (self.y_2, v1), lw=2)        
        
        #Add strut1-3 to the graph
        axes.add_artist(strut1)
        axes.add_artist(strut2)
        axes.add_artist(strut3)
        
        #Stalwart platform        
        triangle = plt.Polygon([[self.x, self.y], [u1, v1], [u2, v2]], fill=None, edgecolor='y', lw=3)
        
        #add the platform
        axes.add_artist(triangle)    
        
        #Show the plot        
        plt.show()
        
        if debug == 1:
            print " x,  y\t", self.x, self.y
            print "u1, v1\t", u1, v1
            print "u2, v2\t", u2, v2
        
        
    def root_and_pose(self, title):
        #Stated in book that all solutions are from -pi to pi
        theta = np.linspace( (-1*math.pi), (math.pi), 2000)
        current = self.function_theta(theta)
        sign = np.sign(current)

        roots = []        
        
        #Used the below to be able to iterate through the range of values to get all roots
        #Brentq can't be used in general because the start of interval and end of interval 
        #could be both be positive
        #http://stackoverflow.com/questions/14878110/how-to-find-all-zeros-of-a-function-using-numpy-and-scipy
        for i in range(1999):
            if sign[i] + sign[i+1] == 0:
                cur_theta = brentq(self.function_theta, theta[i], theta[i+1])
                check = self.function_theta(cur_theta)
                if np.isnan(check) or abs(check) > .0001:
                    continue
                roots.append(cur_theta)
        
        if debug == 2:
            print roots
            print len(roots)
        
        for j, value in enumerate(roots):
            cur_root = value
            if debug == 2:
                print cur_root
            self.plot_pose_at(cur_root, title)
        
        
    def root_count(self):
        theta = np.linspace( (-1*math.pi), (math.pi), 2000)
        current = self.function_theta(theta)
        sign = np.sign(current)

        roots = []        
        
        #Used the below to be able to iterate through the range of values to get all roots
        #Brentq can't be used in general because the start of interval and end of interval 
        #could be both be positive
        #http://stackoverflow.com/questions/14878110/how-to-find-all-zeros-of-a-function-using-numpy-and-scipy
        for i in range(1999):
            if sign[i] + sign[i+1] == 0:
                cur_theta = brentq(self.function_theta, theta[i], theta[i+1])
                check = self.function_theta(cur_theta)
                if np.isnan(check) or abs(check) > .0001:
                    continue
                roots.append(cur_theta)
        
        return len(roots)
        
    def set_p_2(self, p2):
        self.p_2 = p2
        self.p_2_2 = p2*p2
        