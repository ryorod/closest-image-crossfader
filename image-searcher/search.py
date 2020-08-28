import os
import numpy as np
from PIL import Image
from getFeature import get_feature
import glob
import pickle
from datetime import datetime
import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client


def main():
    query_img_path = input("Enter the path of the query image: ")
    f = get_feature()
    features = []
    img_paths = []
    urls = query_img_path + " "
    for feature_path in glob.glob("feature/*"):
        features.append(pickle.load(open(feature_path, 'rb')))
        img_paths.append('img/' + os.path.splitext(os.path.basename(feature_path))[0] + '.jpg')



    

    img = Image.open(query_img_path) 
    uploaded_img_path = "uploaded/" + datetime.now().isoformat() + "_" + os.path.basename(query_img_path)
    img.save(uploaded_img_path)

    query = f.get(img)
    dists = np.linalg.norm(features - query, axis=1) 
    ids = np.argsort(dists)[:30]
    scores = [(dists[id], img_paths[id]) for id in ids]
    for score in scores:
        urls += "/Users/ryorod/image-searcher/" + score[1] + " "
    urls.rstrip()
    print(urls)

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="192.168.11.6",
        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=12000,
        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)
    client.send_message("/urls", urls)


if __name__=="__main__":
    main()