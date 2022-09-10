#!/usr/bin/env python
# coding=utf-8
import rospy
import numpy as np
import random as rdm
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

#Creamos la clase
class MoveArUco():
    def __init__(self):
        #Inicializamos el nodo
        rospy.init_node("goToPoint")
        #Creamos el publisher
        self.pub = rospy.Publisher("turtle1/cmd_vel", Twist, queue_size=1)        
        
        self.subPose = rospy.Subscriber("turtle1/pose",Pose,self.pose_callback)

        #Declaramos que vamos a mandar 20 mensajes por segundo.
        self.rate = rospy.Rate(20)
        self.msg = Twist()

        self.current_pose = None
               
        self.target = [round(rdm.uniform(0.1,10),2),round(rdm.uniform(0.1,10),2)]
        print("Target: ", self.target)
    
        
        self.state = "pointingTowardsGoal"
        #Creamos un función de que hacer cuando haya un shutdown
        rospy.on_shutdown(self.end_callback)


    def pose_callback(self, pose):
        self.current_pose = pose

    def move(self,v_lin,v_ang):
        """Funcion que publica la velocidad lineal y angular en el Rover"""
        #Declaramos le velocidad deseada en el mensaje tipo Twist
        self.msg.linear.x = v_lin        
        self.msg.angular.z = v_ang
        #Publicamos la velocidad
        self.pub.publish(self.msg)

    def create_reference_points(self):
        return [[self.current_pose.x+0.1,self.current_pose.y],
                [self.current_pose.x-0.1,self.current_pose.y],
                [self.current_pose.x,self.current_pose.y+0.1],
                [self.current_pose.x,self.current_pose.y-0.1],
                [self.current_pose.x+0.1,self.current_pose.y+0.1],
                [self.current_pose.x+0.1,self.current_pose.y-0.1],
                [self.current_pose.x-0.1,self.current_pose.y+0.1],
                [self.current_pose.x-0.1,self.current_pose.y-0.1]]

    def end_callback(self):
        """Funcion que para el Rover cuando el nodo deja de ser corrido"""
        #Declaramos las velocidades de cero
        self.msg.linear.x = 0.0
        self.msg.angular.z = 0.0
        #Publicamos las velocidades
        self.pub.publish(self.msg)


#Si el archivo es corrido directametne y no llamado desde otro archivo corremos
if __name__ == "__main__":
    #iniciamos la clase
    mov = MoveArUco()
    
    Kpw = 2.0
    Kpv = 0.5
    while not rospy.is_shutdown():

        if mov.current_pose != None:

            theta_target = np.arctan2(mov.target[1]-mov.current_pose.y, mov.target[0]-mov.current_pose.x)
            e_theta = theta_target - mov.current_pose.theta
            e_pos = np.sqrt((mov.target[0]-mov.current_pose.x)**2 + (mov.target[1]-mov.current_pose.y)**2)
                
            if mov.state == "pointingTowardsGoal":                    
                w = Kpw*e_theta
                v = 0.0
              
                mov.move(v,w)

            if mov.state == "travelingTowardsGoal":
                w = Kpw*0.25*e_theta
 
                v = Kpv*e_pos               
                    
            mov.move(v,w)
            print("Turle at:", mov.current_pose.x,mov.current_pose.y, "Target is: ", mov.target)
            
            if (abs(e_theta) <= 0.025) and mov.state == "pointingTowardsGoal":                    
                mov.state = "travelingTowardsGoal"
                        
            if ( abs(e_pos) <= 0.025 and mov.state == "travelingTowardsGoal"):                    
                mov.move(0.0,0.0)
                print("Arrived to", mov.target, ", approximately at: ",mov.current_pose.x,mov.current_pose.y)
                mov.state = "goalReached"
                    
            if mov.state == "goalReached":
                mov.end_callback()
                reference_points = mov.create_reference_points()
                print("Close points of the goal:",reference_points)
                break                                              
        mov.rate.sleep()

        
