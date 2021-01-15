import rospy
from std_msgs.msg import String
from gazebo_msgs.msg import ModelState
import numpy as np
import math
import random
import time
import argparse


parser = argparse.ArgumentParser(description='move camera by script')

parser.add_argument('--mask', action='store_true',help='mask mode, save only rgb to mask img folder')

args = parser.parse_args()


class ROSCamera():
    def __init__(self, camera_name = 'kinect_ros', node_name = 'camera_control'):
        self.pub = rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=10)
        self.save_trigger = rospy.Publisher('image_save_trigger', String, queue_size=10)
        
        rospy.init_node(node_name, anonymous=True)

        # clear file name index
        self.save_trigger.publish("00")

        self.camera_msg = ModelState()
        self.camera_msg.model_name = camera_name
        self.camera_msg.reference_frame = 'world'
        #static position
        self.camera_msg.pose.position.x = 0.0
        self.camera_msg.pose.position.y = 0.0
        self.camera_msg.pose.position.z = 0.5
        self.camera_msg.pose.orientation.x = 0.0
        self.camera_msg.pose.orientation.y = 0.0
        self.camera_msg.pose.orientation.z = 0.0
        self.camera_msg.pose.orientation.w = 0.0
        # motion
        self.camera_msg.twist.linear.x = 0.0
        self.camera_msg.twist.linear.y = 0.0
        self.camera_msg.twist.linear.z = 0.0
        self.camera_msg.twist.angular.x = 0.0
        self.camera_msg.twist.angular.y = 0.0
        self.camera_msg.twist.angular.z = 0.0

    def move_to(self, x, y, z, i = 0.0, j= 0.0, k= 0.0, w=0.0):
        # x, y, z
        self.camera_msg.pose.position.x = x
        self.camera_msg.pose.position.y = y
        self.camera_msg.pose.position.z = z
        # quaternions
        self.camera_msg.pose.orientation.x = i
        self.camera_msg.pose.orientation.y = j
        self.camera_msg.pose.orientation.z = k
        self.camera_msg.pose.orientation.w = w

        self.pub_message()



    def set_eular_angle(self, roll, pitch, yaw):

        qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
        qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
        qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

        #return [qx, qy, qz, qw]

        self.camera_msg.pose.orientation.x = qx
        self.camera_msg.pose.orientation.y = qy
        self.camera_msg.pose.orientation.z = qz
        self.camera_msg.pose.orientation.w = qw
        self.pub_message()

    def point_camera_at(self, px, py, pz, theta=0.0):
        
        dx = px - self.camera_msg.pose.position.x
        dy = py - self.camera_msg.pose.position.y
        dz = pz - self.camera_msg.pose.position.z

        base = np.sqrt(np.sum(np.square([dx, dy])))

        yaw = np.arctan2(dy,dx)
        pitch = -1.0*np.arctan2(dz,base)

        print('pitch', pitch)
        self.set_eular_angle(0.0, pitch, yaw)
        

    def send_save_signal(self):
        if args.mask:
            self.save_trigger.publish("10")
        else:
            self.save_trigger.publish("11")

    def pub_message(self):
        rate = rospy.Rate(10)
        rospy.loginfo(self.camera_msg)
        for i in range(10):
            self.pub.publish(self.camera_msg)
            rate.sleep()



if __name__ == '__main__':

    f = open('camera_script.txt', 'r')
    lines = f.readlines()
    try:
        cam = ROSCamera()
        for line in lines:
            x, y, z, roll, pitch, yaw = line.split(',')
            cam.move_to(float(x), float(y), float(z))
            cam.set_eular_angle(float(roll), float(pitch), float(yaw))
            #cam.point_camera_at(0.0, 0.0, 1.02, 1.0)
            cam.send_save_signal()
            time.sleep(1)

    except rospy.ROSInterruptException:
        pass
