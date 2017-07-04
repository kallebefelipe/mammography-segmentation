"""
Fuzzy witch normalizaton
"""

import numpy as np
from skimage.segmentation import random_walker
from skimage import io
import scipy.io as sio
import scipy.misc
from skimage import segmentation
import scipy.io
from math import sqrt
import math
import csv

beta = [10000, 20000, 30000, 40000]
tol = [0.01, 0.02, 0.0001]
mode = ['cg_mg', 'cg', 'bf']

constante = [5]

medias = []
numero_marcacao = []
with open('../output/fuzzy-sementes-iniciais/resultado.csv', "w") as \
        resultado:
    output = csv.writer(resultado, quoting=csv.QUOTE_ALL)

    cabecalho_1 = []
    cabecalho_1.append("")
    for a in beta:
        for b in tol:
            for c in mode:
                titulo = str(' beta='+str(a)+' tol='+str(b) +
                             ' mode='+str(c)+' ')
                cabecalho_1.append(titulo)
                cabecalho_1.append('')
                cabecalho_1.append('')
                cabecalho_1.append('')
                cabecalho_1.append('')
                cabecalho_1.append('')
                cabecalho_1.append('')
                cabecalho_1.append('')

    output.writerow(cabecalho_1)

    cabecalho_2 = []
    cabecalho_2.append('')
    cont = 0
    for a in beta:
        for b in tol:
            for c in mode:
                cabecalho_2.append('TP')
                cabecalho_2.append('TN')
                cabecalho_2.append('FP')
                cabecalho_2.append('FN')
                cabecalho_2.append('Sensibility')
                cabecalho_2.append('Especificy')
                cabecalho_2.append('Jaccard')
                cabecalho_2.append('TFP')
                cont += 8
    output.writerow(cabecalho_2)

    images = ['mdb001', 'mdb002',  'mdb005', 'mdb010', 'mdb012',
              'mdb013', 'mdb015', 'mdb017', 'mdb019', 'mdb021',
              'mdb023', 'mdb025', 'mdb028', 'mdb030', 'mdb032',
              'mdb058', 'mdb063', 'mdb069', 'mdb080', 'mdb091',
              'mdb132_1', 'mdb132_2', 'mdb134', 'mdb141', 'mdb142',
              'mdb144_1', 'mdb144_2', 'mdb145', 'mdb148', 'mdb175',
              'mdb178', 'mdb179', 'mdb181', 'mdb184', 'mdb186',
              'mdb188', 'mdb190', 'mdb191', 'mdb193', 'mdb195',
              'mdb198', 'mdb199', 'mdb202', 'mdb204', 'mdb206',
              'mdb207', 'mdb244', 'mdb264', 'mdb265', 'mdb267',
              'mdb270', 'mdb271', 'mdb274', 'mdb290', 'mdb312',
              'mdb314', 'mdb315']

    soma = [0] * cont
    for i in images:
        numbMarkx = 0
        numbMarky = 0
        posX = [0] * 6
        posY = [0] * 6
        posX_origem = [0] * 6
        posY_origem = [0] * 6
        image = io.imread('../data/imagens/'+i+'.bmp')
        markers = np.zeros((image.shape[0], image.shape[1]))

        mat_contents = sio.loadmat('../data/labels_roi/'+i+'.mat')
        oct_cells = mat_contents['labels']
        val = oct_cells[0, 1]
        markers = np.zeros((image.shape[0], image.shape[1]))

        for x in range(0, image.shape[0]):
            for y in range(0, image.shape[1]):
                val1 = oct_cells[x, y]

                if val1 == 1:
                    posX[numbMarkx] = x         #atribuicao no vetor de x's
                    posY[numbMarky] = y         #atribuicao no vetor de y's
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

        copia = io.imread('../data/imagens/' + i + '.bmp')

        for x in range(0, image.shape[0]):
            for y in range(0, image.shape[1]):
                if(imageShape[x, y] > 0.5):
                    copia[x, y] = 1
                else:
                    copia[x, y] = 0

        contorno = segmentation.mark_boundaries(image, copia,
                                                color=(1, 0, 0))

        for x in range(0, image.shape[0]):
            for y in range(0, image.shape[1]):
                val1 = oct_cells[x, y]
                val2 = copia[x, y]

                if val1 == 1:
                    markers[x][y] = 1
                if val2 == 0:
                    markers[x][y] = 2

        ouro = io.imread('../data/imagens/'+i+'_bin.bmp')

        linha = []
        linha.append(i)

        pos = 0
        for a in beta:
            for b in tol:
                for c in mode:
                    labels_rw = random_walker(image,
                                              markers,
                                              beta=a, tol=b, mode=c)
                    name = '%d-%.4f-%s.jpg' % (a, b, c)
                    contorno = \
                        segmentation.mark_boundaries(image, ouro,
                                                     color=(0, 0, 0))
                    contorno = \
                        segmentation.mark_boundaries(contorno,
                                                     labels_rw,
                                                     color=(0, 1, 0))
                    name = \
                        '../output/fuzzy-sementes-iniciais/imagens/'+i+'-'+str(a)+'-'+str(b) +\
                        '-'+str(c)+'.jpg'
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

                    linha.append(str(somaTP))
                    soma[pos] += somaTP
                    pos += 1
                    linha.append(str(somaTN))
                    soma[pos] += somaTN
                    pos += 1
                    linha.append(str(somaFP))
                    soma[pos] += somaFP
                    pos += 1
                    linha.append(str(somaFN))
                    soma[pos] += somaFN
                    pos += 1

                    XOR = (somaFP + somaFN)/(somaTP + somaFN)
                    Precision = somaTP/float(somaTP + somaFP)
                    Sensitivity = somaTP/float(somaTP + somaFN)
                    Specificity = somaTN/float(somaFP + somaTN)
                    Jaccard = somaTP/float(somaTP + somaFN + somaFP)
                    Recall = somaTP/float(somaTP + somaFN)

                    if (Precision != 0) and (Recall != 0):
                        Fmeasure = \
                            (Precision*Recall)/(Precision+Recall)
                    else:
                        Fmeasure = 0

                    linha.append(str(Sensitivity))
                    soma[pos] += Sensitivity
                    pos += 1
                    linha.append(str(Specificity))
                    soma[pos] += Specificity
                    pos += 1
                    linha.append(str(Jaccard))
                    soma[pos] += Jaccard
                    pos += 1
                    linha.append(str(1-Specificity))
                    soma[pos] += 1-Specificity
                    pos += 1
        output.writerow(linha)
    media = ['media']
    for valor in soma:
        media.append(str(valor/len(images)))
    medias.append(media)
    output.writerow(media)

    with open('../output/fuzzy-sementes-iniciais/result_medias.csv',
              "w") as result_medias:
        output_2 = csv.writer(result_medias, quoting=csv.QUOTE_ALL)

        cabecalho = ['']
        cabecalho.append('TP')
        cabecalho.append('TN')
        cabecalho.append('FP')
        cabecalho.append('FN')
        cabecalho.append('Sensibility')
        cabecalho.append('Especificy')
        cabecalho.append('Jaccard')
        cabecalho.append('TFP')
        output_2.writerow(cabecalho)
        pos_2 = 1
        for a in beta:
            for b in tol:
                for c in mode:
                    linha = []
                    linha.append(' beta='+str(a)+' tol='+str(b) +
                                 ' mode='+str(c)+' '
                                 )
                    for t in range(pos_2, pos_2+8):
                        linha.append(media[t])
                    pos_2 += 8
                    output_2.writerow(linha)
