"""
Fuzzy witch normalizaton
"""

import numpy as np
from skimage.segmentation import random_walker
from skimage import io
import scipy.misc
from skimage import segmentation
import scipy.io
import csv

beta = [10000, 20000, 30000, 40000]
tol = [0.01, 0.02, 0.0001]
mode = ['cg_mg', 'cg', 'bf']

constante = [5]

pastas = ['primeira', 'segunda', 'terceira']
sub_pastas = ['4', '6', '8']

medias = []
numero_marcacao = []
for pasta in pastas:
    for sub_pasta in sub_pastas:
        with open('../output/classico/'+pasta+'/'+sub_pasta+'/resultado.csv', "w") as \
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
                count = 0
                posX_origem = [0] * int(sub_pasta)
                posY_origem = [0] * int(sub_pasta)
                posX_externo = [0] * int(sub_pasta)
                posY_externo = [0] * int(sub_pasta)
                image = io.imread('../data/imagens/'+i+'.bmp')
                markers = np.zeros((image.shape[0], image.shape[1]))

                with open('../data/'+pasta+'/'+sub_pasta+'/'+i+'.txt') as f:
                    data = f.readlines()
                    for item in data[:int(sub_pasta)]:
                        item = item.replace('\n', '')
                        item = item.split(',')
                        posX_origem[count] = int(item[2])
                        posY_origem[count] = int(item[1])
                        count += 1

                    count = 0

                    for item in data[int(sub_pasta):int(sub_pasta)*2]:
                        item = item.replace('\n', '')
                        item = item.split(',')
                        posX_externo[count] = int(item[2])
                        posY_externo[count] = int(item[1])
                        count += 1

                for pos in range(0, int(sub_pasta)):

                    markers[posX_origem[pos]][posY_origem[pos]] = 1
                    markers[posX_externo[pos]][posY_externo[pos]] = 2

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
                                '../output/classico/'+pasta+'/'+sub_pasta +\
                                '/imagens/'+i+'-'+str(a)+'-'+str(b) +\
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
            print(pasta, sub_pasta)
            media[0] = pasta+': '+sub_pasta
            medias.append(media)
            output.writerow(media)

            with open('../output/classico/'+pasta+'/'+sub_pasta+'/result_medias.csv',
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

with open('../output/classico/resultados.csv', "w") as output:
    saida = csv.writer(output, quoting=csv.QUOTE_ALL)
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

    saida.writerow(cabecalho_1)

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
    saida.writerow(cabecalho_2)

    for each in medias:
        saida.writerow(each)
