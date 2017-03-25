
# coding: utf-8

# # Self-Driving Car Engineer Nanodegree
# 
# ## Deep Learning
# 
# ## Project: Build a Traffic Sign Recognition Classifier
# 
# In this notebook, a template is provided for you to implement your functionality in stages, which is required to successfully complete this project. If additional code is required that cannot be included in the notebook, be sure that the Python code is successfully imported and included in your submission if necessary. 
# 
# > **Note**: Once you have completed all of the code implementations, you need to finalize your work by exporting the iPython Notebook as an HTML document. Before exporting the notebook to html, all of the code cells need to have been run so that reviewers can see the final implementation and output. You can then export the notebook by using the menu above and navigating to  \n",
#     "**File -> Download as -> HTML (.html)**. Include the finished document along with this notebook as your submission. 
# 
# In addition to implementing code, there is a writeup to complete. The writeup should be completed in a separate file, which can be either a markdown file or a pdf document. There is a [write up template](https://github.com/udacity/CarND-Traffic-Sign-Classifier-Project/blob/master/writeup_template.md) that can be used to guide the writing process. Completing the code template and writeup template will cover all of the [rubric points](https://review.udacity.com/#!/rubrics/481/view) for this project.
# 
# The [rubric](https://review.udacity.com/#!/rubrics/481/view) contains "Stand Out Suggestions" for enhancing the project beyond the minimum requirements. The stand out suggestions are optional. If you decide to pursue the "stand out suggestions", you can include the code in this Ipython notebook and also discuss the results in the writeup file.
# 
# 
# >**Note:** Code and Markdown cells can be executed using the **Shift + Enter** keyboard shortcut. In addition, Markdown cells can be edited by typically double-clicking the cell to enter edit mode.

# ---
# ## Step 0: Load The Data

# In[1]:

# Load pickled data
import pickle

# TODO: Fill this in based on where you saved the training and testing data

training_file  = './traffic-signs-data/train.p'
validation_file= './traffic-signs-data/valid.p'
testing_file   = './traffic-signs-data/test.p'
 
with open(training_file, mode='rb') as f:
    train = pickle.load(f)
with open(validation_file, mode='rb') as f:
    valid = pickle.load(f)
with open(testing_file, mode='rb') as f:
    test = pickle.load(f)
    
X_train, y_train = train['features'], train['labels']
X_valid, y_valid = valid['features'], valid['labels']
X_test,  y_test  =  test['features'],  test['labels']

assert(len(X_train) == len(y_train))
assert(len(X_valid) == len(y_valid))
assert(len(X_test)  == len(y_test))


# ---
# 
# ## Step 1: Dataset Summary & Exploration
# 
# The pickled data is a dictionary with 4 key/value pairs:
# 
# - `'features'` is a 4D array containing raw pixel data of the traffic sign images, (num examples, width, height, channels).
# - `'labels'` is a 1D array containing the label/class id of the traffic sign. The file `signnames.csv` contains id -> name mappings for each id.
# - `'sizes'` is a list containing tuples, (width, height) representing the original width and height the image.
# - `'coords'` is a list containing tuples, (x1, y1, x2, y2) representing coordinates of a bounding box around the sign in the image. **THESE COORDINATES ASSUME THE ORIGINAL IMAGE. THE PICKLED DATA CONTAINS RESIZED VERSIONS (32 by 32) OF THESE IMAGES**
# 
# Complete the basic data summary below. Use python, numpy and/or pandas methods to calculate the data summary rather than hard coding the results. For example, the [pandas shape method](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.shape.html) might be useful for calculating some of the summary results. 

# ### Provide a Basic Summary of the Data Set Using Python, Numpy and/or Pandas

# In[2]:

### Replace each question mark with the appropriate value. 
### Use python, pandas or numpy methods rather than hard coding the results
#import 

# TODO: Number of training examples
n_train = X_train.shape[0]

# TODO: Number of testing examples.
n_test = X_test.shape[0]

# TODO: What's the shape of an traffic sign image? 
image_shape = X_train.shape[1:]

# TODO: How many unique classes/labels there are in the dataset.
# read number of classes from signnames.csv
def bufcount(filename):
    #http://stackoverflow.com/a/850962/5411817
    f = open(filename)
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.read # loop optimization

    buf = read_f(buf_size)
    while buf:
        lines += buf.count('\n')
        buf = read_f(buf_size)

    return lines
# first line in datafile is classnames: ClassID, SignName 
num_classes = bufcount('./signnames.csv') - 1


print("Number of training examples =", n_train)
print("Number of testing examples =", n_test)
print("Image data shape =", image_shape)
print("Number of classes =", num_classes)


# ### Include an exploratory visualization of the dataset

# Visualize the German Traffic Signs Dataset using the pickled file(s). This is open ended, suggestions include: plotting traffic sign images, plotting the count of each sign, etc.
# 
# The [Matplotlib](http://matplotlib.org/) [examples](http://matplotlib.org/examples/index.html) and [gallery](http://matplotlib.org/gallery.html) pages are a great resource for doing visualizations in Python.
# 
# **NOTE:** It's recommended you start with something simple first. If you wish to do more, come back to it after you've completed the rest of the sections.

# In[3]:

### Data exploration visualization code goes here.
### Feel free to use as many code cells as needed.
import matplotlib.pyplot as plt

# Visualizations will be shown in the notebook.
get_ipython().magic('matplotlib inline')


# SH look at training set labels. count how many images there are of each label
import numpy as np
from collections import Counter, OrderedDict
def plot_data(data, title, short_label):
    counts = Counter(data)
    #print(counts, "\n|")
    counted = OrderedDict(sorted(counts.items()))
    #print(counted[0], counted, "\n")
    final_count = [counted[i] for i in range(len(counted))]
    #print(final, "\n")
    y_data = final_count
    x_data = range(len(y_data))
    
    
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel("traffic sign class number (0-42)\n")
    ax.set_ylabel("number of example images (relative)")
    ax.bar(x_data, y_data)#, bins=len(y_data))#, normed=True)
    #ax.hist(y_data)#, bins=len(y_data))#, normed=True)
    #spacing = np.linspace(0, len(x_data), 1)
    #ax.plot(x, 1 / np.sqrt(2*np.pi) * np.exp(-(x**2)/2), linewidth=4)
    #ax.plot(x_data, y_data, linewidth=4)
    
    ax.set_xticks([])
    ax.set_yticks([])
    fig.savefig("bar_chart_"+short_label+"_data.png", dpi=25)  # results in 160x120 px image

print("Let's see how traffic sign examples are distributed \nacross the Training, Validation, and Test sets\n")
plot_data(y_train, "Training Data: number of images in each class", "training")
plot_data(y_valid, "Validation Data: number of images in each class", "validation")
plot_data(y_test, "Test Data: number of images in each class","test")


# In[4]:

# diplay sample images from training data set
def display_images(images):
    num_channels = images[0].shape[-1]
    print("shape 1st image", images[0].shape)
    num_images = len(images)
    print(num_images, "num_images, num_channels:", num_channels)
    plt.figure(1)
    rows = 1
    cols = int(num_images/rows)
    for i in range(num_images):
        plt.subplot(rows, cols, i+1)
        if num_channels == 3:
            print("color")
            plt.imshow(images[i])
        elif num_channels == 1:
            print("grayscale")
            plt.imshow(images[i], cmap = plt.get_cmap('gray'))
        else: "error, number of channels should be 1 or 3"
    plt.show()

print("Sample images from training data set")
sample_images = [X_train[50], X_train[500], X_train[1000]]
display_images(sample_images)

# consider showing histogram of individual sample images
# consider showing average histogram of all images
# consider showing zero mean of sample images
# consider showing normalized sample images


# In[5]:

#imgplot = plt.imshow(X_train[500])


# In[6]:

#imgplot = plt.imshow(X_train[1000])

'''
#normalized_rgb   = np.zeros(image_shape, np.uint8)
#normalized_image = np.zeros(image_shape, np.uint8)
# normalized in color
def rgb_normalizer(image):
    normalized_rgb   = np.zeros(image_shape, np.uint8)
    normalized_channel = np.zeros([image_shape[0], image_shape[1], 1], np.uint8)

    r = image[:,:,0]
    g = image[:,:,1]
    b = image[:,:,2]
    print("rgb\n", r[0][0:15],"\n", g[0][0:15],"\n", b[0][0:15])
    rgb_sum = r+b+g
    rgb_mean = rgb_sum.mean() 
    r_ave = r.mean()
    g_ave = g.mean()
    b_ave = b.mean()
    if rgb_mean == 0: rgb_mean = 0.01  #avoid divide by zero for pure black image
    print("rgb_ave", rgb_mean)
    print("r_ave  ", r_ave)
    #print("rgb_sum[0]\n", rgb_sum[0][0:15])

    rgb_multiplier = np.float32(128/rgb_mean) #3*255 #128 #123*3
    #rgb_multiplier = np.float32(3*128/rgb_mean) #3*255 #128 #123*3
    print("rgb_mul ", rgb_multiplier)
    
    channels = [r, g, b]
    print("normalized")
    for channel in range(len(channels)):
        channel_multiplier = rgb_multiplier
        #channel_multiplier = np.float32(128/channels[channel].mean()) #rgb_multiplier
        #channel_multiplier = (128/rgb_multiplier + channel_multiplier)/2
        normalized_channel = np.rint(np.float32(channel_multiplier * channels[channel])).astype(int)
        print(normalized_channel[0][0:15])       
        normalized_rgb[0:,0:,channel] = normalized_channel
    print()
    return normalized_rgb

sample_images = [X_train[1000], X_train[500], X_train[50]]
#image_1000 = X_train[1000]
#normalized_rgb = rgb_normalizer(image_1000)
#imgplot = plt.imshow(normalized_rgb)

plt.figure(1)
num_images = len(sample_images)
for i in range(num_images):
    #sample_image = sample_images[i]
    #normalized_rgb = rgb_normalizer(sample_image)
    plt.subplot(num_images, 2, 2*i+1)
    plt.imshow(sample_images[i])
    plt.subplot(num_images, 2, 2*i+2)
    plt.imshow(rgb_normalizer(sample_images[i]))
'''
'''
image = X_train[50]
normalized_rgb = rgb_normalizer(image)
plt.subplot(223)
plt.imshow(image)
plt.subplot(224)
plt.imshow(normalized_rgb)
'''
'''
plt.show()
''''''
def rgb_grayscale_combo(color_image, bw):
    combo_image   = np.zeros(image_shape, np.uint8)
    combo_channel = np.zeros(image_shape, np.uint8)

    r = color_image[:,:,0]
    g = color_image[:,:,1]
    b = color_image[:,:,2]
    #print("rgb\n", r[0][0:15],"\n", g[0][0:15],"\n", b[0][0:15])
    #rgb_sum = np.float32(r+b+g+.1)
    rgb_sum = np.float32(r) + np.float32(b) + np.float32(g) +.1
    ##print("rgb_sum\n", rgb_sum[0][0:15])
    #if rgb_sum == 0: rgb_sum = 0.01  #avoid divide by zero for pure black pixel
    ##print("bw\n",bw[0][0:15])
    rgb_mean = rgb_sum.mean() 
    r_ave = r.mean()
    g_ave = g.mean()
    b_ave = b.mean()
    channels_ave = [r_ave, g_ave, b_ave]
    if rgb_mean == 0: rgb_mean = 0.01  #avoid divide by zero for pure black image
    print("rgb_ave", rgb_mean)
    print("r_ave  ", r_ave)
    #print("rgb_sum[0]\n", rgb_sum[0][0:15])

    rgb_multiplier = np.float32(128/rgb_mean) #3*255 #128 #123*3
    #rgb_multiplier = np.float32(3*128/rgb_mean) #3*255 #128 #123*3
    #print("rgb_mul ", rgb_multiplier)
    
    channels = [r, g, b]
    print("combo")
    for channel in range(len(channels)):
        #channel_multiplier = rgb_sum /(255 * bw)
        ##channel_multiplier = channels_ave[channel]  / (128 * bw)
        ##print("channel_multiplier", channel_multiplier[0][0:15])
        #channel_multiplier = np.float32(128/channels[channel].mean()) #rgb_multiplier
        #channel_multiplier = (128/rgb_multiplier + channel_multiplier)/2
        ##combo_channel = np.rint(np.float32(channel_multiplier * channels[channel])).astype(int)
        
        #channel_value = (bw) * 255 * ((3*128.0/rgb_mean) - (rgb_sum-channels[channel])/rgb_sum)  ##/ (128 * bw)
        #channel_value = 255*(bw) * ((128.0)/rgb_mean) * (1-(rgb_sum-channels[channel])/rgb_sum)  ##/ (128 * bw)
        channel_value = 255*(bw) * ((128.0)/rgb_mean) * (1-(rgb_sum/rgb_mean-channels[channel]/channels_ave[channel])/(rgb_sum/rgb_mean))  ##/ (128 * bw)
        #channel_value = 255*(bw) * 3*(np.float32(channels[channel])/np.float32(rgb_sum))  ##/ (128 * bw)
        combo_channel = np.rint(np.float32(channel_value)).astype(int)
        
        #print(combo_channel[0][0:15]) 
        combo_image[0:,0:,channel] = combo_channel
        #print("diff\n", (color_image[18:18][10:15]-combo_image[18:18][10:15])[:])
    print()
    return combo_image

plt.figure(2)
sample_images = [X_train[1000], X_train[500], X_train[50]]
num_images = len(sample_images)
bw_images = []
for i in range(num_images):
    bw_images.append(color.rgb2gray(sample_images[i]))
for i in range(num_images):
    #sample_image = sample_images[i]
    #normalized_rgb = rgb_normalizer(sample_image)
    plt.subplot(num_images, 2, 2*i+1)
    plt.imshow(sample_images[i])
    plt.subplot(num_images, 2, 2*i+2)
    plt.imshow(rgb_grayscale_combo(sample_images[i], bw_images[i]))
plt.show()
'''
# In[ ]:




# In[7]:

#print("normlizing as rgb")
#for i in ranage(len(X_train)):
#    rgb_normalizer(X_train[i])

'''
from skimage import color
gray_img1000 = color.rgb2gray(X_train[1000])
#imgplot = plt.imshow(gray_img1000)
print("grayscale image")
imgplot= plt.imshow(gray_img1000, cmap = plt.get_cmap('gray'))
print("converting validation data to grayscale")
gray_valid = color.rgb2gray(X_valid)
print("converting training data to grayscale")
gray_train = color.rgb2gray(X_train)
print("converting training data to grayscale")
gray_test = color.rgb2gray(X_test)
print("done converting to grayscale")
''''''
from sklearn.preprocessing import normalize
print("normalized grayscale image")
fig = plt.figure(1)
plt.subplot(1, 2, 1)
normalized_gray_image1000 = normalize(X_train[500,:,:,2])#(gray_img1000)
plt.imshow(normalized_gray_image1000, cmap = plt.get_cmap('gray'))
#im2 = fig.add_subplot()
#im2=plt.imshow(normalized_gray_image1000, cmap = plt.get_cmap('gray'))
print("normalizing grayscale validation images")
norm_gray_valid = color.rgb2gray(normalize(X_valid[:,:,:]))
print("normalizing grayscale training images")
norm_gray_train = color.rgb2gray(normalize(X_train[:,:,:]))
print("normalizing grayscale test images")
norm_gray_test = color.rgb2gray(gray_test)


print("creating 3channel version of normalized grayscale image")
gray_rgb_normalized_train = np.zeros(X_train.shape, np.uint8)
gray_rgb_normalized_valid = np.zeros(X_valid.shape, np.uint8)
gray_rgb_normalized_test  = np.zeros(X_test.shape,  np.uint8)
print( [3 *4])

#gray_rgb_normalized_train[:,:,:,0] = gray_rgb_normalized_train[:,:,:,1] = gray_rgb_normalized_train[:,:,:,2] = norm_gray_train
gray_rgb_normalized_train[:,:,:,[norm_gray_train,norm_gray_train,norm_gray_train]] 
print(gray_valid.shape, norm_gray_valid.shape)
gray_rgb_normalized_valid[:,:,:,0] = gray_rgb_normalized_valid[:,:,:,1] = gray_rgb_normalized_valid[:,:,:,2] = norm_gray_valid
#gray_rgb_normalized_test[i][:,:,0]  = gray_rgb_normalized_test[i][:,:,1]  = gray_rgb_normalized_test[i][:,:,2]  = norm_gray_test

plt.subplot(1,2,2)
plt.imshow(gray_rgb_normalized_test[500])
''''''
from sklearn.preprocessing import normalize
# zero center the data
# subtract the mean of TRAINING DATA from each of the train, valid, test sets
X_train = X_train.astype(np.float32)
X_valid = X_valid.astype(np.float32)
#X_test  = X_test.astype(np.float32)
training_data_mean = np.mean(X_train, axis=0)
print(training_data_mean.shape, training_data_mean)
X_train -= training_data_mean
X_valid -= training_data_mean
X_test  -= training_data_mean

# display
sample_images=[X_train[50], X_train[500], X_train[1000]]
display_images(sample_images)
print(sample_images[0][16][16][0:5])
'''
# In[11]:

from sklearn.preprocessing import normalize
def separate_channels(images):
    # returns 2-D array
    R = images[:,:,:,0].reshape(len(images),-1)
    G = images[:,:,:,1].reshape(len(images),-1)
    B = images[:,:,:,2].reshape(len(images),-1)
    return [R,G,B]

def combine_channels(R,G,B):
    # returns 4-D array
    R =  R.reshape(-1, 32, 32, 1)
    G =  G.reshape(-1, 32, 32, 1)
    B =  B.reshape(-1, 32, 32, 1)
    rgb = []
    return rgb

R, G, B = separate_channels(X_train)
r_norm = normalize(R)
print("normalized R")
g_norm = normalize(G)
print("normalized G")
b_norm = normalize(B)
print("normalized B")
R = r_norm.reshape(-1,32,32,1)
print(R)
G = g_norm.reshape(-1,32,32,1)
B = b_norm.reshape(-1,32,32,1)
print(R.shape)
X_train[:,:,:,0] = R[:,:,:,0]
X_train[:,:,:,1] = G[:,:,:,0]
X_train[:,:,:,2] = B[:,:,:,0]
#display_images([X_train[50]])#, G[500], B[1000]])
print(X_train[500][16][:][:])


# ----
# 
# ## Step 2: Design and Test a Model Architecture
# 
# Design and implement a deep learning model that learns to recognize traffic signs. Train and test your model on the [German Traffic Sign Dataset](http://benchmark.ini.rub.de/?section=gtsrb&subsection=dataset).
# 
# The LeNet-5 implementation shown in the [classroom](https://classroom.udacity.com/nanodegrees/nd013/parts/fbf77062-5703-404e-b60c-95b78b2f3f9e/modules/6df7ae49-c61c-4bb2-a23e-6527e69209ec/lessons/601ae704-1035-4287-8b11-e2c2716217ad/concepts/d4aca031-508f-4e0b-b493-e7b706120f81) at the end of the CNN lesson is a solid starting point. You'll have to change the number of classes and possibly the preprocessing, but aside from that it's plug and play! 
# 
# With the LeNet-5 solution from the lecture, you should expect a validation set accuracy of about 0.89. To meet specifications, the validation set accuracy will need to be at least 0.93. It is possible to get an even higher accuracy, but 0.93 is the minimum for a successful project submission. 
# 
# There are various aspects to consider when thinking about this problem:
# 
# - Neural network architecture (is the network over or underfitting?)
# - Play around preprocessing techniques (normalization, rgb to grayscale, etc)
# - Number of examples per label (some have more than others).
# - Generate fake data.
# 
# Here is an example of a [published baseline model on this problem](http://yann.lecun.com/exdb/publis/pdf/sermanet-ijcnn-11.pdf). It's not required to be familiar with the approach used in the paper but, it's good practice to try to read papers like these.

# ### Pre-process the Data Set (normalization, grayscale, etc.)

# Use the code cell (or multiple code cells, if necessary) to implement the first step of your project.

# In[ ]:

### Preprocess the data here. Preprocessing steps could include normalization, converting to grayscae, etc.
### Feel free to use as many code cells as needed.

from sklearn.utils import shuffle
from sklearn.preprocessing import normalize
from skimage import color
import tensorflow as tf

# images are already sized properly for leNet at (32x32)
print(image_shape, image_shape[1:])
assert (image_shape == [32, 32, 3])  #32px x 32px, 3 color channels:RGB
          
# shuffle data
X_train, y_train = shuffle(X_train, y_train)
X_valid, y_valid = shuffle(X_valid, y_valid)
    # don't need to shuffle test data

''' 
# normalization
print("normalizing")
#for i in range(len(X_train))
#X_train=[(i, tf.image.per_image_standardization(X_train[i])) for i in range(len(X_train))] 
#list(map(lambda x: x**2, range(10)))
#tf.image.per_image_standardization(X_valid)
#tf.image.per_image_standardization(X_test)
##X_valid=[(i, tf.image.per_image_standardization(X_valid[i])) for i in range(len(X_valid))] 
#X_test=[(i, tf.image.per_image_standardization(X_test[i]))  for i in range(len(X_test))]
#X_valid = N_valid

X_train_preprocessed = normalized(X_train)
X_valid_preprocessed = normalized(X_valid)
X_test_preprocessed  = normalized(X_test)

print("normalized image:")
x_1000_normalized = normalize(X_train_preprocessed[1000])
imgplot = plt.imshow(x_1000_normalized)

# to grayscale
#Gray Scale you could use cvtcolor from OpenCV:
#gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

print("to grayscale")
X_train_preprocessed = color.rgb2gray(X_train_preprocessed)
X_valid_preprocessed = color.rgb2gray(X_valid_preprocessed)
X_test_preprocessed  = color.rgb2gray(X_test_preprocessed)
print("grayscale done")
#imgplot = plt.imshow(X_train[1000], cmap="gray")
image_shape = X_train_preprocessed.get_shape().as_list()[1:]
print(image_shape)
assert (image_shape == [32, 32, 1])  #32px x 32px, 1 color channel: grayscale
'''

# define training variables, constants
EPOCHS = 100
BATCH_SIZE = 128

mu = 0
sigma = 0.1  # or try .01, or ..
training_rate = 0.01

def filter_size(in_size, out_size, stride):
    assert(padding == "VALID")
    return (in_size+1) - (out_size*stride)

padding = "VALID"
stride = 1
strides = [1, stride, stride, 1]
pool_stride = 2
pool_strides = [1, pool_stride, pool_stride, 1]
ksize = pool_strides
print("finished cell")




# ### Model Architecture
### Define your architecture here.
### Feel free to use as many code cells as needed.

"""
# Layer 1: Convolutional, Activation, Pooling: (32,32,3) --> (28,28,6?) --> (14,14,?6)
# Convolution (32,32,3) --> (28,28,6?)
input_height,  input_width,  input_depth  = x.get_shape()[1:]
output_height, output_width, output_depth = (28, 28, 6)

weights_height = filter_size(input_height, output_height, stride)
weights_width  = filter_size(input_width,  output_width,  stride)
weights_shape  = [filter_height, filter_width, input_depth, output_depth]
bias_shape     = [output_depth]

# initialize weights
filter_weights = tf.Variable(tf.truncated_normal(weights_shape, mean=mu, stddev=sigma))
filter_bias    = tf.Variable(tf.zeros(bias_shape))

layer1 = tf.nn.conv2d(x, filter_weights, strides, padding) + filter_bias

print("\nlayer1 conv: 28x28x6 =?=", layer1.get_shape()[3])
assert( [28, 28, 6] == layer1.get_shape().as_list()[1:])

# Activation
layer1 = tf.nn.relu(layer1)

# Pooling (28,28,6?) --> (14,14,?6)
input_height,  input_width,  input_depth  = layer1.get_shape()[1:]
output_height, output_width, output_depth = (14, 14, input_depth)

ksize = [1, 2, 2, 1]
pool_strides = ksize
layer1 = tf.nn.max_pool(layer1, ksize, pool_strides, padding)
print("layer1 pool: 14x14x6 =?=", layer1.get_shape())
assert( [14, 14, 6] == layer1.get_shape().as_list()[1:])
"""
# could define those calcs as functions, that simply passes in 
  # old layer, new layer size. Returns params for weights and bias shape
    # then only need to init new weights, bias, call conv, activation and pooling
    # but code is already written, so just as easy to simply copy paste
    # swapping out those couple variables that I'd have otherwise passed in.
    # if did 3 Convolutional layers, No Hesitation. Right now, it's a draw.
    
"""
# Layer 2: Convolutional, Activation, Pooling: (14,14,) -- > ()
# Convolution (32,32,3) --> (28,28,6?)
input_height,  input_width,  input_depth  = layer1.get_shape()[1:]
output_height, output_width, output_depth = (10, 10, 16)

weights_height = filter_size(input_height, output_height, stride)
weights_width  = filter_size(input_width,  output_width,  stride)
weights_shape  = [filter_height, filter_width, input_depth, output_depth]
bias_shape     = [output_depth]  # == weights_shape[-1]

# initialize weights
filter_weights = tf.Variable(tf.truncated_normal(weights_shape, mean=mu, stddev=sigma))
filter_bias    = tf.Variable(tf.zeros(bias_shape))

layer2 = tf.nn.conv2d(layer1, filter_weights, strides, padding) + filter_bias

print("\nlayer1 conv: 28x28x6 =?=", layer1.get_shape()[3])
assert( [10, 10, 16] == layer1.get_shape().as_list()[1:])

# Activation
layer2 = tf.nn.relu(layer1)

# Pooling (10, 10, 16) --> (5, 5, 16)
input_height,  input_width,  input_depth  = layer1.get_shape()[1:]
output_height, output_width, output_depth = (5, 5, input_depth)

#ksize = [1, 2, 2, 1]
#pool_strides = ksize
layer2 = tf.nn.max_pool(layer2, ksize, pool_strides, padding)
print("layer2 pool: (5, 5, 16)) =?=", layer2.get_shape())
assert( [5, 5, 16] == layer2.get_shape().as_list()[1:])
"""
"""
# Flatten: 
# from tensorflow.contrib.layers import flatten
flattened_23 = tf.contrib.layers.flatten(layer2)
""""""
# Layer 3: Fully Connected
input_height = flattened_23.get_shape().as_list()[1]  # ==? len(flattened_23 ?)
output_height = 120
weights_shape = [input_height, output_height]
bias_shape    = [output_height]

fcc_weights = tf.Variable(tf.truncated_normal(weights_shape, mean=mu, stddev=sigma)
fcc_bias    = tf.Variable(tf.zeros(bias_shape))

layer3 = tf.add(tf.matmul(flattened_23, fcc_weights), fcc_bias)
layer3 = tf.nn.relu(layer3)
assert( [int(layer3.get_shape()[1]) ] == [120])
""""""
# Layer 4: Fully Connected
input_height = layer3.get_shape().as_list()[1]  # ==? len(layer3 ?)
output_height = 84
weights_shape = [input_height, output_height]
bias_shape    = [output_height]

fcc_weights = tf.Variable(tf.truncated_normal(weights_shape), mean=mu, stddev=sigma)
fcc_bias    = tf.Variable(tf.zeros(bias_shape))

layer4 = tf.add(tf.matmul(layer3, fcc_weights), fcc_bias)
layer4 = tf.nn.relu(layer4)
assert( [int(layer3.get_shape()[1]) ] == [84])
"""'''
# Layer 5: Fully Connected
input_height = layer4.get_shape().as_list()[1]  # ==? len(layer3 ?)
output_height = num_classes
weights_shape = [input_height, output_height]
bias_shape    = [output_height]

fcc_weights = tf.Variable(tf.truncated_normal(weights_shape, mean=mu, stddev=sigma)
fcc_bias    = tf.Variable(tf.zeros(bias_shape))

logits = tf.add(tf.matmul(layer4, fcc_weights), fcc_bias)
assert( [int(logits.get_shape()[1]) ] == [num_classes])
'''

# In[ ]:

def get_conv_layer(x, conv_output_shape, pool_output_shape):
    input_height,  input_width,  input_depth  = x.get_shape().as_list()[1:]
    output_height, output_width, output_depth = conv_output_shape  #(28, 28, 6)

    filter_height = filter_size(input_height, output_height, stride)
    filter_width  = filter_size(input_width,  output_width,  stride)
    weights_shape  = [filter_height, filter_width, input_depth, output_depth]
    bias_shape     = [output_depth]

    # initialize weights
    filter_weights = tf.Variable(tf.truncated_normal(weights_shape, mean=mu, stddev=sigma))
    filter_bias    = tf.Variable(tf.zeros(bias_shape))

    layer1 = tf.nn.conv2d(x, filter_weights, strides, padding) + filter_bias

    #print(conv_output_shape, "=?=", layer1.get_shape().as_list()[1:])
    assert( conv_output_shape == layer1.get_shape().as_list()[1:])

    # Activation
    layer1 = tf.nn.relu(layer1)

    # Pooling (28,28,6?) --> (14,14,?6)
    input_height,  input_width,  input_depth  = layer1.get_shape()[1:]
    output_height, output_width, output_depth = pool_output_shape #(14, 14, input_depth)

    ksize = [1, 2, 2, 1]
    pool_strides = ksize
    layer1 = tf.nn.max_pool(layer1, ksize, pool_strides, padding)
    #print( pool_output_shape, "=?=", layer1.get_shape().as_list()[1:] )
    assert( pool_output_shape == layer1.get_shape().as_list()[1:] )

    return layer1



# In[ ]:

def get_fcc_layer(prev_layer, output_length):
    input_length  = prev_layer.get_shape().as_list()[1]
    weights_shape = [input_length, output_length]
    bias_shape    = [output_length]
    #print(weights_shape, bias_shape, "get_fcc_layer: input_shape, output_shape")

    fcc_weights = tf.Variable(tf.truncated_normal(weights_shape, mean=mu, stddev=sigma))
    fcc_bias    = tf.Variable(tf.zeros(bias_shape))

    fcc_layer = tf.add(tf.matmul(prev_layer, fcc_weights), fcc_bias)
    #fcc_layer = tf.nn.relu(fcc_layer)
    #print(output_length, "=?=", fcc_layer.get_shape()[1])
    assert([output_length] == fcc_layer.get_shape().as_list()[1:])

    return fcc_layer


# In[ ]:

from tensorflow.contrib.layers import flatten

def LeNet(x):
    layer1 = get_conv_layer(x, [28,28,6], [14,14,6])
    layer2 = get_conv_layer(layer1, [10,10,16], [5,5,16])
    
    flattened = tf.contrib.layers.flatten(layer2)
    
    layer3 = get_fcc_layer(flattened, 120)
    layer3 = tf.nn.relu(layer3)

    layer4 = get_fcc_layer(layer3, 84)
    layer4 = tf.nn.relu(layer4)
    # maybe try dropout layer
    
    logits = get_fcc_layer(layer4, num_classes)
    assert( [logits.get_shape().as_list()[1] ] == [num_classes])

    
    return logits


# ### Train, Validate and Test the Model

# A validation set can be used to assess how well the model is performing. A low accuracy on the training and validation
# sets imply underfitting. A high accuracy on the training set but low accuracy on the validation set implies overfitting.

# In[ ]:

### Train your model here.
### Calculate and report the accuracy on the training and validation set.
### Once a final model architecture is selected, 
### the accuracy on the test set should be calculated and reported as well.
### Feel free to use as many code cells as needed.


# In[ ]:

'''   http://stackoverflow.com/a/34243720/5411817
#   use this function instead of separate functions:
#   1) softmax with 2) cross_entropy and 3)(sparce) includes one-hot
#   softmax_cross_entropy_with_logits is more numerically stable/
#       accurate than running two steps of softmax, then cross_entropy
#   using the sparse_.. saves a step by not having to convert labels
#       to one-hot first
'''
# initialize
pixels_x, pixels_y, color_depth = image_shape 
assert ((pixels_x, pixels_y, color_depth) == (32, 32, 3))

# choose which pre-processed set to work with
X_train = norm_gray_valid
X_valid = norm_gray_valid
X_test  = norm_gray_valid
#y_train = y_train
#y_valid =
#y_test  = 
image_shape = x_train.shape()

# features, labels
x = tf.placeholder(tf.float32, (None, pixels_x, pixels_y, color_depth))
y = tf.placeholder(tf.int64, (None))


# run leNet
learning_rate = .001
logits = LeNet(x)

# loss
cross_entropy  = tf.nn.sparse_softmax_cross_entropy_with_logits(logits, y)#labels)
loss_operation = tf.reduce_mean(cross_entropy)

# train
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
training_operation = optimizer.minimize(loss_operation)

# accuracy
model_prediction = tf.argmax(logits, 1)
prediction_is_correct = tf.equal(model_prediction, y)#labels)
accuracy_calculation   = tf.reduce_mean(tf.cast(prediction_is_correct, tf.float32))


# In[ ]:




# In[ ]:

# evaluation routine
def evaluate_data(X_data, y_data):
    print("evaluating..")
    sess = tf.get_default_session()
    total_loss = 0
    total_accuracy = 0
    
    num_samples = len(X_data)
    for batch_start in range(0, num_samples, BATCH_SIZE):
        batch_end = batch_start + BATCH_SIZE
        X_batch = X_data[batch_start:batch_end]
        y_batch = y_data[batch_start:batch_end]
        
        accuracy, loss = sess.run([accuracy_calculation, loss_operation],
                                  feed_dict = {x:X_batch, y:y_batch})
        
        this_batch_size = len(X_batch)
        
        total_accuracy += this_batch_size * accuracy
        total_loss     += this_batch_size * loss
        
    total_accuracy = total_accuracy / num_samples
    total_loss = total_loss / num_samples
        
    return total_accuracy, total_loss     


# In[ ]:

# TEMP TRUNCATE DATA FOR INITIAL TESTING
'''
tr = int(BATCH_SIZE * 1.2)
va = te = int(tr * 0.2)
print(tr, va, te, "total:", (tr+va+te), "percent training: ", tr/(tr+va+te))
X_train = X_train[0:tr]
y_train = y_train[0:tr]
X_valid = X_valid[0:va]
y_valid = y_valid[0:va]
X_test  = X_test[0:te]
y_test  = y_test[0:te]
print('DATA TRUNCATED TO:', len(X_train), "SAMPLES for preliminary testing")
'''

EPOCHS = 30
print('EPOCHS TRUNCATED TO:', EPOCHS, "EPOCHS for preliminary testing")


# In[ ]:

import time

# train our model
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    num_examples = len(X_train)
    
    print("Training...\n")
    for i in range(EPOCHS):
        print("EPOCH: ", i+1, "of", EPOCHS, "EPOCHS")
        X_train, y_train = shuffle(X_train, y_train)
        t0 = time.time()
        for batch_start in range(0, num_examples, BATCH_SIZE):
            batch_end = batch_start + BATCH_SIZE
            features = X_train[batch_start:batch_end]
            labels   = y_train[batch_start:batch_end]
            #train
            sess.run(training_operation, feed_dict = {x:features, y:labels})
            if batch_start % 100 == 0:
                print("        batch ", 1+batch_start//BATCH_SIZE, "of ", 1 + int(num_examples/BATCH_SIZE))#, "batches,  on EPOCH", i+1, "of", EPOCHS, "EPOCHS")
                      
        # evaluate on validation set, and print results of model from this EPOCH       
        validation_accuracy, loss_accuracy = evaluate_data(X_valid, y_valid)

        #print("EPOCH {} ...".format(i+1))
        print("Time: {:.3f} minutes".format(float( (time.time()-t0) / 60 )))
        print("Validation Loss = {:.3f}".format(loss_accuracy))
        print("Validation Accuracy = {:.3f}".format(validation_accuracy))
        print()    
        
    print("underfitting if:  low accuracy on training and low accuracy on validation sets.")
    print("overfitting  if: high accuracy on training but low accuracy on validation sets.")
    print()
    if validation_accuracy >= 0.93:
        print(" !! Congratulations!! Your model meets the minimum required validation Accuracy of 0.93")
        print("   You may now run your model on the Test Set :-)")
    else:
        print("Keep working on your model to acheive a minimum validation accuracy of 0.93")
    print()

    # save trained model
    saver = tf.train.Saver()
    saver.save(sess, './sh_trained_traffic_sign_classifier')
    print("Model Saved")


# In[ ]:




# In[ ]:

# test the trained model
with tf.Session() as sess:
    saver.restore(sess, tf.train.latest_checkpoint('.'))

    test_accuracy, test_loss = evaluate_data(X_test, y_test)
    print(test_accuracy)
    print("Test Loss     = {:.3f}".format(test_loss))
    print("Test Accuracy = {:.3f}".format(test_accuracy))
    


# ---
# 
# ## Step 3: Test a Model on New Images
# 
# To give yourself more insight into how your model is working, download at least five pictures of German traffic signs from the web and use your model to predict the traffic sign type.
# 
# You may find `signnames.csv` useful as it contains mappings from the class id (integer) to the actual sign name.

# ### Load and Output the Images

# In[ ]:

### Load the images and plot them here.
### Feel free to use as many code cells as needed.


# ### Predict the Sign Type for Each Image

# In[ ]:

### Run the predictions here and use the model to output the prediction for each image.
### Make sure to pre-process the images with the same pre-processing pipeline used earlier.
### Feel free to use as many code cells as needed.


# ### Analyze Performance

# In[ ]:

### Calculate the accuracy for these 5 new images. 
### For example, if the model predicted 1 out of 5 signs correctly, it's 20% accurate on these new images.


# ### Output Top 5 Softmax Probabilities For Each Image Found on the Web

# For each of the new images, print out the model's softmax probabilities to show the **certainty** of the model's predictions (limit the output to the top 5 probabilities for each image). [`tf.nn.top_k`](https://www.tensorflow.org/versions/r0.12/api_docs/python/nn.html#top_k) could prove helpful here. 
# 
# The example below demonstrates how tf.nn.top_k can be used to find the top k predictions for each image.
# 
# `tf.nn.top_k` will return the values and indices (class ids) of the top k predictions. So if k=3, for each sign, it'll return the 3 largest probabilities (out of a possible 43) and the correspoding class ids.
# 
# Take this numpy array as an example. The values in the array represent predictions. The array contains softmax probabilities for five candidate images with six possible classes. `tk.nn.top_k` is used to choose the three classes with the highest probability:
# 
# ```
# # (5, 6) array
# a = np.array([[ 0.24879643,  0.07032244,  0.12641572,  0.34763842,  0.07893497,
#          0.12789202],
#        [ 0.28086119,  0.27569815,  0.08594638,  0.0178669 ,  0.18063401,
#          0.15899337],
#        [ 0.26076848,  0.23664738,  0.08020603,  0.07001922,  0.1134371 ,
#          0.23892179],
#        [ 0.11943333,  0.29198961,  0.02605103,  0.26234032,  0.1351348 ,
#          0.16505091],
#        [ 0.09561176,  0.34396535,  0.0643941 ,  0.16240774,  0.24206137,
#          0.09155967]])
# ```
# 
# Running it through `sess.run(tf.nn.top_k(tf.constant(a), k=3))` produces:
# 
# ```
# TopKV2(values=array([[ 0.34763842,  0.24879643,  0.12789202],
#        [ 0.28086119,  0.27569815,  0.18063401],
#        [ 0.26076848,  0.23892179,  0.23664738],
#        [ 0.29198961,  0.26234032,  0.16505091],
#        [ 0.34396535,  0.24206137,  0.16240774]]), indices=array([[3, 0, 5],
#        [0, 1, 4],
#        [0, 5, 1],
#        [1, 3, 5],
#        [1, 4, 3]], dtype=int32))
# ```
# 
# Looking just at the first row we get `[ 0.34763842,  0.24879643,  0.12789202]`, you can confirm these are the 3 largest probabilities in `a`. You'll also notice `[3, 0, 5]` are the corresponding indices.

# In[ ]:

### Print out the top five softmax probabilities for the predictions on the German traffic sign images found on the web. 
### Feel free to use as many code cells as needed.


# ---
# 
# ## Step 4: Visualize the Neural Network's State with Test Images
# 
#  This Section is not required to complete but acts as an additional excersise for understaning the output of a neural network's weights. While neural networks can be a great learning device they are often referred to as a black box. We can understand what the weights of a neural network look like better by plotting their feature maps. After successfully training your neural network you can see what it's feature maps look like by plotting the output of the network's weight layers in response to a test stimuli image. From these plotted feature maps, it's possible to see what characteristics of an image the network finds interesting. For a sign, maybe the inner network feature maps react with high activation to the sign's boundary outline or to the contrast in the sign's painted symbol.
# 
#  Provided for you below is the function code that allows you to get the visualization output of any tensorflow weight layer you want. The inputs to the function should be a stimuli image, one used during training or a new one you provided, and then the tensorflow variable name that represents the layer's state during the training process, for instance if you wanted to see what the [LeNet lab's](https://classroom.udacity.com/nanodegrees/nd013/parts/fbf77062-5703-404e-b60c-95b78b2f3f9e/modules/6df7ae49-c61c-4bb2-a23e-6527e69209ec/lessons/601ae704-1035-4287-8b11-e2c2716217ad/concepts/d4aca031-508f-4e0b-b493-e7b706120f81) feature maps looked like for it's second convolutional layer you could enter conv2 as the tf_activation variable.
# 
# For an example of what feature map outputs look like, check out NVIDIA's results in their paper [End-to-End Deep Learning for Self-Driving Cars](https://devblogs.nvidia.com/parallelforall/deep-learning-self-driving-cars/) in the section Visualization of internal CNN State. NVIDIA was able to show that their network's inner weights had high activations to road boundary lines by comparing feature maps from an image with a clear path to one without. Try experimenting with a similar test to show that your trained network's weights are looking for interesting features, whether it's looking at differences in feature maps from images with or without a sign, or even what feature maps look like in a trained network vs a completely untrained one on the same sign image.
# 
# <figure>
#  <img src="visualize_cnn.png" width="380" alt="Combined Image" />
#  <figcaption>
#  <p></p> 
#  <p style="text-align: center;"> Your output should look something like this (above)</p> 
#  </figcaption>
# </figure>
#  <p></p> 
# 

# In[ ]:

### Visualize your network's feature maps here.
### Feel free to use as many code cells as needed.

# image_input: the test image being fed into the network to produce the feature maps
# tf_activation: should be a tf variable name used during your training procedure that represents the calculated state of a specific weight layer
# activation_min/max: can be used to view the activation contrast in more detail, by default matplot sets min and max to the actual min and max values of the output
# plt_num: used to plot out multiple different weight feature map sets on the same block, just extend the plt number for each new feature map entry

def outputFeatureMap(image_input, tf_activation, activation_min=-1, activation_max=-1 ,plt_num=1):
    # Here make sure to preprocess your image_input in a way your network expects
    # with size, normalization, ect if needed
    # image_input =
    # Note: x should be the same name as your network's tensorflow data placeholder variable
    # If you get an error tf_activation is not defined it maybe having trouble accessing the variable from inside a function
    activation = tf_activation.eval(session=sess,feed_dict={x : image_input})
    featuremaps = activation.shape[3]
    plt.figure(plt_num, figsize=(15,15))
    for featuremap in range(featuremaps):
        plt.subplot(6,8, featuremap+1) # sets the number of feature maps to show on each row and column
        plt.title('FeatureMap ' + str(featuremap)) # displays the feature map number
        if activation_min != -1 & activation_max != -1:
            plt.imshow(activation[0,:,:, featuremap], interpolation="nearest", vmin =activation_min, vmax=activation_max, cmap="gray")
        elif activation_max != -1:
            plt.imshow(activation[0,:,:, featuremap], interpolation="nearest", vmax=activation_max, cmap="gray")
        elif activation_min !=-1:
            plt.imshow(activation[0,:,:, featuremap], interpolation="nearest", vmin=activation_min, cmap="gray")
        else:
            plt.imshow(activation[0,:,:, featuremap], interpolation="nearest", cmap="gray")


# ### Question 9
# 
# Discuss how you used the visual output of your trained network's feature maps to show that it had learned to look for interesting characteristics in traffic sign images
# 

# **Answer:**

# > **Note**: Once you have completed all of the code implementations and successfully answered each question above, you may finalize your work by exporting the iPython Notebook as an HTML document. You can do this by using the menu above and navigating to  \n",
#     "**File -> Download as -> HTML (.html)**. Include the finished document along with this notebook as your submission.

# ### Project Writeup
# 
# Once you have completed the code implementation, document your results in a project writeup using this [template](https://github.com/udacity/CarND-Traffic-Sign-Classifier-Project/blob/master/writeup_template.md) as a guide. The writeup can be in a markdown or pdf file. 
