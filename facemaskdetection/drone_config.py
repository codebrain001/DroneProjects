# Importing the Tello Drone Library
from djitellopy import Tello
# Importing OpenCV library
import cv2
# Importing time package
import time
# Importing OS module
import os

# Instatiating the Tello module
pkg = Tello()
# Connecting the drone to the python script after connecting to the Drone's WiFi
pkg.connect()


class Drone:

    """Wrapper class to setup the tello drone"""

    def __init__(self, width, height):
        self.StartCounter = 0
        self.width = width
        self.height = height
        self.back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 0

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
        return status_files.items()

    def get_stream_on(self):
        pkg.streamon()

    def get_stream_off(self):
        pkg.streamoff()

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

    def advance_movement(self):
        pkg.takeoff()
        pkg.move_forward(40)
        # pkg.rotate_counter_clockwise(90)

    def fallback_movement(self):
        pkg.rotate_counter_clockwise(90)
        pkg.move_forward(20)
        pkg.end()

    def get_movement(self):
        # Predefined mapped out movement in my use case
        pkg.takeoff()
        pkg.rotate_counter_clockwise(5)
        pkg.move_up(5)
        pkg.move_forward(5)
        pkg.rotate_clockwise(90)
        time.sleep(20)
        pkg.rotate_clockwise(90)
        pkg.move_forward(5)
        time.sleep(5)
        pkg.end()

    def get_snap_shots(self, label, frame):
        count = 0
        if label.split(':')[0] == 'No Mask':
            file_name = './snapshots/no mask ' + str(count) + '.jpg'
            print(file_name)
            cv2.imwrite(file_name, frame)
            count += 1
            time.sleep(2)
