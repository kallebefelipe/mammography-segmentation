import matplotlib.pyplot as plt
from skimage import io

# images = ['mdb001', 'mdb002', 'mdb005', 'mdb010', 'mdb012', 'mdb013', 'mdb015',
#           'mdb017', 'mdb019', 'mdb021', 'mdb023', 'mdb025', 'mdb028', 'mdb030',
#           'mdb032', 'mdb058', 'mdb063', 'mdb069', 'mdb080', 'mdb091',
#           'mdb132_1', 'mdb132_2', 'mdb134', 'mdb141', 'mdb142', 'mdb144_1',
#           'mdb144_2', 'mdb145', 'mdb148', 'mdb175', 'mdb178', 'mdb179',
#           'mdb181', 'mdb184', 'mdb186', 'mdb188', 'mdb190', 'mdb191', 'mdb193',
#           'mdb195', 'mdb198', 'mdb199', 'mdb202', 'mdb204', 'mdb206', 'mdb207',
#           'mdb244', 'mdb264', 'mdb265', 'mdb267', 'mdb270', 'mdb271', 'mdb274',
#           'mdb290', 'mdb312', 'mdb314', 'mdb315']
# images = ['mdb032']
images = [
          'mdb264', 'mdb265', 'mdb267', 'mdb270', 'mdb271', 'mdb274',
          'mdb290', 'mdb312', 'mdb314', 'mdb315']

for each in images:
    image = io.imread('data/'+each+'_bin.bmp')
    plt.imshow(image, cmap='gray', interpolation='nearest')
    plt.show()
