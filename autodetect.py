#!/usr/bin/env python
# coding: utf-8

# In[16]:


from detect import DETECT
from detect_grid import DETECT_GRID
from datetime import date
import time
import os
import cv2
from matplotlib import pyplot as plt
import xml.etree.cElementTree as ET


# In[3]:


FILES_DIR = r'\\magna.global\nbd\MagJIS_A3Q2\EOL_Images'

window_size = 1.5
local = True
# In[4]:


def join_dir(elements):
    joined_dir = ''
    for e in elements:
        joined_dir = os.path.join(joined_dir, e)
    return joined_dir


# In[5]:


def start_detection(image_dir, grid):
    det = DETECT_GRID.run(weights=r'C:\Users\samrutt\OneDrive - Magna\Documents\Error_detection\application_test\YOLO\data_yolo\yolov5\runs\train\exp7\weights\best.pt',
              source=image_dir,
              nosave = True,
              view_img= False,
              grid_cells=grid)
    return det


# In[6]:
def check_img(dir, name, old_list):
    #global wf
    images_new = os.listdir(dir)
    new_image = list(set(images_new) - set(old_list))
    #new_image=['221854824A3VL_10145-A_175914.jpg']
    if len(new_image) > 0:
        print('New image: ', new_image[0])
        old_list = images_new
        det_img, det_cell = start_detection(os.path.join(dir,new_image[0]), grid)
        #show_img(det_img)
        save_xml(det_cell, new_image[0], dir)

    return old_list

def save_xml(cells, img_name, dir):

    root = ET.Element("wrinkles")

    for cell in cells:
        c = ET.Element('cell')
        root.append(c)
        ET.SubElement(c, "Defekt", name="Defekt").text = "4"
        ET.SubElement(c, "Koordinate_X", name="Koordinate_X").text = cell[1]
        ET.SubElement(c, "Koordinate_Y", name="Koordinate_Y").text = cell[0]
        ET.SubElement(c, "Koordinate_Z", name="Koordinate_Z").text = 'Front view'
        ET.SubElement(c, "path", name="path").text = dir
        

    tree = ET.ElementTree(root)
    tree.write(img_name.split('.')[0] + ".xml")

def show_img(img):
    global wf
    global window_size

    img = cv2.resize(img, (int(180*window_size), int(255*window_size)))

    x_offset = int(173*window_size)
    y_offset = int(104*window_size)

    x_end = x_offset + img.shape[1]
    y_end = y_offset + img.shape[0]

    wf[y_offset:y_end,x_offset:x_end] = img

    #cv2.imwrite('wireframe.png', wf)
    cv2.imshow('MagJIS prediction', wf)
    cv2.waitKey(1)


# In[7]:
prod_folders = os.listdir(os.path.join(FILES_DIR, 'OP10145_VOR'))
prod_folders = [ int(x) for x in prod_folders ]
last_folder = max(prod_folders)

DIR_BEFORE = join_dir([FILES_DIR, 'OP10145_VOR', str(last_folder)])
#DIR_AFTER = join_dir([FILES_DIR, 'OP10145_NACH', td_map])


# In[13]:

'''
test_img = os.listdir(DIR_BEFORE)[3]
test = start_detection(test_img, DIR_BEFORE)
test = cv2.resize(test, (500, 900))
cv2.imshow('test', test)
cv2.waitKey()
'''
# In[1]:
grid_size = (384, 216)
grid = []
for x in range(0,5):
    for y in range(0,5):
        grid.append([chr(y+65)+str(x+1),  x*grid_size[1], y*grid_size[0]])

images_before_old = os.listdir(DIR_BEFORE)
#images_after_old = os.listdir(DIR_AFTER)

wf = cv2.imread(r'C:\Users\samrutt\OneDrive - Magna\Pictures\visual_instpection.png')
wf = cv2.resize(wf, (int(557*window_size), int(423*window_size)))


test_path = r'C:\Users\samrutt\OneDrive - Magna\Documents\Error_detection\application_test\YOLO\data_yolo\data_yolo_v2\images\test'
test_img = os.listdir(test_path)

#pred = start_detection(os.path.join(test_path, test_img[0]), grid)

#show_img(pred)
i=0
while True:
    if local:
        try:
            det_img, det_cell = start_detection(os.path.join(test_path, test_img[i]), grid)
            #show_img(det_img)
            save_xml(det_cell, test_img[i], test_path)
        except:
            print('Not possible  for image')
        time.sleep(30)
        i+=1

    else:
        prod_folders_new = os.listdir(os.path.join(FILES_DIR, 'OP10145_VOR'))
        if prod_folders_new != prod_folders:
            prod_folders = prod_folders_new
            prod_folders = [ int(x) for x in prod_folders ]
            last_folder = max(prod_folders)
            DIR_BEFORE = join_dir([FILES_DIR, 'OP10145_VOR', str(last_folder)])
            images_before_old = os.listdir(DIR_BEFORE)

        images_before_old = check_img(DIR_BEFORE, 'Grid before ironing', images_before_old)
        time.sleep(3)
    #images_after_old = check_img(DIR_AFTER, 'Grid after ironing', images_after_old)
    


# In[ ]:




