'''
Created on Sep 19, 2014

@author: James
'''
import request as r
import pdb
import math
import datetime
import fields
import time

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm

import threading

class Team(object):
    def __init__(self, host, port):
        self.timestamp = datetime.datetime.utcnow()
        self.TIMEMULTIPLIER = 2
        r.Request.connect(host, port)
        
        
        self.CONSTANTS = r.Constants().dictionary()
        self.ANGULARACCEL = float(self.CONSTANTS["angularaccel"])
        self.bases = r.Bases()


        world = GridWorld(self.CONSTANTS)
        mytanks = r.Mytanks()



	fig = plt.figure()
        img = plt.imshow(world.world, aspect=None, cmap=cm.YlGnBu, interpolation="none")

        def animate(i):
            mytanks = r.Mytanks()
            for num in range(len(mytanks.list)):
                occgrid = r.Occgrid(num)
                world.update(occgrid.corner(), occgrid.grid())

                #num = 0
                r.Speed(num, 1)
                #pdb.set_trace()
                if mytanks.flag(num) == True:
                    goal = self.bases.center(self.CONSTANTS["team"])
                else:
                    goal = r.Flags().index(3)

                self.steer(mytanks, num, goal)
                #r.Shoot(num)   

            return plt.imshow(world.world, aspect=None, cmap=cm.YlGnBu, interpolation="none")

        ani = animation.FuncAnimation(fig, animate, interval = 20, save_count=0)
        plt.show()



	#print self.CONSTANTS
	#goal = r.Flags().index(1)
	#fields.make_potential_fields(r.Obstacles().get_Obstacles(), int(self.CONSTANTS['worldsize']), r.Flags().index(0), self.generate_field_function(150,goal,r.Obstacles().get_Obstacles()))

#         for item in r.Obstacles().list:
#             print map(float, item[1:])
#         
# 
#          
#         print r.Obstacles().get_Obstacles()
#         pdb.set_trace()   
        
    '''
        while True:
            mytanks = r.Mytanks() 

            
            for num in range(len(mytanks.list)):
                occgrid = r.Occgrid(num)
                world.update(occgrid.corner(), occgrid.grid())

#                 num = 0
                r.Speed(num, 1)
#                 pdb.set_trace()
                if mytanks.flag(num) == True:
                    goal = self.bases.center(self.CONSTANTS["team"])
                else:
                    goal = r.Flags().index(3)

                self.steer(mytanks, num, goal)
                r.Shoot(num)   
    '''
            




    def dumbagent(self, num1, num2):
        mytanks = r.Mytanks()
        desired_angle = 1
        
        for idx in range(len(mytanks.list)):
                r.Speed(idx, 0)
                r.Angvel(idx, 0)
            
        def straight(desired_angle, start):
            r.Speed(num1, 1)
            r.Speed(num2, 1)
            while True:
                mytanks = r.Mytanks()
                angadj = self.angveladj(mytanks.angle(num1), mytanks.angvel(num1), desired_angle) 
                r.Angvel(num1, angadj)
                r.Angvel(num2, angadj)
                end = time.time()
                delta_time = end - start
                if -.1 < delta_time % 2 < .1:
                    r.Shoot(num1)
                    r.Shoot(num2)
                if delta_time > 5:
                    print "got out of straight"
                    return
                
                
        def turn(desired_angle, start):
            r.Speed(num1, 0)
            r.Speed(num2, 0)
            while True:
                mytanks = r.Mytanks()
                angadj = self.angveladj(mytanks.angle(num1), mytanks.angvel(num1), desired_angle) 
                r.Angvel(num1, angadj)
                r.Angvel(num2, angadj)
                end = time.time()
                delta_angle = desired_angle - mytanks.angle(num1)
#                 print "angle"
#                 print desired_angle
#                 print mytanks.angle(num)
                delta_time = end - start
                if -.1 < delta_time % 2 < .1:
                    r.Shoot(num1) 
                    r.Shoot(num2)
                if -.1 < delta_angle < .1:
                    return
            
        while True:
            start = time.time()
            straight(desired_angle, start) 
            desired_angle += 1
            if desired_angle < math.pi:
                desired_angle = desired_angle % math.pi
            else:
                desired_angle = -1 * (desired_angle % math.pi)
            print "desired"
            print desired_angle
            turn(desired_angle, start)


        
    
    def steer(self, mytanks, num, goal):
        desired_angle = self.angle(mytanks.position(num), self.generate_field_function(150, goal))#, r.Obstacles().get_Obstacles()))        
        angadj = self.angveladj(mytanks.angle(num), mytanks.angvel(num), desired_angle)    
        r.Angvel(num, angadj)
        
    def simple_vector(self, agent, goal):
        desired_angle = self.angle(agent, goal)
                

    def distance(self, pos1, pos2):
        return math.sqrt(pow(pos2[0]-pos1[0],2) + pow(pos1[1]-pos2[1],2))
    
    def generate_field_function(self, scale, goal):#, obstacles):
        def function(x, y):
            #print x, y
            vGoalDif = (goal[0]-x,goal[1]-y)
            vGoalAng = math.atan2(vGoalDif[1], vGoalDif[0])
            vGoalDis = (vGoalDif[0]**2 + vGoalDif[1]**2) ** .5
            vGoalMag = 10
            if vGoalDis > 50:
                vGoalMag = 5
            else:
                vGoalMag = (50-vGoalDis)/10
            vGoal = (math.cos(vGoalAng)*vGoalMag,math.sin(vGoalAng)*vGoalMag)
            


	    #User-defined field function.
            #return vGoal[0],vGoal[1]

            vOb = [0,0]
            '''
            for obs in obstacles:
                lines = []
                last_point = obs[0]
                for cur_point in obs[1:]:
                    lines.append((last_point, cur_point))
                    last_point = cur_point
                lines.append((last_point, obs[0]))
                for line in lines:
                    if line[0][0] == line[1][0]:
                        #vertical
                        xpos = line[0][0]
                        ymax = max(line[0][1], line[1][1])
                        ymin = min(line[0][1], line[1][1])
                        if y < ymax and y > ymin:
                            if x < xpos and xpos - x < 50:
                                vOb[0] -= (50 - (xpos-x)) / 100
                                vOb[1] += (50 - (xpos-x)) / 5
                            elif x > xpos and x - xpos < 50:
                                vOb[0] += (50 - (x-xpos)) / 100
                                vOb[1] -= (50 - (x-xpos)) / 5
                    elif line[0][1] == line[1][1]:
                        #horizontal
                        ypos = line[0][1]
                        xmax = max(line[0][0], line[1][0])
                        xmin = min(line[0][0], line[1][0])
                        if x < xmax and x > xmin:
                            if y < ypos and ypos - y < 50:
                                vOb[1] -= (50 - (ypos-y)) / 100
                                vOb[0] -= (50 - (ypos-y)) / 5
                            elif y > ypos and y - ypos < 50:
                                vOb[1] += (50 - (y-ypos)) / 100
                                vOb[0] += (50 - (y-ypos)) / 5
            '''
            return (vGoal[0]+vOb[0])/5, (vGoal[1]+vOb[1])/5
        return function
	

#    def angle(self, agent, goal):
#        return math.atan2(goal[1]-agent[1], goal[0]-agent[0])

    def angle(self, agent, func):
        vx,vy = func(agent[0], agent[1])
        return math.atan2(vy,vx)
   
    def angveladj(self, angle, angvel, desired_angle):
        angle = angle + angvel / self.ANGULARACCEL
	#print desired_angle, angle
        #print angvel
        a = math.atan2(math.sin(desired_angle - angle), math.cos(desired_angle - angle))
        if a > 0:
            return 1
        if a < 0:
            return -1
        return 0
    



class GridWorld(object):
    def __init__(self, CONSTANTS):
        self.worldsize = int(CONSTANTS["worldsize"])
        self.world = [ [ .5 for i in range(self.worldsize) ] for j in range(self.worldsize) ]
#         self.times_updated = [ [ 1 for i in range(worldsize) ] for j in range(worldsize) ]
        
        self.obs_occ = float(CONSTANTS["truepositive"])
        self.Nobs_occ = 1 - self.obs_occ
        self.Nobs_Nocc = float(CONSTANTS["truenegative"])
        self.obs_Nocc = 1 - self.Nobs_Nocc
        
    def update(self, corner, grid):

        
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                x = corner[0] + i + self.worldsize / 2
                y = corner[1] + j + self.worldsize / 2

                if grid[i][j]:
                    self.world[x][y] = self.obs(self.world[x][y])
                else:
                    self.world[x][y] = self.Nobs(self.world[x][y])

    def Nobs(self, prior):
        return (self.Nobs_occ * prior) / (self.Nobs_occ * prior + self.Nobs_Nocc * (1-prior))
    
    def obs(self, prior):
        return (self.obs_occ * prior) / (self.obs_occ * prior + self.obs_Nocc * (1-prior))




import sys
Team("localhost", sys.argv[1])
if __name__ == '__main__':
    pass
