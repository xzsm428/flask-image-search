from pyimagesearch.FeatureDescriptor import FeatureDescriptor
import argparse
import glob
import cv2

# 构造参数解析器并解析参数
#  python index.py --dataset static/dataset --index index.csv
ap = argparse.ArgumentParser()
# --dataset: 数据集的路径
ap.add_argument("-d", "--dataset", required = True,
	help = "Path to the directory that contains the images to be indexed")
# --index: 从数据集中提取的图像特征index.csv文件的路径
ap.add_argument("-i", "--index", required = True,
	help = "Path to where the computed index will be stored")
args = vars(ap.parse_args())

# 初始化FeatureDescriptor类
# 8个色调bin，12个饱和度bin，3个value bin
cd = FeatureDescriptor((8, 12, 3))

# 图像特征索引文件output
output = open(args["index"], "w")
# 遍历数据集中的所有图片
for imagePath in glob.glob(args["dataset"] + "/*.jpg"):
	# imageID：图像的唯一文件名
	imageID = imagePath.split("\\")[-1]
	image = cv2.imread(imagePath)
	# 提取图像的特征并写入文件
	# 图像分为五个区域，每个区域由一个直方图表示（包含8*12*3=288个bin），所以整体特征向量维数为288*5=1440
	features = cd.describe(image)
	features = [str(f) for f in features]
	output.write("%s,%s\n" % (imageID, ",".join(features)))

output.close()