import numpy as np
import cv2

# 提取图像的3D HSV颜色直方图
class FeatureDescriptor:
	def __init__(self, bins):
		# 存放直方图的bin的个数
		self.bins = bins

	# 将RGB转换为HSV并初始化特征以量化和表示图像
	def describe(self, image):
		image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		features = []

		# 获取图像的尺寸并计算图像的中心
		(h, w) = image.shape[:2]
		(cx, cy) = (int(w * 0.5), int(h * 0.5))

		# 将图像分成四个部分（左上角，右上角，右下角，左下角）
		segments = [(0, cx, 0, cy), (0, cx, cy, h), (cx, w, cy, h), (cx, w, 0, cy)]

		# 构造一个椭圆形的mask，代表图像的中心，大小为图像的0.75倍
		(axesX, axesY) = (int(int(w * 0.75) / 2), int(int(h * 0.75) / 2))
		ellipse_mask = np.zeros(image.shape[:2], dtype="uint8")
		cv2.ellipse(ellipse_mask, (cx, cy), (axesX, axesY), 0, 0, 360, 255, -1)

		# 遍历四个corner
		for seg in segments:
			# 构造每个corner的mask
			corner_mask = np.zeros(image.shape[:2], dtype='uint8')
			corner_mask[seg[0]:seg[1], seg[2]:seg[3]] = 255
			corner_mask = cv2.subtract(corner_mask, ellipse_mask)

			# 提取对应corner区域的HSV直方图特征
			hist = self.histogram(image, corner_mask)

			features.extend(hist)

		# 提取中心椭圆区域的HSV直方图特征
		hist_ellipse = self.histogram(image, ellipse_mask)
		features.extend(hist_ellipse)

		return features

	# 计算图像的对应mask区域的直方图
	def histogram(self, image, mask):
		hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins,
			[0, 180, 0, 256, 0, 256])

		# 归一化，使得直方图具有尺度不变性
		hist = cv2.normalize(hist, hist).flatten()

		return hist