#!/usr/bin/env python
import rospy, time, sys
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

class Acceleration:

    def __init__(self):
        rospy.Subscriber("odom", Odometry, self.odom_callback)
        self.vel_pub = rospy.Publisher("cmd_vel", Twist, queue_size = 10)

        #Odometry data
        self.linear_speed_x = 0.0
        self.linear_speed_y = 0.0
        self.angular_spped_z = 0.0

    def odom_callback(self, data):
        self.linear_speed_x = data.twist.twist.linear.x
        self.linear_speed_y = data.twist.twist.linear.y
        self.angular_spped_z = data.twist.twist.angular.z

    def get_acceleration(self, axis, max_velocity):
        twist_msg = Twist()
        vel_ref = 0.0

        #get initial time before moving the robot (for accel calculation)
        t0 = rospy.Time.now().to_sec()

        rospy.loginfo("Moving the robot..")

        #keep moving until the robot reaches the max velocity
        while(vel_ref < max_velocity):
            #get ths speed of the robot in the axis of interest
            #set maximum_velocity in the axis of interest
            if axis == 'x':
                vel_ref = self.linear_speed_x
                twist_msg.linear.x = max_velocity
            
            elif axis == 'y':
                vel_ref = self.linear_speed_y
                twist_msg.linear.y = max_velocity

            elif axis == 'z':
                vel_ref = self.angular_spped_z
                twist_msg.angular.z = max_velocity

            self.vel_pub.publish(twist_msg)
            time.sleep(0.01)

        #get the time when the robot reach its maximum velocity (for accel calculation)
        t1 = rospy.Time.now().to_sec()

        #stop the robot
        twist_msg.linear.x = 0.0
        twist_msg.linear.y = 0.0
        twist_msg.angular.z = 0.0
        self.vel_pub.publish(twist_msg)

        #calculate acceleration
        acceleration = max_velocity / (t1 - t0)

        return acceleration

if __name__ == "__main__":

    rospy.init_node("get_acceleration", anonymous = True)
   
    while not rospy.is_shutdown():
        try:
            axis_of_movement = sys.argv[1]
            max_velocity = float(sys.argv[2])
        except:
            rospy.logerr("Specify the maximum velocity and axis of movement. ie rosrun lino_nav_tune get_accel.py x 0.35") 
            break
        
        accel = Acceleration()

        rospy.loginfo("MAX ACCELERATION: %f", accel.get_acceleration(axis_of_movement, max_velocity))

        break