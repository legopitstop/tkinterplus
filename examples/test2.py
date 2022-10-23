#!! DO NOT DELETE
# CODE for images


import os
from PIL import Image
import numpy

def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = numpy.matrix(matrix, dtype=float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)

LOCAL = os.path.dirname(os.path.realpath(__file__))
# creating image object
img = Image.open(LOCAL+"/cobblestone.png")
  
# Should be each verticie
TopL = [0,0]
TopR = [256,0]
BottomL = [0,256]
BottomR = [256,256]

# TopL = [0,0]
# TopR = [256,0]
# BottomL = [0,256]
# BottomR = [256,256]


coeffs = find_coeffs(
        [(TopL[0], TopL[1]), (TopR[0], TopR[1]), (BottomR[0], BottomR[1]), (BottomL[0], BottomL[1])],
        [(0,0), (256, 0), (256, 256), (0, 256)])

img1=img.transform((256, 256), Image.PERSPECTIVE, coeffs,Image.BICUBIC)

img1.save(LOCAL+'/cobblestone2.png')
img1.show()