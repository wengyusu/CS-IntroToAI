# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import pandas as pd
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
from tool import *
# ## Load rgb pixel matrix from file



train_path="./train/"
size=(64,64)
rgb_pixs = load_imgs(train_path, size)
lab_pixs = np.array(rgb_to_lab(rgb_pixs))
print(rgb_pixs[0][0][0])
print(lab_pixs[0][0][0])
print(lab_pixs.shape)

x_train = lab_pixs[:, :, :, 0]
y_train = np.add(lab_pixs[:, :, :, 1:], 128)

test_path="./test/"
rgb_pixs_1 = load_imgs(test_path, size)
lab_pixs_1 = np.array(rgb_to_lab(rgb_pixs_1))
x_test = lab_pixs_1[:, :, :, 0]
y_test = np.add(lab_pixs_1[:, :, :, 1:], 128)
# test_index = np.random.randint(len(x_train))
# x_test = x_train[test_index]
# y_test = y_train[test_index]
train_in = np.reshape( x_train, (-1, size[0], size[1], 1) )/100 
test_in = np.reshape( x_test, (-1, size[0], size[1], 1) ) /100 
train_out = np.reshape( y_train, (-1, size[0], size[1], 2) )/255 
print(train_out.shape)
test_out = np.reshape( y_test, (-1, size[0], size[1], 2) )/255 

# digit_input = tf.keras.layers.Input( shape = (size[0],size[1],1) )## Each input image is 64x64 pixels, with 1 channel depth for each (the grayscale value)
# cnn_1 = tf.keras.layers.Conv2D( filters = 32, kernel_size = (5,5), strides = (1,1), padding = "same", activation = tf.nn.relu, use_bias = True, kernel_initializer = tf.keras.initializers.TruncatedNormal(mean=0.0, stddev=0.1, seed=None), bias_initializer = tf.keras.initializers.Constant(value=0.1) )( digit_input )
# max_poo1 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=None, padding='same', data_format=None)(cnn_1)
# cnn_2 = tf.keras.layers.Conv2D( filters = 64, kernel_size = (5,5), strides = (1,1), padding = "same", activation = tf.nn.relu, use_bias = True, kernel_initializer = tf.keras.initializers.TruncatedNormal(mean=0.0, stddev=0.1, seed=None), bias_initializer = tf.keras.initializers.Constant(value=0.1) )(max_poo1)
# max_poo2 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=None, padding='same', data_format=None)(cnn_2)
# flatten_image = tf.keras.layers.Flatten()( max_poo2 )

#     ## This flattens the block from the CNN layer to a flat vector 
# fc1 = tf.keras.layers.Dense(units = 2048, activation=tf.nn.relu, use_bias=True, kernel_initializer = tf.keras.initializers.TruncatedNormal(mean=0.0, stddev=0.1, seed=None), bias_initializer = tf.keras.initializers.Constant(value=0.1) )(flatten_image)
# fc2 = tf.keras.layers.Dense(units = 4096, activation=tf.nn.relu, use_bias=True, kernel_initializer = tf.keras.initializers.TruncatedNormal(mean=0.0, stddev=0.1, seed=None), bias_initializer = tf.keras.initializers.Constant(value=0.1) )(fc1)
# dropout_1 = tf.keras.layers.Dropout( rate = 0.5 )( fc2 )
# fc3 = tf.keras.layers.Dense( units = size[0]*size[1]*2, activation = None )(dropout_1 )
# a_b_channels = tf.keras.layers.Reshape((size[0], size[1], 2))(fc3)
digit_input = tf.keras.layers.Input( shape = (size[0],size[1],1) )## Each input image is 64x64 pixels, with 1 channel depth for each (the grayscale value)
cnn_1 = tf.keras.layers.Conv2D( filters = 32, kernel_size = (3,3), strides = (1,1), padding = "same", activation = tf.nn.relu )( digit_input )
cnn_2 = tf.keras.layers.Conv2D( filters = 32, kernel_size = (3,3), strides = (1,1), padding = "same", activation = tf.nn.relu )( cnn_1 )
max_poo1 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=None, padding='same', data_format=None)(cnn_2)
cnn_3 = tf.keras.layers.Conv2D( filters = 64, kernel_size = (3,3), strides = (1,1), padding = "same", activation = tf.nn.relu )(max_poo1)
cnn_4 = tf.keras.layers.Conv2D( filters = 64, kernel_size = (3,3), strides = (1,1), padding = "same", activation = tf.nn.relu )(cnn_3)
max_poo2 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=None, padding='same', data_format=None)(cnn_4)
flatten_image = tf.keras.layers.Flatten()( max_poo2 )

    ## This flattens the block from the CNN layer to a flat vector 
fc1 = tf.keras.layers.Dense(units = 2048, activation=tf.nn.relu)(flatten_image)
fc2 = tf.keras.layers.Dense(units = 2048, activation=tf.nn.relu )(fc1)
dropout_1 = tf.keras.layers.Dropout( rate = 0.5 )( fc2 )
fc3 = tf.keras.layers.Dense( units = size[0]*size[1]*2, activation = None )(dropout_1 )
a_b_channels = tf.keras.layers.Reshape((size[0], size[1], 2))(fc3)

model = tf.keras.Model( inputs = digit_input, outputs = a_b_channels )
model.compile( optimizer = "adam", loss = 'mean_squared_error', metrics = ['accuracy'] )

history = model.fit( train_in, train_out, batch_size=3, epochs = 50, validation_data = (test_in, test_out) )
model.save("test3.h5")
prediction = model.predict( test_in ) * 255
print(prediction.shape)


print(y_test.shape)
print(prediction.shape)
print('Grayscale:')
show_grayscale_matrix(x_test[0].reshape(size[1],size[0]))
print('RGB:')
show_rgb_matrix(lab_channel_to_rgb(x_test[0], y_test[0], size))
print('Prediction:')
show_rgb_matrix(lab_channel_to_rgb(x_test[0], prediction[0],size))