# Importing the Tello Drone Library
from djitellopy import Tello
# Importing OpenCV library
import cv2
# Importing time package
import time
# Importing OS module
import os

# Import threading
from threading import Thread

# Instatiating the Tello module
pkg = Tello()
# Connecting the drone to the python script after connecting to the Drone's WiFi
pkg.connect()


class Drone:

    """Wrapper class to setup the tello drone"""

    def __init__(self, StartCounter, width, height, back_velocity, left_right_velocity, up_down_velocity, yaw_velocity, speed):
        self.StartCounter = StartCounter
        self.width = width
        self.height = height
        self.back_velocity = back_velocity
        self.left_right_velocity = left_right_velocity
        self.up_down_velocity = up_down_velocity
        self.yaw_velocity = yaw_velocity
        self.speed = speed

    def get_status(self):
        battery = pkg.get_battery()
        fly_time = pkg.get_flight_time()
        drone_height = pkg.get_height()
        atmospheric_pressure = pkg.get_barometer()
        temperature = pkg.get_temperature()
        yaw_velocity = pkg.get_yaw()
        speed_x = pkg.get_speed_x()
        speed_y = pkg.get_speed_y()
        speed_z = pkg.get_speed_z()
        acceleration_x = pkg.get_acceleration_x()
        acceleration_y = pkg.get_acceleration_y()
        acceleration_z = pkg.get_acceleration_z()

        #   Function to return a dictionary of the status
        status_files = {
            'battery': battery,
            'fly_time': fly_time,
            'drone_height': drone_height,
            'atmospheric_pressure': atmospheric_pressure,
            'temperature': temperature,
            'yaw_velocity': yaw_velocity,
            'speed': (speed_x, speed_y, speed_z),
            'acceleration': (acceleration_x, acceleration_y, acceleration_z)
        }
        return status_files

    def get_stream(self):
        pkg.streamoff()
        pkg.streamon()

    def get_frame(self):
        frame_read = pkg.get_frame_read()
        return frame_read.frame

    def get_video(self):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('drone_video.avi', fourcc, 20.0, (640, 480))
        frame_read = pkg.get_frame_read()
        while(True):
            cv2.imshow('Video Stream', frame_read.frame)
            out.write(frame_read.frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        out.release()
        cv2.destroyAllWindows()

        return 'complete'

    # ?def get_snap_shots(self, get_frame):
    #     frame = get_frame()
    #     count = 0
    #     if facemask_detection.label.split(':')[0] == 'No Mask':
    #         file_name = './no mask ' + str(count) + '.jpg'
    #         print(file_name)
    #         cv2.imwrite(file_name, frame)
    #         count += 1
    #         time.sleep(2)

    def get_movement(self):
        #   Predefined mapped out movement in my use case
        # pkg.takeoff()
        # pkg.rotate_counter_clockwise(20)
        # pkg.move_up(20)
        # pkg.move_forward(1000)
        # pkg.rotate_clockwise(90)
        # time.sleep(3)
        # pkg.rotate_clockwise(90)
        # pkg.move_forward(330)
        # time.sleep(5)
        # pkg.end()
        pass


drone_test = Drone(0, 640, 480, 0, 0, 0, 0, 0)
drone_test.get_status()
drone_test.get_stream()
drone_test.get_video()
# drone_test.get_movement()
