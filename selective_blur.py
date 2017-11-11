import numpy as np
import cv2
from PIL import Image

def blur(img, x1, y1, x2, y2, seg_simple=False):
	img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
	x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

	size = 15
	motionblur = np.zeros((size, size))
	motionblur[size/2, :] = np.ones(size) / size

	
	if seg_simple == True:
		mask = np.zeros(img.shape, np.uint8) + 1
		mask[min(y1, y2): max(y1,y2), min(x1, x2):max(x1, x2), :] = 0
	else:
		mask = np.zeros(img.shape[:2], np.uint8)
		bgdModel = np.zeros((1,65), np.float64)
		fgdModel = np.zeros((1,65), np.float64)
		rect = (min(x1, x2), min(y1, y2), abs(x2-x1), abs(y2-y1))

		# segmentation
		cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 1, cv2.GC_INIT_WITH_RECT)
		
		mask = np.where((mask == 2) | (mask == 0), 1, 0).astype('uint8')
		mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

	out = img * (1 - mask) + cv2.filter2D(img, -1, motionblur) * mask 

	# cv2.imwrite("report/inp.jpg", img)
	# cv2.imwrite("report/out.jpg", out)

	return Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))

def main():
	pass

if __name__ == '__main__':
	main()