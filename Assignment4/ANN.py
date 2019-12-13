from PIL import Image
from skimage.io import imread
from skimage import color
from skimage.transform import resize
import matplotlib.pyplot as plt
import numpy as np


class NeuralNetwork:
    def __init__(self, layers):


        self.activation = self.tanh
        self.activation_deriv = self.tanh_derivative

        self.weights = []
        for i in range(1, len(layers)):
            if i == len(layers)-1:
                self.weights.append((2 * np.random.random((layers[i - 1] + 1, layers[i])) - 1) * 0.25)
            else:
                self.weights.append((2 * np.random.random((layers[i - 1] + 1, layers[i] + 1)) - 1) * 0.25)

    def train(self, X, y, learning_rate=0.2, epochs=10000):

        X = np.atleast_2d(X)
        temp = np.ones([X.shape[0], X.shape[1]+1])
        temp[:, 0:-1] = X  # adding bias to input layer
        X = temp
        y = np.array(y)

        for k in range(epochs):
            i = np.random.randint(X.shape[0])
            a = [X[i]]

            for l in range(len(self.weights)):  # forward
                a.append(self.activation(np.dot(a[l], self.weights[l])))

            error = y[i] - a[-1]
            deltas = [error * self.activation_deriv(a[-1])]

            for l in range(len(a) - 2, 0, -1):  # backward
                deltas.append(deltas[-1].dot(self.weights[l].T)*self.activation_deriv(a[l]))
            deltas.reverse()
            for i in range(len(self.weights)):  # update
                layer = np.atleast_2d(a[i])
                delta = np.atleast_2d(deltas[i])
                self.weights[i] += learning_rate * layer.T.dot(delta)

    def predict(self, x):

        x = np.array(x)
        temp = np.ones(x.shape[0]+1)
        temp[0:-1] = x
        a = temp
        for l in range(0, len(self.weights)):
            a = self.activation(np.dot(a, self.weights[l]))
        return a

    def tanh(self,x):
        return np.tanh(x)

    def tanh_derivative(self,x):
        return 1.0 - np.tanh(x) ** 2

def window(pic, i, j):

    arr = []
    for p in range(i-1, i+2):
        for q in range(j-1, j+2):
            arr.append(pic[p, q])
    return arr


def normalize(pic):

    for i in range(pic.shape[0]):
        for j in range(pic.shape[1]):
            pic[i, j, 0] = (pic[i, j, 0] // 80) * 80
            pic[i, j, 1] = (pic[i, j, 1] // 80) * 80
            pic[i, j, 2] = (pic[i, j, 2] // 80) * 80
    return pic


def onehot(num):

    onehot = [0,0,0,0]
    for i in range(4):
        if i == num:
            onehot[i]=1

    return onehot


def recover(onehot):

    num = 0
    for i in range(4):
        if round(onehot[i]) == 1:
            num = i
    return num


def compare(original, prediction):
    difference=prediction/80 - original/80
    op1 = np.sqrt(np.sum(np.square(prediction/80 - original/80)))

    op=op1/(difference.shape[0]*difference.shape[1]*difference.shape[2])
    return op



img = imread("/Users/zhaoxiangliu/Desktop/CS-IntroToAI/Assignment4/ANNdataset/sky/sky.jpg" )
origin=img
img = normalize(img)
gray=color.rgb2gray(img)
# plt.imshow(gray,cmap='gray')
train_data=gray
train_label=img
img2 = imread("/Users/zhaoxiangliu/Desktop/CS-IntroToAI/Assignment4/ANNdataset/sky/sky2.jpg" )
img2=normalize(img2)
gray2=color.rgb2gray(img2)
test_x=gray2
test_y=img2

layers = [9, 9, 4]
rate = 0.05
epochs = 20000
red = NeuralNetwork(layers)
blue = NeuralNetwork(layers)
green = NeuralNetwork(layers)
X = []
y_r = []
y_g = []
y_b = []

for i in range(1, train_data.shape[0]-1):
    for j in range(1, train_data.shape[1]-1):
        X.append(window(train_data, i, j))
        y_r.append(onehot(train_label[i, j, 0] / 80))
        y_g.append(onehot(train_label[i, j, 1] / 80))
        y_b.append(onehot(train_label[i, j, 2] / 80))


red.train(X, y_r, learning_rate=rate, epochs=epochs)
green.train(X, y_g, learning_rate=rate, epochs=epochs)
blue.train(X, y_b, learning_rate=rate, epochs=epochs)

result = np.zeros([test_x.shape[0], test_x.shape[1], 3], dtype=np.uint8)
for i in range(1, test_x.shape[0] - 1):
    for j in range(1, test_x.shape[1] - 1):
        result[i, j, 0] = recover(red.predict(window(test_x, i, j))) * 80
        result[i, j, 1] = recover(green.predict(window(test_x, i, j))) * 80
        result[i, j, 2] = recover(blue.predict(window(test_x, i, j))) * 80


plt.figure(figsize=(12, 12))

plt.subplot(3,1,1)
plt.title('train')
plt.imshow(origin)

plt.subplot(3,1,2)
plt.title('real')
plt.imshow(test_y)

plt.subplot(3,1,3)
plt.title('predict')
plt.imshow(result)
plt.show()



print("Euclidean distance:", compare(test_y, result))




