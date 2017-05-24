import scipy.io as sio
from skimage import io
import numpy as np

path_marks = 'data/primeira/6'
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


for i in images:
    f = open('data/primeira/6/'+i+'.txt', 'w')
    mat_contents = sio.loadmat('data/labels_roi/'+i+'.mat')
    oct_cells = mat_contents['labels']
    image = io.imread("classico/imagens/" + i + '.bmp')
    markers = np.zeros((image.shape[0], image.shape[1]))
    marcacoes = []
    for x in range(0, image.shape[0]):
        for y in range(0, image.shape[1]):
            val1 = oct_cells[x, y]

            if val1 == 1:
                marcacoes.append([1, x, y])

            elif val1 == -1:
                marcacoes.append([2, x, y])
    for each in marcacoes:
        if each[0] == 1:
            f.write('1,'+str(each[1])+','+str(each[2])+'\n')
    for each in marcacoes:
        if each[0] == 2:
            f.write('2,'+str(each[1])+','+str(each[2])+'\n')
    f.close()
