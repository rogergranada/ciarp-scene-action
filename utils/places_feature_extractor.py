import urllib2
import numpy as np
import sys
import progressbar
import argparse
import logging
from PIL import Image
from cv2 import resize
from keras.models import Model
from vgg16_places_365 import VGG16_Places365
from os.path import join, realpath, dirname, exists, basename, splitext, abspath

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def count_lines(f):

	lines = 0
	with open(f) as fi:
		for l in fi:
			lines += 1

	return lines

def write_features(feat_file, path, label, feat):

	feat_file.write(path+' '+label+' ')

	for i in feat:
		for j in i:
			feat_file.write('%s' % round(j,3))
			feat_file.write(' ')

	feat_file.write('\n')

def extractor(path_file):

	# Initializing the model
	model = VGG16_Places365(weights='places', include_top=True)
	intermediate_layer_model = Model(inputs=model.input,
	                                 outputs=model.get_layer('fc2').output)
	
	# Counting the number of lines in path_file
	pb = progressbar.ProgressBar(count_lines(path_file))

	dir_to_save = abspath(path_file).split(basename(path_file))[0]
	fc2 = dir_to_save+splitext(basename(path_file))[0]+'_fc2.txt'
	softmax = dir_to_save+splitext(basename(path_file))[0]+'_softmax.txt'

	# Creating the files
	file_fc2 = open(fc2, 'w')
	file_softmax = open(softmax, 'w')

	# Logging...
	logging.info('Saving... '+fc2)
	logging.info('Saving... '+softmax)

	with open(path_file) as f:
		for line in f:

			img_path = line.split()[0]
			label = line.split()[1]
			image = Image.open(img_path)
			image = np.array(image, dtype=np.uint8)
			image = resize(image, (224, 224))
			image = np.expand_dims(image, 0)		

			fc2_output = intermediate_layer_model.predict(image)
			softmax_output = model.predict(image)

			# Writing features into the files
			write_features(file_fc2, label, img_path, fc2_output)
			write_features(file_softmax, label, img_path, softmax_output)

			pb.update()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument('path_file', metavar='path_file', 
	                    help='file containing the path of images')

	args =  parser.parse_args()

	extractor(args.path_file)

