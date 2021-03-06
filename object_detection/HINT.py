
# coding: utf-8

# # Object Detection Demo
# Welcome to the object detection inference walkthrough!  This notebook will walk you step by step through the process of using a pre-trained model to detect objects in an image. Make sure to follow the [installation instructions](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md) before you start.

## Imports

# In[1]:

import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
from copy import deepcopy
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
import cv2
# os.chdir('object_detection')
# import clarifai
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

# app = ClarifaiApp(api_key='bb5f7ed42b944db7b8cdf566b13c67a6')
app = ClarifaiApp(api_key='adfa7b13a8a24954b4199539667d1ed5')

# adfa7b13a8a24954b4199539667d1ed5



# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")
from object_detection.utils import ops as utils_ops

if tf.__version__ < '1.4.0':
	raise ImportError('Please upgrade your tensorflow installation to v1.4.* or later!')


### Env setup

# In[2]:

# This is needed to display the images.
# %matplotlib inline


# ## Object detection imports
# Here are the imports from the object detection module.

# In[3]:

from utils import label_map_util

from utils import visualization_utils as vis_util


## Model preparation 

# ## Variables
# 
# Any model exported using the `export_inference_graph.py` tool can be loaded here simply by changing `PATH_TO_CKPT` to point to a new .pb file.  
# 
# By default we use an "SSD with Mobilenet" model here. See the [detection model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) for a list of other models that can be run out-of-the-box with varying speeds and accuracies.

# In[4]:

# What model to download.
MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'
MODEL_FILE =  './object_detection/' + MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = './object_detection/' + MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('./object_detection/data', 'mscoco_label_map.pbtxt')

NUM_CLASSES = 90


### Download Model

# In[5]:

# opener = urllib.request.URLopener()
# opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
tar_file = tarfile.open(MODEL_FILE)
for file in tar_file.getmembers():
	file_name = os.path.basename(file.name)
	if 'frozen_inference_graph.pb' in file_name:
		tar_file.extract(file, os.getcwd())


### Load a (frozen) Tensorflow model into memory.

# In[6]:

detection_graph = tf.Graph()
with detection_graph.as_default():
	od_graph_def = tf.GraphDef()
	with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
		serialized_graph = fid.read()
		od_graph_def.ParseFromString(serialized_graph)
		tf.import_graph_def(od_graph_def, name='')

print("loaded model")
# ## Loading label map
# Label maps map indices to category names, so that when our convolution network predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine

# In[7]:

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


### Helper code

# In[8]:

def load_image_into_numpy_array(image):
	(im_width, im_height) = image.size
	return np.array(image.getdata()).reshape(
			(im_height, im_width, 3)).astype(np.uint8)


## Detection

# In[9]:

# For the sake of simplicity we will use only 2 images:
# image1.jpg
# image2.jpg
# If you want to test the code with your images, just add path to the images to the TEST_IMAGE_PATHS.
PATH_TO_TEST_IMAGES_DIR = 'test_images'
TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, 'image{}.jpg'.format(i)) for i in range(1, 3) ]

# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)


# In[10]:

def run_inference_for_single_image(image, graph):
	with graph.as_default():
		with tf.Session() as sess:
			# Get handles to input and output tensors
			ops = tf.get_default_graph().get_operations()
			all_tensor_names = {output.name for op in ops for output in op.outputs}
			tensor_dict = {}
			for key in [
					'num_detections', 'detection_boxes', 'detection_scores',
					'detection_classes', 'detection_masks'
			]:
				tensor_name = key + ':0'
				if tensor_name in all_tensor_names:
					tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
							tensor_name)
			if 'detection_masks' in tensor_dict:
				# The following processing is only for single image
				detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
				detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
				# Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
				real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
				detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
				detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
				detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
						detection_masks, detection_boxes, image.shape[0], image.shape[1])
				detection_masks_reframed = tf.cast(
						tf.greater(detection_masks_reframed, 0.5), tf.uint8)
				# Follow the convention by adding back the batch dimension
				tensor_dict['detection_masks'] = tf.expand_dims(
						detection_masks_reframed, 0)
			image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

			# Run inference
			output_dict = sess.run(tensor_dict,
														 feed_dict={image_tensor: np.expand_dims(image, 0)})

			# all outputs are float32 numpy arrays, so convert types as appropriate
			output_dict['num_detections'] = int(output_dict['num_detections'][0])
			output_dict['detection_classes'] = output_dict[
					'detection_classes'][0].astype(np.uint8)
			output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
			output_dict['detection_scores'] = output_dict['detection_scores'][0]
			if 'detection_masks' in output_dict:
				output_dict['detection_masks'] = output_dict['detection_masks'][0]
	return output_dict


# In[11]:

# for image_path in TEST_IMAGE_PATHS:


refsize = 500
apparel = ['person']
food_items = ['wine glass','sandwich','broccoli','banana','apple','orange','carrot','pizza','cake','donut','hotdog','cup']
print(os.getcwd())
for item in os.listdir('Objects'):
	path = os.path.join('Objects', item)
	os.remove(path)
def run(filename):
	# image = Image.open(image_path)
	# the array based representation of the image will be used later in order to prepare the
	# result image with boxes and labels on it.
	# image_np = load_image_into_numpy_array("/home/raghav/Desktop/download.jpeg")
	# Expand dimensions since the model expects images to have shape: [1, None, None, 3]
	information = []
	image_np = cv2.imread(filename)
	# image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
	refsize = min(image_np.shape[0], 500)
	image_np = cv2.resize(image_np, (image_np.shape[1]*refsize/image_np.shape[0],refsize))
	im_objs = deepcopy(image_np)
	# print(image_np.shape)
	# exit()
	shape = image_np.shape
	print(shape)
	image_np_expanded = np.expand_dims(image_np, axis=0)
	# Actual detection.
	output_dict = run_inference_for_single_image(image_np, detection_graph)
	# Visualization of the results of a detection.
	_, coordinates, labels = vis_util.visualize_boxes_and_labels_on_image_array(
			image_np,
			output_dict['detection_boxes'],
			output_dict['detection_classes'],
			output_dict['detection_scores'],
			category_index,
			instance_masks=output_dict.get('detection_masks'),
			use_normalized_coordinates=True,
			line_thickness=8)
	for i in range(len(labels)):
		ymin1 = int(coordinates[i][0] * shape[0])
		xmin1 = int(coordinates[i][1] * shape[1])
		ymax1 = int(coordinates[i][2] * shape[0])
		xmax1 = int(coordinates[i][3] * shape[1])
		# print(ymin1,ymax1,xmin1,xmax1)
		class_im = im_objs[ymin1-2:ymax1+3,xmin1-2:xmax1+3,:]
		cv2.imwrite("Objects/"+labels[i]+str(i)+".png",class_im)
		cv2.imwrite("temp.png", class_im)
		class_im = ClImage(file_obj=open("temp.png","rb"))
		classifier = -1#'general-v1.3'
		lim = 3
		print('')
		print("OBJECT "+labels[i])
		print("")
		detected = dict()
		detected['label'] = labels[i]
		detected['attr'] = []
		if(labels[i] in food_items):
			classifier = 'food-items-v1.0'
		elif(labels[i] in apparel):
			classifier = 'apparel'
			lim = 3
		if classifier != -1:
			model = app.models.get(classifier)
			description = model.predict([class_im])
			description = description['outputs']
			description = (description[0]['data'])['concepts']
		

			if labels[i] == 'sandwich' or labels[i] == 'burger':
				lim = 8
			for item in description[:lim]:
				attr = dict()
				attr['name'] = str(item['name'])
				attr['value'] = item['value']
				detected['attr'].append(attr)
				print(str(item['name'])+" "+str(item['value']))
				# information[str(item['name'])] = str(item['value'])
		if(labels[i] in food_items):
			information.append(detected)
			continue

		if(labels[i] == 'laptop' or labels[i] == 'bottle'):
			model = app.models.get('logo')
			description = model.predict([class_im])
			description = description['outputs']
			try:
				description = (description[0]['data'])['regions']
				for item in description:
					item1 = item['data']['concepts'][0]
					attr = dict()
					attr['name'] = str(item1['name'])
					attr['value'] = item1['value']
					detected['attr'].append(attr)
					print(str(item1['name'])+" "+str(item1['value']))
			except:
				print("No logo found")
			
			# information[str(item['w3c']['name'])] = str(item['value'])

		model = app.models.get('color')
		description = model.predict([class_im])
		description = description['outputs']
		description = (description[0]['data'])['colors']

		for item in description:
			attr = dict()
			colour_name = item['w3c']['name']
			ans = ""
			for i in range(len(colour_name)-1,-1,-1):
				ans = colour_name[i] + ans
				if(colour_name[i].isupper()):
					break
				
			attr['name'] = ans
			attr['value'] = item['value']
			detected['attr'].append(attr)
			print(ans+" "+str(item['value']))
			# information[str(item['w3c']['name'])] = str(item['value'])
		information.append(detected)	
	# plt.figure(figsize=IMAGE_SIZE)
	# plt.imshow(image_np)
	# plt.show()
	# os.chdir('../')
	return information


# In[11]:



