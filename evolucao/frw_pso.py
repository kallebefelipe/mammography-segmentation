import numpy as np
from skimage.segmentation import random_walker
from skimage import segmentation
from math import sqrt
import scipy.misc
import math
import copy

beta = 30000
tol = 0.02
mode = 'bf'

constante = 5


def frw_pso(image, ouro, individu, pasta, path, n):
    numbMarkx = 0
    numbMarky = 0
    tamanho_individuo = len(individu)
    posX = [0] * tamanho_individuo
    posY = [0] * tamanho_individuo
    posX_origem = [0] * tamanho_individuo
    posY_origem = [0] * tamanho_individuo
    markers = np.zeros((image.shape[0], image.shape[1]))

    for count, item in enumerate(individu):
        if (count % 2) == 0:
            posX[numbMarkx] = individu[count]
            posY[numbMarky] = individu[count+1]
            posX_origem[numbMarkx] = individu[count]
            posY_origem[numbMarky] = individu[count+1]
            numbMarkx = numbMarkx + 1
            numbMarky = numbMarky + 1

    posX = list(map(lambda x: x/float(image.shape[0]), posX))
    posY = list(map(lambda x: x/float(image.shape[1]), posY))

    xm = 0
    ym = 0
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
                    math.exp(((-1)*math.pow((x_n-xm), 2)) / float(
                        2 * constantex * desviox) + ((-1) * math.pow(
                            (y_n-ym), 2))/float(2*constantey*desvioy))
            except:
                imageShape[x, y] = \
                    math.exp(((-1)*math.pow((x_n-xm), 2)) / float(
                        2 * constantex * 1) + ((-1) * math.pow(
                            (y_n-ym), 2))/float(2*constantey*1))

    copia = copy.deepcopy(image)

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

    for pos in range(0, tamanho_individuo):
        markers[posX_origem[pos]][posY_origem[pos]] = 1

    labels_rw = random_walker(image,
                              markers,
                              beta=beta, tol=tol, mode=mode)
    contorno_ouro = \
        segmentation.mark_boundaries(image, ouro,
                                     color=(0, 0, 0))
    contorno = \
        segmentation.mark_boundaries(contorno_ouro,
                                     labels_rw,
                                     color=(0, 1, 0))
    scipy.misc.imsave('resultados_pso/'+str(pasta) +
                      '/images/'+path+'-'+str(n)+'-'+str(tamanho_individuo) +
                      '_seg.bmp', contorno)
    labels_rw = (2-labels_rw)

    TP = sum((labels_rw == 1) & (ouro == 255))
    somaTP = sum(TP)
    FN = sum((labels_rw == 0) & (ouro == 255))

    FP = sum((labels_rw == 1) & (ouro == 0))
    somaFN = sum(FN)
    somaFP = sum(FP)

    Jaccard = somaTP/float(somaTP + somaFN + somaFP)

    return Jaccard
