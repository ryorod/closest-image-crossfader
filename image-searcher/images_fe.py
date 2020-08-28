import glob
import os
import pickle
from PIL import Image
from getFeature import get_feature

f = get_feature()

for img_path in sorted(glob.glob('img/*.jpg')):
    print(img_path)
    img = Image.open(img_path)
    feature = f.get(img)
    feature_path = 'feature/' + os.path.splitext(os.path.basename(img_path))[0] + '.pkl'
    pickle.dump(feature, open(feature_path, 'wb'))