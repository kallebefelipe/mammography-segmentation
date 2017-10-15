from skimage import io
import scipy.misc
import skimage
import csv
from datetime import datetime
from pso import PSO
from pso import fitnessFunction


def avaliar_result(ouro, individual):
    count_correct = 0
    for count, semente in enumerate(individual):
        if (count % 2) == 0:
            if ouro[individual[count]][individual[count+1]] == 255:
                count_correct += 1
    return str((count_correct*100)/(len(individual)/2))


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

N = [10]
PopulationSize = [30]
interation = 1


medias_interacao = []
desvios_interacao = []
for pasta in range(1, interation+1):
    with open('sementes_pso/resultado.csv', "w") as \
                resultado:
        output = csv.writer(resultado, quoting=csv.QUOTE_ALL)

        cabecalho_1 = []
        cabecalho_1.append("")
        count = 0
        for n in N:
            for population_size in PopulationSize:
                titulo = 'Pop= '+str(population_size) + \
                         ', Sement='+str(n)
                cabecalho_1.append(titulo)
                count += 1
        output.writerow(cabecalho_1)

        soma = [0] * count
        matriz_resultado = []
        for count, path in enumerate(images):
            print('Interacao: '+str(pasta)+' | Image: '+str(count))
            comeco = datetime.now()

            row = []
            row_result = []
            row.append(path)
            image = io.imread('../data/imagens/'+path+'.bmp')
            ouro = io.imread('../data/imagens/'+path+'_bin.bmp')
            max_x = image.shape[0]
            max_y = image.shape[1]
            tamanho_image = [max_x, max_y]

            pos_soma = 0
            for n in N:
                for population_size in PopulationSize:
                    pso = PSO()
                    bestFitness =  pso.run(fitnessFunction, max_x, max_y, dimensions=n,
                                      num_particles=population_size, maxiter=3000, image_atual=image)

                    image_rgb = skimage.color.grey2rgb(image)
                    for i in range(0, n):
                        if (i % 2) == 0:
                            image_rgb[bestFitness[i]][bestFitness[i+1]] = [255, 0, 0]
                            try:
                                image_rgb[bestFitness[i]][bestFitness[i+1]-1] = [255, 0, 0]
                            except:
                                pass
                            try:
                                image_rgb[bestFitness[i]][bestFitness[i+1]+1] = [255, 0, 0]
                            except:
                                pass
                            try:
                                image_rgb[bestFitness[i]+1][bestFitness[i+1]] = [255, 0, 0]
                            except:
                                pass
                            try:
                                image_rgb[bestFitness[i]-1][bestFitness[i+1]] = [255, 0, 0]
                            except:
                                pass
                    scipy.misc.imsave('sementes_pso/imagens/'+path+
                                      '-'+str(n)+'-'+str(population_size) +
                                      '.bmp', image_rgb)

                    f = open('sementes_pso/'+path+'.txt', 'w')

                    for x in range(0, n):
                        if (x % 2) == 0:
                            f.write('1,'+str(int(bestFitness[x]))+','+str(int(bestFitness[x+1]))+'\n')

                    f.close()

                    percent = avaliar_result(ouro, bestFitness)
                    row.append(avaliar_result(ouro, bestFitness))
                    soma[pos_soma] += float(percent)

                    row_result.append(float(percent))
                    pos_soma += 1
            matriz_resultado.append(row_result)
            output.writerow(row)
            fim = datetime.now()
            print(fim-comeco)

        row = ['media']
        media = []
        for som in soma:
            row.append(str(som/len(images)))
            media.append(som/len(images))
        output.writerow(row)
        medias_interacao.append(media)

        desvio = []
        for col in range(0, len(matriz_resultado[0])):
            somatorio = 0
            for lin in range(0,     len(matriz_resultado)):
                somatorio += (matriz_resultado[lin][col]-media[col])**2

            if len(images) == 1 or somatorio == 0:
                desvio.append(0)
            else:
                desvio.append((somatorio/len(images)-1)**(1/2))
        desvios_interacao.append(desvio)

        row = ['desvio']
        for each in desvio:
            row.append(each)

        output.writerow(row)
