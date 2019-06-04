import progressbar
import argparse
import sys
import numpy as np
from os.path import realpath, dirname, basename


def count_lines(f):

	lines = 0
	with open(f) as fi:
		for l in fi:
			lines += 1

	return lines


def divide(train_file, num_classes, split_percent):

	pb = progressbar.ProgressBar(count_lines(train_file))
	dir_path = dirname(train_file)
	new_train = open(dir_path+'/new_train.txt', 'w')
	new_val = open(dir_path+'/new_validation.txt', 'w')
	num_of_videos = 0
	classes = int(num_classes)
	percentage = float(split_percent)

	with open(train_file) as tf:

		dic = {key: [] for key in map(str, np.arange(classes))}
	
		for line in tf:

			video_path = dirname(line.split()[0]).split('/')[-1]
			video_class = line.split()[-1]
			
			if video_path not in dic[video_class]:
				dic[video_class].append(video_path)

		for key in dic:
			num_of_videos += len(dic[key])

		num_of_splited_videos =  np.floor(num_of_videos/percentage)
		num_of_videos_per_class = int(np.floor(num_of_splited_videos/classes))
		
		np.random.seed(13)

		validation_videos = []

		for k in dic:
			validation_videos.extend(np.random.choice(dic[k], 
				num_of_videos_per_class, 
				replace=False))
		
	

	with open(train_file) as tf:

		for line in tf:

			full_video_path = line.split()[0]
			video_path = dirname(line.split()[0]).split('/')[-1]
			video_class = line.split()[-1]
			
			if video_path in validation_videos:
				new_val.write(full_video_path+' '+video_class+'\n')

			else:
				new_train.write(full_video_path+' '+video_class+'\n')

			pb.update()



if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument('filetrain', metavar='file_train', 
	                    help='file containing training examples')

	parser.add_argument('numclasses', metavar='number_of_classes', 
	                    help='number of classes')

	parser.add_argument('splitpercent', metavar='split_percentage', 
	                    help='percentage to split the train file')

	args = parser.parse_args()

	divide(args.filetrain, args.numclasses, args.splitpercent)