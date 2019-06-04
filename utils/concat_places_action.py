import progressbar
import sys
from os.path import join, realpath, dirname, exists, basename, splitext

#path_action = '/usr/share/datasets/CIARP/best/UCF11_RGB/FC/TEST_FC_VGG16_RGB_UCF.txt'
#path_places = '/usr/share/datasets/UCF11/OptFlow/FEATURES/test_of_feats.txt'
path_action = '/usr/share/datasets/UCF11/OptFlow/FEATURES/train_action_ofl_fc2.txt'
path_places = '/usr/share/datasets/CIARP/ucf_places/train_ucf_fc2.txt'
path_feat = '/usr/share/datasets/UCF11/OptFlow/FEATURES/'
stream_file = open(path_feat+'train_action_ofl_places_fc2.txt','w')

def count_lines(f):

	lines = 0
	with open(f) as fi:
		for l in fi:
			lines += 1

	return lines


pb = progressbar.ProgressBar(count_lines(path_places))

with open(path_places) as p, open(path_action) as a:

		for line_p, line_a in zip(p,a):

			arr = line_a.split()
			img_path = arr[0]
			label = arr[1]
			
			action_features = arr[2:]
			places_features = arr[2:]
			
			stream_file.write(img_path+' '+label)

			for af in action_features:
				stream_file.write(' '+af)

			for pf in places_features:
				stream_file.write(' '+pf)

			stream_file.write('\n')				
			
			pb.update()