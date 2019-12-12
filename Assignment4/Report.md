# Assignment4

## Representing the process
To better solve the problem, we first convert RGB color space to CIELAB(LAB) color space. The LAB space consists of three channels: L for lightness, A for green-red, B for blue-yellow. The value of L ranges from 0 to 100, while other two channel range from -128 to 127. Since the grayscale image only has L channel, we can represent the process as mapping the L channel as input to the A&B channels as the output. At last, we convert the predicted LAB space back to the RGB space.

## Data

We obtain the data from Imagenet, with the category of seashore.
```
http://image-net.org/api/text/imagenet.synset.geturls?wnid=n09428293
```
Due to the limitation of the computing power of our laptop, we only downloaded 1000 images as the train set, and 100 addtional images as the validation set.


These images are not included in the archive but can be downloaded by the python script `get_dataset.py`

##
