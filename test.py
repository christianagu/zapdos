import requests
import cv2
import tensorflow as tf

cap = cv2.VideoCapture(0)
model = tf.keras.models.load_model('path_to_model.h5')


prediction = model.predict(processed_frame)

while True:
    ret, frame = cap.read()
    cv2.imshow('USB Camera Feed')


    if cv2.waitKey(1) & 0xFF:
        break

cap.release()
cv2.destroyAllWindows()



# don't forget to set up raspberry pi - if this hasn't been started on
# by 10/2. you failed

# Set up open cv obj det

# set up classes for robot arm and servos

