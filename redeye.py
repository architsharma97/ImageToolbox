import cv2
import numpy as np
from PIL import Image

def redeye_mask(img, mode='rgb'):
	# threshold in the rgb domain
	if mode == 'rgb':
		b,g,r = cv2.split(img)
		bg = cv2.add(b,g)
		mask  = ((r > bg) & (r > 80)).astype(np.uint8)*255

	if mode == 'hsv':
		# hsv value of red: [0, 255, 255]
		h, s, v = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2HSV))
		mask = (((h <=35) | (h>=195)) & ((s>=100) & (v>=100))).astype(np.uint8)*255

	if mode == 'rgb2':
		b,g,r = cv2.split(img.astype(np.float32))
		mask = ((r ** 2) / (b**2 + g**2 + 0.1) >= 5.0).astype(np.uint8)*255
	
	return mask

def fillHoles(mask):
	maskFloodfill = mask.copy()
	h, w = maskFloodfill.shape[:2]
	maskTemp = np.zeros((h+2, w+2), np.uint8)
	cv2.floodFill(maskFloodfill, maskTemp, (0, 0), 255)
	mask2 = cv2.bitwise_not(maskFloodfill)
	return mask2 | mask 

def fix_red_eyes(img):
	img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
	out = img.copy()

	# detect eyes, if fails, detect face and try again
	eye_classifier = cv2.CascadeClassifier('haarcascade_eye.xml')
	eyes = eye_classifier.detectMultiScale(img, 1.3, 4)
	
	if len(eyes) == 0:
		# no eyes detected, let's try faces
		print "Detecting faces!"
		face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
		faces = face_classifier.detectMultiScale(img, 1.2, 4)
		
		print "%d faces detected " %(len(faces))

		eyes = None
		for x, y, w, h in faces:
			face = img[y:y+h, x:x+w]
			if eyes is None:
				eyes = eye_classifier.detectMultiScale(face, 1.3, 5)
			else:
				eyes = np.concatenate([eyes, eye_classifier.detectMultiScale(face, 1.1, 3)], axis=0)

	if eyes is not None:
		print "%d eyes detected" %(len(eyes))

	for x, y, w, h in eyes:
		eye = img[y:y+h, x:x+w]
		b, g, r = cv2.split(eye)
		bg = cv2.add(b, g)
		mask = redeye_mask(eye)

		# fix mask for holes and dilate for completeness
		# mask = fillHoles(mask)
		mask = cv2.erode(mask, (3,3), iterations=2)
		# mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_DILATE,(5,5)))
		mask = cv2.dilate(mask, None, anchor=(-1, -1), iterations=4, borderType=1, borderValue=1)
		
		#  fix red eye: avoid texture loss
		mean = bg / 2
		# mean = np.uint8(np.ones(mean.shape) * 255)
		mean = cv2.bitwise_and(mean, mask)
		mean  = cv2.cvtColor(mean, cv2.COLOR_GRAY2BGR)
		mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

		# replace the fixed red eye in output image
		out[y:y+h, x:x+w, :] = cv2.bitwise_and(~mask, eye) + mean

	# cv2.imwrite("report/inp.jpg", img)
	# cv2.imwrite("report/out.jpg", out)

	return Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))

def main():
	img = Image.open("red_eye/i1.jpg")
	cv2.imshow('img', cv2.cvtColor(np.array(fix_red_eyes(img)), cv2.COLOR_RGB2BGR))
	cv2.waitKey(0)
	cv2.destroyAllWindows()

if __name__ == "__main__":
	main()