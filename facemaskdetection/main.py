from drone_module.drone_config import Drone
from detection_module.real_time_detection import get_facenet_and_masknet
from detection_module.real_time_detection import detect_and_predict_mask
import cv2

if __name__ == '__main__':
    # Getting the faceNet and maskNet
    faceNet, maskNet = get_facenet_and_masknet()

    # Instatiating the Drone and setup operation
    drone_test = Drone(0, 640, 480, 0, 0, 0, 0, 0)
    status = drone_test.get_status()
    drone_test.get_stream()

    # loop over the frames from the video stream
    while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        frame = drone_test.get_frame()
        #frame = imutils.resize(frame, width=400)

        # detect faces in the frame and determine if they are wearing a
        # face mask or not
        locs, preds = detect_and_predict_mask(frame, faceNet, maskNet)

        # loop over the detected face locations and their corresponding
        # locations
        count = 0
        for (box, pred) in zip(locs, preds):
            # unpack the bounding box and predictions
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred

            # determine the class label and color we'll use to draw
            # the bounding box and text
            label = "Mask" if mask > withoutMask else "No Mask"
            color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

            # include the probability in the label
            label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
            print(label)

            # display the label and bounding box rectangle on the output
            # frame
            cv2.putText(frame, label, (startX, startY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

            # get snapshots of individuals without facemask
            # drone_test.get_snap_shots(label, frame)

        # show the output frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()
