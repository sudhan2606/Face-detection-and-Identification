import os
import numpy as np
import cv2
# path = 'Face-dataset'
if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(BASE_DIR,"Face-dataset")
    #Mapping numpy array(images) to their ID(labels)
    x_train = []
    y_labels = []
    for root, dirs, files in os.walk(image_dir):
        for file in files :
            if file.endswith("jpg"):
                path = os.path.join(root,file)
                label = os.path.basename(path)[0]
                # print(label)
                # print(path)
                y_labels.append(int(label)) #use some number for labels
                image = cv2.imread(path)
                image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
                image_array = image
                x_train.append(image_array) # store it as a numpy array of gray colour
                # print(image_array)
    # print(y_labels)
    # print(x_train)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    # to train the model
    recognizer.train(x_train,np.array(y_labels))
    # saving the trained data, .yml file
    recognizer.save('trainedData.yml')

