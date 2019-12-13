# Assignment4
Yusu Weng(yw706) Zhaoxiang Liu(zl355)

## CNN-Regression Approach
### Model Structure
Input Layer

$\Downarrow$

Convolutional Layer

$\Downarrow$

Convolutional Layer

$\Downarrow$

MaxPooling Layer

$\Downarrow$

Flatten Layer

$\Downarrow$

Dropout Layer

$\Downarrow$

FullConnected Layer

$\Downarrow$

FullConnected Layer

$\Downarrow$

Output Layer
### Representing the process
To better solve the problem, we first convert RGB color space to CIELAB(LAB) color space. The LAB space consists of three channels: L for lightness, A for green-red, B for blue-yellow. The value of L ranges from 0 to 100, while other two channel range from -128 to 127. Since the grayscale image only has L channel, we can represent the process as mapping the L channel as input to the A&B channels as the output. At last, we convert the predicted LAB space back to the RGB space.

### Data

We obtain the data from Imagenet, with the category of seashore.
```
http://image-net.org/api/text/imagenet.synset.geturls?wnid=n09428293
```
Due to the limitation of the computing power of our laptops, we only downloaded 1000 images as the train set, and 100 addtional images as the validation set.

These images are not included in the archive but can be downloaded by the python script `get_dataset.py`

### Preprocess
Before training, we resize the images to 64pixelsx64pixels and read as a 2D array.

We also preprocess the input values of LAB channels, converting them range from 0 to 1.
### Evaluation

We choose Mean-squared Error(MSE) as the loss function:

$Loss=\frac{1}{n}\sum^{n}_{i=1}{\sqrt{(\tilde{A_i}-A_i)^2+(\tilde{B_i}-B_i)^2}}$

n is the total number of pixels

We also define that if $|\tilde{A_i}-A_i|\leq=10$ and $|\tilde{B_i}-B_i|\leq=10,pixel_i$ is correct since human can hardly tell the difference.

So the $accuracy=\frac{\#\{correct pixels\}}{\#\{total pixels\}}$

### Training

Instead of Gradient descent, we choose Stochatic gradient descent for two reasons. First, it is computationally cheaper to compute the gradients with respect to one of these loss terms
rather than every loss term in the full sum of dataset. Second, SGD is less likely to be trapped in local minima as it is less sensitive to fine grained details in dataset. Practically, we set the batch size as 10 instead of the total number of the dataset.


We also introduce some methods to prevent overfitting:

`Regularization`

We add a L2 Regularizer to the loss function:

$Cost=Loss+\lambda\sum{||w||^2}$

In practice we set the $\lambda$ 0.001

`Early Termination`

As mentioned before we have a validation set to track the performation. We can terminate the training when the error on the validation set beigin to increase.

`Dropout Layer`

The dropout layer can ignore certain sets of neurons during the training which is chosen at random.Dropout forces a neural network to learn more robust features that are useful in conjunction with many different random subsets of the other neurons.We set the dropout rate as 0.2

### Assesment
Our model can reach a 68% accuracy on coloring images with category of seashore. 

`Demos`

`Example1`

Real
![Real](demo/1.png)

Prediction

![Prediction](demo/2.png)

`Example2`

Real
![Real](demo/3.png)

Prediction

![Prediction](demo/4.png)

`Example3`

Real
![Real](demo/5.png)

Prediction

![Prediction](demo/6.png)

`Example4`

Real
![Real](demo/7.png)

Prediction

![Prediction](demo/8.png)

Base on our observation, predicted images make sense in some degree, but still have some evident flaws:

First, the overall prediction of our model is conservative. The predicted color is always less vivid than the real color.

Second, the margin between sea, sky and beach is vague and the model tend to use close colors to colorize them.

Finally, the model may confuse the sea with beach if the coastline is irregular.

Besides, the model cannot handle the images that are not seashore at all as was expected. The model will try to use blue and yellow which are colors of sea and sands to colorize the image.
![](demo/9.png)
![](demo/10.png)
### Rethinking & Improvement

First, the size of dataset maybe not enough for the problem as our model seems not to extract all the features from the image correctly, which leads some mistakes when finding the margin.

Then, the loss function we choose encourages the model to make a conservative selection on colors. These losses are inherited from standard regression
problems, where the goal is to minimize Mean squared error between an estimate
and the ground truth.
Additionally, the model will prefer to use a set of similar color uniformly rather than choose a set of colors that are distinct to each other.

To improve it, maybe we should try to consider it as a classification problem rather than a regression problem to avoid the model to choose an mean of the set. Instead, we can use cross entropy loss to have a better performance








