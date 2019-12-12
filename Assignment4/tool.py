# coding=utf-8
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import random
from skimage.io import imread
from skimage import color
from skimage.transform import resize

def load_and_resize(path, size):
    resized_pics=[]
    # print(path)
    for roots,dirs,files in os.walk(path):
        for file in files:
            filename,ext = os.path.splitext(file)
            # print(ext)
            if ext == ".jpg":
                img = imread(roots +"/" + file)
                img = resize(img, size)
                resized_pics.append(img)
    return resized_pics

def show_rgb_matrix(pix_array):
    plt.imshow(pix_array)
    plt.show()

def show_grayscale_matrix(pix_array):
    plt.imshow(pix_array,cmap='gray')
    plt.show()


def load_imgs(path, size):
    rgb_pics=load_and_resize(path,size)
    return rgb_pics

def rgb_to_lab(rgb_pixs):
    lab_pixs=[]
    for rgb_pix in rgb_pixs:
        lab_pix = color.rgb2lab(rgb_pix)
        lab_pixs.append(lab_pix)
    return lab_pixs

def lab_to_rgb(lab_pixs, size):
    rgb_pixs=[]
    for lab_pix in lab_pixs:
        rgb_pix= color.lab2rgb(lab_pix)
        rgb_pixs.append(rgb_pix)
    return rgb_pixs

def lab_channel_to_rgb(channel_l, channel_ab, size):
    a = []
    b = []
    for x in range(size[0]):
        for y in range(size[1]):
            a.append(channel_ab[x][y][0])
            b.append(channel_ab[x][y][1])
    a = np.array(a).reshape(size[1],size[0])
    b = np.array(b).reshape(size[1],size[0])
    a = np.subtract(a, 128)
    b = np.subtract(b, 128)
    l = channel_l.reshape(size[1],size[0])
    pred_lab_pix = []
    for y in range(size[1]):
        row=[]
        for x in range(size[0]):
            lab_pixel = (l[y][x], a[y][x], b[y][x])
            row.append(lab_pixel)
        pred_lab_pix.append(row)
    pred_lab_pixs = []
    pred_lab_pixs.append(pred_lab_pix)
    pred_rgb_pix = lab_to_rgb(pred_lab_pixs, size)
    return pred_rgb_pix[0]