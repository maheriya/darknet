import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets=[
        ('VOC',  '2012', 'train'),
        ('VOC',  '2012', 'val'),
        ('VOC',  '2007', 'train'),
        ('VOC',  '2007', 'val'),
        ('VOC',  '2007', 'test'),
        ('DVIA', '2017', 'train'),
        ('DVIA', '2017', 'test')]

## cow=>stair, sheep=>doorframe
#classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "stair", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "doorframe", "sofa", "train", "tvmonitor"]


def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(db, year, image_id):
    in_file = open('VOCdevkit/%s%s/Annotations/%s.xml'%(db, year, image_id))
    out_file = open('VOCdevkit/%s%s/labels/%s.txt'%(db, year, image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        #difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes: # or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()

## VOC and DVIA databases
listtrain = ""
listtrainall = ""
listtest = ""
if not os.path.exists('lists'):
    os.makedirs('lists')
for db, year, image_set in sets:
    if not os.path.exists('VOCdevkit/%s%s/labels/'%(db, year)):
        os.makedirs('VOCdevkit/%s%s/labels/'%(db, year))
    image_ids = open('VOCdevkit/%s%s/ImageSets/Main/%s.txt'%(db, year, image_set)).read().strip().split()
    lname = 'lists/%s_%s_%s.txt'%(db, year, image_set)
    list_file = open(lname, 'w')
    for image_id in image_ids:
        list_file.write('%s/VOCdevkit/%s%s/JPEGImages/%s.jpg\n'%(wd, db, year, image_id))
        convert_annotation(db, year, image_id)
    list_file.close()
    listtrainall += " " + lname
    if (image_set == "train" or image_set == "val"):
        listtrain += " " + lname
    if (image_set == "test"):
        listtest += " " + lname


os.system("cat {} > lists/train.txt".format(listtrain))
os.system("cat {} > lists/train.all.txt".format(listtrainall))
os.system("cat {} > lists/test.txt".format(listtest))

