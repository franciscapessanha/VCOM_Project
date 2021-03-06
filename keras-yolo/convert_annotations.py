import xml.etree.ElementTree as ET
import numpy as np
import os
import glob

sets=['train', 'val', 'test']
classes = ['serralves', 'musica', 'clerigos', 'camara', 'arrabida']

"""
It will convert VOC annotations
"""
def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(image_set, image_id):
    #Box format: x_min,y_min,x_max,y_max,class_id (no space)
    in_file = open('../resized_dataset/divided_sets/%s/%s.xml'%(image_set, image_id))
    tree=ET.parse(in_file)
    root = tree.getroot()
    annotation = ''
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(float(xmlbox.find('xmin').text)), int(float(xmlbox.find('ymin').text)), int(float(xmlbox.find('xmax').text)), int(float(xmlbox.find('ymax').text)))
        annotation = annotation + ",".join([str(a) for a in b]) + ',' + str(cls_id) 
    
    return annotation

for image_set in sets:
    image_list = []
    annotations = []
    image_ids = [f.split("/")[-1].replace('.xml','') for f in glob.glob('../resized_dataset/divided_sets/%s/*.xml' % image_set)]
    
    for image_id in image_ids:
        ann = convert_annotation(image_set, image_id)
        annotations.append('../resized_dataset/divided_sets/%s/%s.jpg ' %(image_set, image_id) + ann)
    
    if not os.path.exists('porto_dataset'):
        os.makedirs('porto_dataset')

    with open('porto_dataset/annotations_%s.txt' % (image_set), 'w') as f:
        for item in np.hstack(annotations):
            f.write("%s\n" % item)

filenames = ['porto_dataset/annotations_train.txt', 'porto_dataset/annotations_val.txt']
with open('porto_dataset/annotations_trainval.txt','w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            outfile.write(infile.read())

with open('porto_dataset/porto_classes.txt', 'w') as f:
    for item in np.hstack(classes):
        f.write("%s\n" % item)
