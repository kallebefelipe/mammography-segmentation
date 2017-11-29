"""
Fuzzy witch normalizaton
"""

import numpy as np
from skimage.segmentation import random_walker
from skimage import io
import scipy.misc
from skimage import segmentation
import scipy.io
from math import sqrt
import math
import csv
import cv2

train_data_dir = "../evolucao/data_deep_learning/rotulos_train.txt"
test_data_dir = "../evolucao/data_deep_learning/rotulos_test.txt"


def read_file(path):
    with open(path) as f:
        data = f.readlines()
        data = [x.replace('\n', '').split(',') for x in data]
        return data


images = []
input_train = read_file(train_data_dir)
input_test = read_file(test_data_dir)

count = 0
for each in input_train:
    images.append(each[0])
count = 0
for each in input_test:
    images.append(each[0])

beta = [10000]
tol = [0.02]
mode = ['cg']

constante = [5]


medias = []
numero_marcacao = []
sub_pasta = 5

for count, i in enumerate(images):
    print(count)
    i = i.replace('data', 'data_deep_learning')
    numbMarkx = 0
    numbMarky = 0
    posX = [0] * int(sub_pasta)
    posY = [0] * int(sub_pasta)
    posX_origem = [0] * int(sub_pasta)
    posY_origem = [0] * int(sub_pasta)
    image = cv2.imread('../evolucao/'+i, 0)
    if image is not None and 'test' in i and 'II' in i:
        markers = np.zeros((image.shape[0], image.shape[1]))

        with open('../evolucao/'+i.replace('png', 'txt')) as f:
            data = f.readlines()
            for item in data[:int(sub_pasta)]:
                item = item.replace('\n', '')
                item = item.split(',')
                posX[numbMarkx] = int(item[1])
                posY[numbMarky] = int(item[2])
                posX_origem[numbMarkx] = int(item[1])
                posY_origem[numbMarky] = int(item[2])
                numbMarkx = numbMarkx + 1
                numbMarky = numbMarky + 1
        colb = 1
        posX = list(map(lambda x: x/float(image.shape[0]), posX))
        posY = list(map(lambda x: x/float(image.shape[1]), posY))

        xm = 0
        ym = 0
        ax = 1
        ay = 1
        desviox = 0
        desvioy = 0
        constantex = 1
        constantey = 1

        for x in range(0, numbMarkx):
            xm = xm + posX[x]
        xm = xm / numbMarkx

        for y in range(0, numbMarky):
            ym = ym + posY[y]
        ym = ym / numbMarky

        somadorx = 0

        for x in range(0, numbMarkx):
            somadorx = somadorx + (math.pow((posX[x] - xm), 2))
        desviox = sqrt(somadorx / float(numbMarkx-1))
        somadory = 0

        for y in range(0, numbMarky):
            somadory = somadory + (math.pow((posY[y] - ym), 2))

        desvioy = sqrt(somadory / float(numbMarky-1))

        imageShape = np.ones((image.shape[0], image.shape[1]))

        for x in range(0, image.shape[0]):
            for y in range(0, image.shape[1]):
                x_n = x/float(image.shape[0])
                y_n = y/float(image.shape[1])
                try:
                    imageShape[x, y] = \
                        math.exp(((-1)*math.pow((x_n-xm), 2)) / float(2 * constantex * desviox) + ((-1) * math.pow((y_n-ym), 2))/float(2*constantey*desvioy))
                except:
                    imageShape[x, y] = \
                        math.exp(((-1)*math.pow((x_n-xm), 2)) / float(2 * constantex * 1) + ((-1) * math.pow((y_n-ym), 2))/float(2*constantey*1))

        copia = cv2.imread('../evolucao/'+i, 0)

        for x in range(0, image.shape[0]):
            for y in range(0, image.shape[1]):
                if(imageShape[x, y] > 0.5):
                    copia[x, y] = 1
                else:
                    copia[x, y] = 0

        for x in range(0, image.shape[0]):
            for y in range(0, image.shape[1]):
                val2 = copia[x, y]
                if val2 == 0:
                    markers[x][y] = 2

        for pos in range(0, int(sub_pasta)):

            markers[posX_origem[pos]][posY_origem[pos]] = 1

        pos = 0
        for a in beta:
            for b in tol:
                for c in mode:
                    labels_rw = random_walker(image,
                                              markers,
                                              beta=a, tol=b, mode=c)
                    contorno = \
                        segmentation.mark_boundaries(image,
                                                     labels_rw,
                                                     color=(0, 1, 0))
                    name = \
                        '../evolucao/'+i.replace('.png','_segmentacao.png')
                    scipy.misc.imsave(name, contorno)
                    labels_rw = (2-labels_rw)
