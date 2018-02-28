import cv2
import glob
import utils
import imutils
from colorutils import get_dominant_color

# grab the image paths from the dataset directory
image_paths = glob.glob('{}/*.jpg'.format('icons'))
image_paths = sorted(image_paths)

#init dominant color store
colors = []
#iterate over ims
for i, path in enumerate(image_paths):
	print('processing image {} of {}'.format(i, len(image_paths)))
	#read in im i
	image = cv2.imread(path)
	#get dominant color
	color = get_dominant_color(cv2.cvtColor(image, cv2.COLOR_BGR2HSV), k=3)
	#store color
	colors.append(color)

#sort colors (return list of image inds sorted)
sorted_inds = sorted(range(len(colors)), key=lambda i: colors[i])

#init montage
montage = utils.results_montage(image.shape, 10, len(image_paths))

#iter over sorted image inds
for ind in sorted_inds:
	#add image i to montage
	montage.add_result(cv2.imread(image_paths[ind]))

out = imutils.resize(montage.montage, height = 700)

cv2.imshow('sorted images', out)
cv2.waitKey(0)
cv2.imwrite('sorted_app_icons.jpg', out)