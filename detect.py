from __future__ import division
import time
import torch 
import torch.nn as nn
from torch.autograd import Variable
import numpy as np
import cv2 
from util import *
import argparse
import os 
import os.path as osp
from model import Yolo
import pickle as pkl
import pandas as pd
import random


# returns imlist given relative path of image directory
def get_imlist(images):
    try:
        imlist = [osp.join(osp.realpath('.'), images, img) for img in os.listdir(images)]
    except NotADirectoryError:
        imlist = []
        imlist.append(osp.join(osp.realpath('.'), images))
    except FileNotFoundError:
        print ("No file or directory with the name {}".format(images))
        exit()
    return imlist

def init_detector(imlist, confidence, nms_thresh, det, cfgfile, weightsfile, reso):
    batch_size = 1
    confidence = float(confidence)
    nms_thresh = float(nms_thresh)
    CUDA = torch.cuda.is_available()
    num_classes = 52
    classes = load_classes("darknet/obj.names")

    if not os.path.exists(det):
        os.makedirs(det)

    loaded_ims = [cv2.imread(x) for x in imlist]
        
    #Set up the neural network
    print("Loading network.....")
    model = Yolo(cfgfile)
    model.load_weights(weightsfile)
    print("Network successfully loaded")

    model.net_info["height"] = reso
    inp_dim = int(model.net_info["height"])
    assert inp_dim % 32 == 0 
    assert inp_dim > 32

    #If there's a GPU availible, put the model on GPU
    if CUDA:
        model.cuda()
    #Put model in evaluation mode
    model.eval()
    return batch_size, CUDA, num_classes, classes, model, inp_dim, imlist, loaded_ims


def get_output(batch_size, confidence, nms_thresh, CUDA, num_classes, classes, model, inp_dim, imlist, loaded_ims):

    im_batches = list(map(prep_image, loaded_ims, [inp_dim for x in range(len(imlist))]))
    im_dim_list = [(x.shape[1], x.shape[0]) for x in loaded_ims]
    im_dim_list = torch.FloatTensor(im_dim_list).repeat(1,2)

    leftover = 0
    if (len(im_dim_list) % batch_size):
        leftover = 1

    if batch_size != 1:
        num_batches = len(imlist) // batch_size + leftover            
        im_batches = [torch.cat((im_batches[i*batch_size : min((i +  1)*batch_size,
                            len(im_batches))]))  for i in range(num_batches)]  

    write = 0

    if CUDA:
        im_dim_list = im_dim_list.cuda()
        
    start_det_loop = time.time()
    for i, batch in enumerate(im_batches):
    #load the image 
        start = time.time()
        if CUDA:
            batch = batch.cuda()
        with torch.no_grad():
            prediction = model(Variable(batch), CUDA)

        prediction = write_results(prediction, confidence, num_classes, nms_conf = nms_thresh)

        end = time.time()

        if type(prediction) == int:

            for im_num, image in enumerate(imlist[i*batch_size: min((i +  1)*batch_size, len(imlist))]):
                im_id = i*batch_size + im_num
                print("{0:20s} predicted in {1:6.3f} seconds".format(image.split("/")[-1], (end - start)/batch_size))
                print("{0:20s} {1:s}".format("Objects Detected:", ""))
                print("----------------------------------------------------------")
            continue

        prediction[:,0] += i*batch_size    #transform the atribute from index in batch to index in imlist 

        if not write:                      #If we have't initialised output
            output = prediction  
            write = 1
        else:
            output = torch.cat((output,prediction))

        for im_num, image in enumerate(imlist[i*batch_size: min((i +  1)*batch_size, len(imlist))]):
            im_id = i*batch_size + im_num
            objs = [classes[int(x[-1])] for x in output if int(x[0]) == im_id]
            print("{0:20s} predicted in {1:6.3f} seconds".format(image.split("/")[-1], (end - start)/batch_size))
            print("{0:20s} {1:s}".format("Objects Detected:", " ".join(objs)))
            print("----------------------------------------------------------")

        if CUDA:
            torch.cuda.synchronize()       
    try:
        output
    except NameError:
        print ("No detections were made")
        exit()

    im_dim_list = torch.index_select(im_dim_list, 0, output[:,0].long())

    scaling_factor = torch.min(inp_dim/im_dim_list,1)[0].view(-1,1)


    output[:,[1,3]] -= (inp_dim - scaling_factor*im_dim_list[:,0].view(-1,1))/2
    output[:,[2,4]] -= (inp_dim - scaling_factor*im_dim_list[:,1].view(-1,1))/2



    output[:,1:5] /= scaling_factor

    for i in range(output.shape[0]):
        output[i, [1,3]] = torch.clamp(output[i, [1,3]], 0.0, im_dim_list[i,0])
        output[i, [2,4]] = torch.clamp(output[i, [2,4]], 0.0, im_dim_list[i,1])
    return output
    

def draw_res(output, loaded_ims, classes, det_dir, imlist):
    output_recast = time.time()
    class_load = time.time()
    colors = pkl.load(open("pallete", "rb"))

    def write(x, results):
        # top right corner
        c1 = tuple(x[1:3].int())
        # bottom left corner
        c2 = tuple(x[3:5].int())
        img = results[int(x[0])]
        cls = int(x[-1])
        color = random.choice(colors)
        label = "{0}".format(classes[cls])
        cv2.rectangle(img, c1, c2,color, 1)
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1 , 1)[0]
        c2 = c1[0] + t_size[0] + 3, c1[1] + t_size[1] + 4
        cv2.rectangle(img, c1, c2,color, -1)
        cv2.putText(img, label, (c1[0], c1[1] + t_size[1] + 4), cv2.FONT_HERSHEY_PLAIN, 1, [225,255,255], 1)
        return img


    map(lambda x: write(x, loaded_ims), output)

    det_names = pd.Series(imlist).apply(lambda x: "{}/det_{}".format(det_dir,x.split("/")[-1]))

    map(cv2.imwrite, det_names, loaded_ims)

    torch.cuda.empty_cache()

def arg_parse():
    """
    Parse arguements to the detect module
    
    """
    
    parser = argparse.ArgumentParser(description='YOLO v3 Detection Module')
   
    parser.add_argument("--images", dest = 'images', help = 
                        "Image / Directory containing images to perform detection upon",
                        default = "imgs", type = str)
    parser.add_argument("--det", dest = 'det', help = 
                        "Image / Directory to store detections to",
                        default = "res", type = str)
    parser.add_argument("--confidence", dest = "confidence", help = "Object Confidence to filter predictions", default = 0.5)
    parser.add_argument("--nms_thresh", dest = "nms_thresh", help = "NMS Threshhold", default = 0.4)
    parser.add_argument("--cfg", dest = 'cfgfile', help = 
                        "Config file",
                        default = "cfg/obj-yolov3.cfg", type = str)
    parser.add_argument("--weights", dest = 'weightsfile', help = 
                        "weightsfile",
                        default = "weights/obj-yolov3_last.weights", type = str)
    parser.add_argument("--reso", dest = 'reso', help = 
                        "Input resolution of the network. Increase to increase accuracy. Decrease to increase speed",
                        default = "608", type = str)
    
    return parser.parse_args()

def main():
    args = arg_parse()
    imlist = get_imlist(args.images)
    batch_size, CUDA, num_classes, classes, model, inp_dim, imlist, loaded_ims \
        = init_detector(imlist, args.confidence, args.nms_thresh, args.det, args.cfgfile, args.weightsfile, args.reso) 
    output = get_output(batch_size, args.confidence, args.nms_thresh, CUDA, num_classes, classes, model, inp_dim, imlist, loaded_ims)
    draw_res(output, loaded_ims, classes, args.det, imlist)

if __name__ == "__main__":
    main()
