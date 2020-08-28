from keras.preprocessing import image
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.models import Model
import numpy as np


class get_feature:
    def __init__(self):
        vgg = VGG16(weights='imagenet')
        self.model = Model(inputs=vgg.input, outputs=vgg.get_layer('fc1').output)

    def get(self, img):  
        img = img.resize((224, 224)) 
        img = img.convert('RGB') 
        x = image.img_to_array(img) 
        x = np.expand_dims(x, axis=0) 
        x = preprocess_input(x) 

        feature = self.model.predict(x)[0] 
        return feature / np.linalg.norm(feature)