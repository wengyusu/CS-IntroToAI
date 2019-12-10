# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import pandas as pd
from PIL import Image
import os
import sys
import glob
import shutil
import matplotlib.pyplot as plt
import random
from skimage.io import imread
from skimage import color
from skimage.transform import resize
import tensorflow as tf

# ## Load rgb pixel matrix from file

def load_and_resize(path, size):
    resized_pics=[]
    # print(path)
    for roots,dirs,files in os.walk(path):
        for file in files:
            filename,ext = os.path.splitext(file)
            # print(filename)
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
    rgb_pics=load_and_resize(original_path,size)
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

original_path="./Dataset/beach/"
size=(64,64)
rgb_pixs = load_imgs(original_path, size)
lab_pixs = np.array(rgb_to_lab(rgb_pixs))
print(rgb_pixs[0][0][0])
print(lab_pixs[0][0][0])
print(lab_pixs.shape)

x_train = lab_pixs[:, :, :, 0]
test_index = np.random.randint(len(x_train))
x_test = x_train[test_index]
y_train = np.add(lab_pixs[:, :, :, 1:], 128)
y_test = y_train[test_index]
train_in = np.reshape( x_train, (-1, size[0], size[1], 1) )/255 
test_in = np.reshape( x_test, (-1, size[0], size[1], 1) ) /255 
train_out = np.reshape( y_train, (-1, size[0], size[1], 2) )/255 
print(train_out.shape)
test_out = np.reshape( y_test, (-1, size[0], size[1], 2) )/255 

digit_input = tf.keras.layers.Input( shape = (size[0],size[1],1) )## Each input image is 64x64 pixels, with 1 channel depth for each (the grayscale value)
cnn_1 = tf.keras.layers.Conv2D( filters = 32, kernel_size = (5,5), strides = (1,1), padding = "same", activation = tf.nn.relu, use_bias = True, kernel_initializer = tf.keras.initializers.TruncatedNormal(mean=0.0, stddev=0.1, seed=None), bias_initializer = tf.keras.initializers.Constant(value=0.1) )( digit_input )
max_poo1 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=None, padding='same', data_format=None)(cnn_1)
cnn_2 = tf.keras.layers.Conv2D( filters = 64, kernel_size = (5,5), strides = (1,1), padding = "same", activation = tf.nn.relu, use_bias = True, kernel_initializer = tf.keras.initializers.TruncatedNormal(mean=0.0, stddev=0.1, seed=None), bias_initializer = tf.keras.initializers.Constant(value=0.1) )(max_poo1)
max_poo2 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=None, padding='same', data_format=None)(cnn_2)
flatten_image = tf.keras.layers.Flatten()( max_poo2 )

    ## This flattens the block from the CNN layer to a flat vector 
fc1 = tf.keras.layers.Dense(units = 2048, activation=tf.nn.relu, use_bias=True, kernel_initializer = tf.keras.initializers.TruncatedNormal(mean=0.0, stddev=0.1, seed=None), bias_initializer = tf.keras.initializers.Constant(value=0.1) )(flatten_image)
fc2 = tf.keras.layers.Dense(units = 4096, activation=tf.nn.relu, use_bias=True, kernel_initializer = tf.keras.initializers.TruncatedNormal(mean=0.0, stddev=0.1, seed=None), bias_initializer = tf.keras.initializers.Constant(value=0.1) )(fc1)
dropout_1 = tf.keras.layers.Dropout( rate = 0.0 )( fc2 )
fc3 = tf.keras.layers.Dense( units = size[0]*size[1]*2, activation = None )(dropout_1 )
a_b_channels = tf.keras.layers.Reshape((size[0], size[1], 2))(fc3)


model = tf.keras.Model( inputs = digit_input, outputs = a_b_channels )
model.compile( optimizer = "adam", loss = 'mean_squared_error', metrics = ['mean_squared_error'] )

history = model.fit( train_in, train_out, batch_size=3, epochs = 200 )
prediction = model.predict( test_in ) * 255
print(prediction.shape)


print(y_test.shape)
print(prediction.shape)
print('Grayscale:')
show_grayscale_matrix(x_test.reshape(size[1],size[0]))
print('RGB:')
show_rgb_matrix(lab_channel_to_rgb(x_test, y_test, size))
print('Prediction:')
show_rgb_matrix(lab_channel_to_rgb(x_test, prediction[0],size))