"""Example of applying threshold to image.

Tested with : 
pyimagej            1.4.1
matplotlib          3.8.4
numpy               1.26.4
JPype1              1.5.0
bfio                2.1.9

"""

import imagej
import imglyb
import scyjava
import numpy as np
from scyjava import jimport

# scyjava to configure the JVM
scyjava.config.add_option('-Xmx6g')


# initialize imagej
ij = imagej.init('sc.fiji:fiji:2.14.0', mode='headless')

print(f"ImageJ2 version: {ij.getVersion()}")

# Start up ImageJ
ij = imagej.init()

# Load the image
url_colony = 'https://wsr.imagej.net/images/Cell_Colony.jpg'
cell_colony = ij.io().open(url_colony)

# get python inputs
threshold_value = 100.00

# import java types
Unsigned = jimport('net.imglib2.type.numeric.integer.UnsignedByteType')

# convert to java types
threshold = Unsigned(100)

# Method 1
# we can pass Dataset directly
_output_2 = ij.op().run("threshold.apply", cell_colony, threshold)

# Method 2
# We need to convert Dataset to Iterable
# otherwise method overloading dispatch fails.
img_iterable = ij.op().transform().flatIterableView(cell_colony)
_output_1 = ij.op().threshold().apply(img_iterable, threshold)

# Get numpy array back
out_array_1 = ij.py.from_java(_output_1)
out_array_2 = ij.py.from_java(_output_2)

ij.py.show(cell_colony, cmap='gray')
ij.py.show(out_array_1, cmap='gray')
ij.py.show(out_array_2, cmap='gray')