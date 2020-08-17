






# Importing the Tello Drone Library
from djitellopy import Tello
# Importing OpenCV library
import cv2
# Importing time package
import time

# Instatiating the Tello module
pkg = Tello()
# Connecting the drone to the python script after connecting to the Drone's WiFi
pkg.connect()

startCounter = 1
# 0: Flight & 1: Stationed

# Desired Image size
width = 320
height = 240


class Drone:
    def __init__(self, back_velocity, left_right_velocity, up_down_velocity, yaw_velocity, speed):
        self.back_velocity = back_velocity
        self.left_right_velocity = left_right_velocity
        self.up_down_velocity = up_down_velocity
        self.yaw_velocity = yaw_velocity
        self.speed = speed

        pkg.back_velocity = self.back_velocity
        pkg.left_right_velocity = self.left_right_velocity
        pkg.up_down_velocity = self.up_down_velocity
        pkg.yaw_velocity = self.yaw_velocity
        pkg.set_speed = self.speed

    def status(self):
        print(f" Current Battery: {pkg.get_battery()} %")
        print(f" Current Fly time: {pkg.get_flight_time()} s")
        print(f" Current Height: {pkg.get_height()} cm")
        print(f" Current Atmospheric Pressure: { pkg.get_barometer()} Pa")
        print(f" Current Temperature:{pkg.get_temperature()} K")
        print(
            f" Cureent Speed in the X-axis,Y-axis and Z-axis respectively: [{pkg.get_speed_x()}, {pkg.get_speed_y()}, {pkg.get_speed_z()}] cm/s")
        print(f" Current Yaw Velocity: {pkg.get_yaw()} degrees/s")
        print(f" Current State: { pkg.get_current_state()}")

    def camera_stream(self):
        pkg.streamoff()
        pkg.streamon()

        while True:
            # Getting the images from the drone
            frame_read = pkg.get_frame_read()
            my_frame = frame_read.frame
            img = cv2.resize(my_frame, (width, height))
            #model
            
            cv2.imshow("Result", img)

            # WAIT FOR THE 'Q' BUTTON TO STOP
            if cv2.waitKey(1) & 0xFF == ord('q'):
                pkg.land()
                break


drone_test = Drone(0, 0, 0, 0, 0)
drone_test.status()
drone_test.camera_stream()
