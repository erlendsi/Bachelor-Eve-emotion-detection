# File to get the image of face from process-image and run it in a model to detect emotion.

# Import TEST_process-image.py

# import find face from process-image
# from ... import findFace

# Import models

#Import tensorflow


import rclpy # Python library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library

class emotionHelper(Node):
    def __init__(self):
        super().__init__('Algorithm node')  # Name of the nodee

        # Create the subscriber. This subscriber will receive an Image
        # from the video_frames topic. The queue size is 10 messages.
        self.subscription = self.create_subscription(Image, 'video_frames', self.listener_callback, 10)
        self.subscription  # prevent unused variable warning

        # Used to convert between ROS and OpenCV images
        self.br = CvBridge()

    def start(self):
        self.get_logger().info('Recieving frames')  # Priting recieving frames to the console

        # Convert ROS Image message to OpenCV image
        current_frame = self.br.imgmsg_to_cv2(data)

        # Find face and grayscale it
        faces_detected = findFace(current_frame)

        # Draw Triangles around the faces detected
        for (x, y, w, h) in faces_detected:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), thickness=7)
            roi_gray = gray_image[y: y + w, x: x + h]
            roi_gray = cv2.resize(roi_gray, (48, 48))

            # Processes the image and adjust it to pass it to the model
            image_pixels = tf.keras.preprocessing.image.img_to_array(roi_gray)

            image_pixels = np.expand_dims(image_pixels, axis=0)
            image_pixels /= 255

            # Get the prediction of the model
            predictions = model.predict(image_pixels)
            max_index = np.argmax(predictions[0])
            emotion_detection = ('Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise')  # monkey = happy
            emotion_prediction = emotion_detection[max_index]

            # Get the percentage of the predicted emotion
            # times 100 to get percentage. convert to int to get rid of decimal numbers
            max = int(predictions[0][max_index] * 100)
            percentage = str(max) + '%'

            # Write on the frame the emotion detected
            cv2.putText(frame, emotion_prediction, (int(x), int(y - 65)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

            # Write the percentage to the frame
            cv2.putText(frame, percentage, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

        resize_image = cv2.resize(frame, (1000, 700))
        cv2.imshow('Emotion', resize_image)
        cv2.waitKey(10)