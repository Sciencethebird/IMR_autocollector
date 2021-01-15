import rospy
from std_msgs.msg import String
from gazebo_msgs.msg import ModelState
import numpy as np
import math
import random

class ROSCamera():
    def __init__(self, camera_name = 'kinect_ros', node_name = 'camera_control'):
        self.pub = rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=10)
        rospy.init_node(node_name, anonymous=True)

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

    def pub_message(self):
        rate = rospy.Rate(10)
        rospy.loginfo(self.camera_msg)
        for i in range(10):
            self.pub.publish(self.camera_msg)
            rate.sleep()



if __name__ == '__main__':
    try:
        test = ROSCamera()
        randx = random.uniform(-1.0, 1.0)
        randy = random.uniform(-1.0, 1.0)
        randz = random.uniform(1.5, 1.8)
        test.move_to(randx, randy, randz)
        print(randx, randy, randz)
        test.point_camera_at(-0.05, -0.15, 1.01, 1.0)
    except rospy.ROSInterruptException:
        pass
