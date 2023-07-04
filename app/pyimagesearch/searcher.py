import numpy as np
import csv

class Searcher:
	def __init__(self, indexPath):
		self.indexPath = indexPath

	# 寻找最相似的图像。queryFeatures: 从待检索图像中提取的特征,limit:卡方距离门限，当d<=limit时，认为两幅图像相似
	def search(self, queryFeatures,limit = 6.8):
		# results存放检索结果
		results = {}

		with open(self.indexPath) as f:
			reader = csv.reader(f)
			for row in reader:
				# 提取index.csv文件中存储的图像名和特征向量。row[0]: 图像的唯一文件名，row[1:]: 图像的特征向量
				features = [float(x) for x in row[1:]]
				# 计算待检索图像和index.csv文件中图像的特征向量的卡方距离
				d = self.chi2_distance(features, queryFeatures)
				# 当卡方距离小于等于limit时，将卡方距离和图像名存入results中
				if d <= limit:
					results[row[0]] = d
			f.close()
		# 按照卡方距离从小到大排序（卡方距离越小，越相似）
		results = sorted([(v, k) for (k, v) in results.items()])
		if len(results) >= 6:
			results = results[:6]
		return results

	# 计算两个特征向量的卡方距离
	def chi2_distance(self, histA, histB, eps = 1e-10):
		d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
			for (a, b) in zip(histA, histB)])
		return d