import rospy
from std_msgs.msg import String
from gazebo_msgs.msg import ModelState


def move():
    
    pub = rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=10)
    rospy.init_node('camera_control', anonymous=True)
    
    #camera_msg.position: { 1, 0, 2 }, orientation: {x: 0, y: 0.491983115673, z: 0.5, w: 0.870604813099 } }
    #twist = { x: 0, y: 0, z: 0 }
    
    
    camera_msg = ModelState()
    camera_msg.model_name = 'kinect_ros'
    camera_msg.pose.position.x = 1.0
    camera_msg.pose.position.y = 1.0
    camera_msg.pose.position.z = 0.5
    camera_msg.pose.orientation.x = 0.0
    camera_msg.pose.orientation.y = 0.0
    camera_msg.pose.orientation.z = 0.0
    camera_msg.pose.orientation.W = 0.0
    
    camera_msg.twist.linear.x = 0.0
    camera_msg.twist.linear.y = 0.0
    camera_msg.twist.linear.z = 0.0
    camera_msg.twist.angular.x = 0.0
    camera_msg.twist.angular.y = 0.0
    camera_msg.twist.angular.z = 0.0

    camera_msg.reference_frame = 'world'
    #rospy.loginfo(camera_msg)
    #pub.publish(camera_msg)
    # see ros message attributes
    print(dir(camera_msg.pose.orientation))
    #camera_msg.pose.position= [1, 0, 3]
    #print(type(camera_msg.pose.position))



    rate = rospy.Rate(10)
    #while not rospy.is_shutdown():
    for i in range(10):
        rospy.loginfo(camera_msg)
        pub.publish(camera_msg)
        rate.sleep()


def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException:
        pass
