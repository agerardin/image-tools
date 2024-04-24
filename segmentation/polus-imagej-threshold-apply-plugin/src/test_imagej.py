import imagej
import imglyb
import scyjava

import numpy as np
from scyjava import jimport



# scyjava to configure the JVM
scyjava.config.add_option('-Xmx6g')


# initialize imagej. Take a older version.
# only headless mode works on osx
# ij = imagej.init("sc.fiji:fiji:2.1.1+net.imagej:imagej-legacy:0.37.4", mode='headless')
ij = imagej.init('sc.fiji:fiji:2.14.0', mode='headless')
# ij = imagej.init("2.14.0", mode='headless')
print(f"ImageJ2 version: {ij.getVersion()}")


import imagej

# Start up ImageJ
ij = imagej.init()

# open image
image = ij.io().open("https://fiji.sc/samples/blobs.png")

# threshoold the image
binary = ij.op().threshold().otsu(image)

# show result
# ij.py.show(binary)

# Load the image
url_colony = 'https://wsr.imagej.net/images/Cell_Colony.jpg'
cell_colony = ij.io().open(url_colony)

# Send the image to Python
xr_colony = ij.py.from_java(cell_colony)

# Display the image
# ij.py.show(xr_colony, cmap='gray')

print(f"cell_colony type: {type(cell_colony)}")
print(f"xr_colony type: {type(xr_colony)}")


array = np.random.rand(5, 4, 3)
dataset = ij.py.to_java(array)

print(dataset.shape)

System = jimport('java.lang.System')
Unsigned = jimport('net.imglib2.type.numeric.integer.UnsignedByteType')
System.out.println("ok")
Runtime = jimport('java.lang.Runtime')
print(Runtime.getRuntime().maxMemory() // (2**20), " MB available to Java")

test_image_path = "/Users/antoinegerardin/Documents/data/imageJ/test_image.tif"
dataset = ij.io().open(test_image_path)
# ij.py.show(dataset)
# import HyperSphereShape and create radius of 5
HyperSphereShape = jimport('net.imglib2.algorithm.neighborhood.HyperSphereShape')
radius = HyperSphereShape(5)

# apply filter
result = ij.dataset().create(dataset)
ij.op().filter().mean(result, dataset, radius)

# show image
# ij.py.show(result)

ApplyManualThreshold = jimport('net.imagej.ops.threshold.apply.ApplyManualThreshold')
threshold = ApplyManualThreshold()

print(threshold)

threshold_value = 100.00

# type net.imglib2.IterableInterval
_input = imglyb.util.Views.iterable(ij.py.to_java(xr_colony))
# to_imageplus
# _input2 = ij.py.to_imageplus(xr_colony)

dtype = ij.py.dtype(_input)

from skimage import io

# Create a numpy image using scikit
img = io.imread('https://imagej.net/images/clown.jpg')
# ij.py.show(img)

img_dataset = ij.py.to_java(img)

result = np.zeros(img.shape) # HINT: Uses float dtype, for more accurate noising.

imgIterable = ij.op().transform().flatIterableView(img_dataset)
resIterable = ij.op().transform().flatIterableView(ij.py.to_java(result))

ij.op().filter().addPoissonNoise(resIterable, imgIterable)

# ij.py.show(result)
# _input3 = cell_colony.getImgPlus().getImg()


# threshold = ij.py.to_java(ij, threshold_value, "RealType", dtype=dtype)
threshold = ij.py.to_java(threshold_value)
# thresholdIterable = ij.op().transform().flatIterableView(threshold)
_output = ij.op().run("threshold.apply", cell_colony, Unsigned(100))
_output = ij.op().run("threshold.huang", cell_colony)
# _output = ij.op().run("threshold.manual", cell_colony)
_output = ij.op().threshold().apply(imgIterable, Unsigned(100))
out_array = ij.py.from_java(_output)
ij.py.show(out_array, cmap='gray')