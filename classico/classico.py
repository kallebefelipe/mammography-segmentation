
import numpy as np
from skimage.morphology import watershed
from skimage.feature import peak_local_max
from skimage import measure
from skimage.segmentation import random_walker
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage import io
from pylab import plot, ginput, show, axis
import sys
import numpy
from PIL import Image
import scipy.misc
from skimage import segmentation
from numpy import array
import PIL.ImageOps
import scipy.io
import numpy as np
import scipy.io as sio
import xlsxwriter

workbook = xlsxwriter.Workbook('resultado.xlsx')
worksheet = workbook.add_worksheet()


f = open('resultado.txt','w')
beta = ['10000','20000','30000','40000']
tol = ['0.01','0.02','0.0001']
mode= ['cg_mg', 'cg', 'bf']

col = 1
for a in beta:
    for b in tol:
        for c in mode:
            worksheet.write(0, col, 'beta='+a+' tol='+b+' mode='+c+' ')
            col = col+4


col = 1
for a in beta:
    for b in tol:
        for c in mode:
            worksheet.write(1, col,    'TP')
            col = col + 1
            worksheet.write(1, col,    'TN')
            col = col + 1
            worksheet.write(1, col,    'FP')
            col = col + 1
            worksheet.write(1, col,    'FN')
            col = col + 1


images = ['mdb001', 'mdb002', 'mdb005','mdb010','mdb012','mdb013','mdb015','mdb017','mdb019','mdb021','mdb023','mdb025','mdb028','mdb030','mdb032','mdb058','mdb063','mdb069','mdb080','mdb091','mdb132_1','mdb132_2','mdb134','mdb141','mdb142','mdb144_1','mdb144_2','mdb145','mdb148','mdb175','mdb178','mdb179','mdb181','mdb184','mdb186','mdb188','mdb190','mdb191','mdb193','mdb195','mdb198','mdb199','mdb202','mdb204','mdb206','mdb207','mdb244','mdb264','mdb265','mdb267','mdb270','mdb271','mdb274','mdb290','mdb312','mdb314','mdb315']

row = 2
rowb = 2
for i in images:
    worksheet.write(row, 0,    i)
    row = row + 1
    image = io.imread("imagens/"+i+'.bmp')
    mat_contents = sio.loadmat('sementes/labels_roi/'+i+'.mat')
    oct_cells = mat_contents['labels']
    val = oct_cells[0, 1]
    markers = np.zeros((image.shape[0], image.shape[1]))

    for x in range(0, image.shape[0]):
        for y in range(0, image.shape[1]):
            val = oct_cells[x, y]

            if val == 1:
                markers[x][y] = 1
            if val == -1:
                markers[x][y] = 2

    ouro = io.imread('imagens/'+i+'_bin.bmp')

    beta = [10000, 20000, 30000, 40000]
    tol = [0.01, 0.02, 0.0001]
    mode = ['cg_mg', 'cg', 'bf']

    colb = 1

    for a in beta:
        for b in tol:
            for c in mode:
                labels_rw = random_walker(image, markers, beta = a, tol=b, mode=c)
                name = '%d-%.4f-%s.jpg' %(a,b,c)
                contorno = segmentation.mark_boundaries(image, ouro, color=(0,0,0))
                contorno = segmentation.mark_boundaries(contorno, labels_rw, color=(0,1,0))
                name = 'resultados/'+str(i)+"-"+str(a)+"-"+str(b)+"-"+str(c)+'.jpg'
                scipy.misc.imsave(name, contorno)

                labels_rw = (2-labels_rw) # Inverter imagem

                TP = sum((labels_rw == 1) & (ouro == 255))
                somaTP = sum(TP)
                TN = sum((labels_rw == 0) & (ouro == 0))
                somaTN = sum(TN)
                FP = sum((labels_rw == 0) & (ouro == 255))
                somaFP = sum(FP)
                FN = sum((labels_rw == 1) & (ouro == 0))
                somaFN = sum(FN)

                worksheet.write(rowb, colb,    somaTP)
                colb = colb + 1
                worksheet.write(rowb, colb,    somaTN)
                colb = colb + 1
                worksheet.write(rowb, colb,    somaFP)
                colb = colb + 1
                worksheet.write(rowb, colb,    somaFN)
                colb = colb + 1

                XOR = (somaFP + somaFN) / (somaTP + somaFN)
                Precision = somaTP/(somaTP + somaFP)
                Sensitivity = somaTP / (somaTP + somaFN)
                Specificity = somaTN / (somaFP + somaTN)
                Jaccard = somaTP/(somaTP + somaFN + somaFP)
                Recall = somaTP/(somaTP + somaFN)
                Fmeasure = (Precision*Recall)/(Precision+Recall)
                TP = str(somaTP)
                TN = str(somaTN)
                FP = str(somaFP)
                FN = str(somaFN)

    rowb = rowb + 1
workbook.close()
