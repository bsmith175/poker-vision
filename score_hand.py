import numpy as np
from detect import init_detector, get_output
from util import class_num_to_tuple
from os import path as osp
import argparse
from probability import choose_function 

CONF = .6
NMS_THRESH = .4
RES = "./res"
CFG = "cfg/obj-yolov3.cfg"
WEIGHTS = "weights/obj-yolov3_last.weights"

# param: hole: path to personal hand image
# param: community: path to community cards image
def get_cards(hole_img, community_img=None):
    bs = 1
    reso = "608"
    if community_img:
        imlist = [osp.join(osp.realpath('.'), hole_img), osp.join(osp.realpath('.'), community_img)]
    if not community_img:
        imlist = [osp.join(osp.realpath('.'), hole_img)]

    batch_size, CUDA, num_classes, classes, model, inp_dim, imlist, loaded_ims \
        = init_detector(imlist, CONF, NMS_THRESH, RES, CFG, WEIGHTS, reso)
    output = get_output(batch_size, CONF, NMS_THRESH, CUDA, num_classes, classes, model, inp_dim, imlist, loaded_ims)
    classes = output[:, -1]
    cards = set()
    for i in range(len(classes)):
        cards.add(class_num_to_tuple(classes[i]))
    print(list(cards))
    return list(cards)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("imgs", nargs="+", help="1-2 images to be scored as a single hand, paths relative to project root")
    args = parser.parse_args()
    if (len(args.imgs) > 2):
        print("Error: more than two images. Please enter one image for your hand and optionally an image of the community cards.")
        exit()
    cards = get_cards(*args.imgs)
    choose_function(cards)
    

if __name__ == "__main__":
    main()
