from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
from tool import *
import numpy as np

size=(64,64)
train_path="./train/"
# size=(64,64)
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
index = np.random.randint(len(x_train))
# index=0
train_in = np.reshape( x_train, (-1, size[0], size[1], 1) )/100 
test_in = np.reshape( x_test, (-1, size[0], size[1], 1) ) /100 
train_out = np.reshape( y_train, (-1, size[0], size[1], 2) ) /255
print(train_out.shape)
test_out = np.reshape( y_test, (-1, size[0], size[1], 2) ) /255
model = tf.keras.models.load_model('test5.h5')
# history = model.fit( train_in, train_out, batch_size=3, epochs = 50, validation_data = (test_in, test_out) )
# model.save("test6.h5")
prediction = model.predict( np.array([train_in[index]]) ) *255

print('Grayscale:')
show_grayscale_matrix(x_train[index].reshape(size[1],size[0]))
print('RGB:')
show_rgb_matrix(lab_channel_to_rgb(x_train[index], y_train[index], size))
print('Prediction:')
show_rgb_matrix(lab_channel_to_rgb(x_train[index], prediction[0],size))

