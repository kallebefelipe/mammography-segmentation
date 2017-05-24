"""
Fuzzy witch normalizaton
"""

import numpy as np
from skimage.segmentation import random_walker
from skimage import io
import scipy.misc
from skimage import segmentation
import scipy.io
import scipy.io as sio
import xlsxwriter
from math import sqrt
import math

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('resultado_fuzzy_si_v2.xlsx')
worksheet = workbook.add_worksheet()


beta = [10000, 20000, 30000, 40000]
tol = [0.01, 0.02, 0.0001]
mode = ['cg_mg', 'cg', 'bf']
constante = [5]

col = 1

for a in beta:
    for b in tol:
        for c in mode:
            worksheet.write(0, col, ' beta='+str(a)+' tol='+str(b) +
                            ' mode='+str(c)+' ')
            col = col+8


col = 1
for a in beta:
    for b in tol:
        for c in mode:
            worksheet.write(1, col, 'TP')
            col = col + 1
            worksheet.write(1, col, 'TN')
            col = col + 1
            worksheet.write(1, col, 'FP')
            col = col + 1
            worksheet.write(1, col, 'FN')
            col = col + 1
            worksheet.write(1, col, 'Sensibility')
            col = col + 1
            worksheet.write(1, col, 'Especificy')
            col = col + 1
            worksheet.write(1, col, 'Jaccard')
            col = col + 1
            worksheet.write(1, col, 'TFP')
            col = col + 1

images = ['mdb001', 'mdb002',  'mdb005', 'mdb010', 'mdb012', 'mdb013',
          'mdb015', 'mdb017', 'mdb019', 'mdb021', 'mdb023', 'mdb025',
          'mdb028', 'mdb030', 'mdb032', 'mdb058', 'mdb063', 'mdb069',
          'mdb080', 'mdb091', 'mdb132_1', 'mdb132_2', 'mdb134', 'mdb141',
          'mdb142', 'mdb144_1', 'mdb144_2', 'mdb145', 'mdb148', 'mdb175',
          'mdb178', 'mdb179', 'mdb181', 'mdb184', 'mdb186', 'mdb188',
          'mdb190', 'mdb191', 'mdb193', 'mdb195', 'mdb198', 'mdb199',
          'mdb202', 'mdb204', 'mdb206', 'mdb207', 'mdb244', 'mdb264',
          'mdb265', 'mdb267', 'mdb270', 'mdb271', 'mdb274', 'mdb290',
          'mdb312', 'mdb314', 'mdb315']

row = 2
rowb = 2

for i in images:
    numbMarkx = 0
    numbMarky = 0
    posX = [0, 0, 0, 0, 0, 0]
    posY = [0, 0, 0, 0, 0, 0]
    worksheet.write(row, 0, i)
    row = row + 1
    # image = io.imread('imagens/'+i+'.bmp');
    image = io.imread("../base/" + i + '.bmp')
    # mat_contents = sio.loadmat('sementes/labels_roi/'+i+'.mat')
    mat_contents = sio.loadmat('../base/labels_roi/'+i+'.mat')
    oct_cells = mat_contents['labels']
    val = oct_cells[0, 1]
    markers = np.zeros((image.shape[0], image.shape[1]))

    for x in range(0, image.shape[0]):
        for y in range(0, image.shape[1]):
            val1 = oct_cells[x, y]

            if val1 == 1:
                posX[numbMarkx] = x
                posY[numbMarky] = y
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
            imageShape[x, y] = \
                math.exp(((-1)*math.pow((x_n-xm), 2)) / float(2 * constantex * desviox) + ((-1) * math.pow((y_n-ym), 2))/float(2*constantey*desvioy))

    # copia =  io.imread('imagens/'+i+'.bmp')
    copia = io.imread("../base/" + i + '.bmp')

    for x in range(0, image.shape[0]):
        for y in range(0, image.shape[1]):
            if(imageShape[x, y] > 0.5):
                copia[x, y] = 1
            else:
                copia[x, y] = 0

    contorno = segmentation.mark_boundaries(image, copia, color=(1, 0, 0))

    for x in range(0, image.shape[0]):
        for y in range(0, image.shape[1]):
            val1 = oct_cells[x, y]
            val2 = copia[x, y]

            if val1 == 1:
                markers[x][y] = 1
            if val2 == 0:
                markers[x][y] = 2


    # ouro = io.imread('imagens/'+i+'_bin.bmp')
    ouro = io.imread('../base/'+i+'_bin.bmp')

    for a in beta:
        for b in tol:
            for c in mode:
                labels_rw = random_walker(image=image, markers=markers,
                                          beta=a, tol=b, mode=c)
                name = '%d-%.4f-%s.jpg' % (a, b, c)
                contorno = segmentation.mark_boundaries(image, ouro,
                                                        color=(0, 0, 0))
                contorno = segmentation.mark_boundaries(contorno, labels_rw,
                                                        color=(0, 1, 0))
                name = 'resultados/'+i+'-'+str(a)+'-'+str(b)+'-'+str(c)+'.jpg'
                scipy.misc.imsave(name, contorno)
                labels_rw = (2-labels_rw)

                TP = sum((labels_rw == 1) & (ouro == 255))
                somaTP = sum(TP)
                TN = sum((labels_rw == 0) & (ouro == 0))
                somaTN = sum(TN)
                FN = sum((labels_rw == 0) & (ouro == 255))

                FP = sum((labels_rw == 1) & (ouro == 0))
                somaFN = sum(FN)
                somaFP = sum(FP)

                worksheet.write(rowb, colb,    somaTP)
                colb = colb + 1
                worksheet.write(rowb, colb,    somaTN)
                colb = colb + 1
                worksheet.write(rowb, colb,    somaFP)
                colb = colb + 1
                worksheet.write(rowb, colb,    somaFN)
                colb = colb + 1

                XOR = (somaFP + somaFN)/(somaTP + somaFN)
                Precision = somaTP/float(somaTP + somaFP)
                Sensitivity = somaTP/float(somaTP + somaFN)
                Specificity = somaTN/float(somaFP + somaTN)
                Jaccard = somaTP/float(somaTP + somaFN + somaFP)
                Recall = somaTP/float(somaTP + somaFN)

                if (Precision != 0) and (Recall != 0):
                    Fmeasure = (Precision*Recall)/(Precision+Recall)
                else:
                    Fmeasure = 0

                worksheet.write(rowb, colb, Sensitivity)
                colb = colb + 1
                worksheet.write(rowb, colb, Specificity)
                colb = colb + 1
                worksheet.write(rowb, colb, Jaccard)
                colb = colb + 1
                worksheet.write(rowb, colb, 1-Specificity)
                colb = colb + 1

    rowb = rowb + 1

workbook.close()
