from skimage import io
import scipy.misc
import random
import skimage
import csv
from datetime import datetime
from frw import frw
import math


def dist_euclidiana(p1, p2):
    soma = 0
    for i in range(len(p1)):
        soma = soma + (p2[i] - p1[i])**2
    distancia = math.sqrt(soma)
    return distancia


def fitnessFunction1(individual, N, image):
    soma = 0
    for i in range(0, N):
        soma += image[individual[i][0]][individual[i][1]]
    return soma


def fitnessFunction2(individual):
    soma = 0
    for i in range(0, len(individual)):
        for j in range(0, len(individual)):
            soma += dist_euclidiana(individual[i], individual[j])
    return soma


# def fitnessFunction(individual, N, image):
#     soma = 0
#     for i in range(0, N):
#         soma += image[individual[i][0]][individual[i][1]]
#     return soma


def generateIndividual(max_x, max_y, N):
    individual = []

    for i in range(0, N):
        x = random.randint(0, max_x-1)
        y = random.randint(0, max_y-1)
        individual.append([x, y])
    return individual


def avaliar_result(
        image, ouro, individua, pasta, path, n, cr
        ):
    # count_correct = 0
    # for semente in individual:
    #     if ouro[semente[0]][semente[1]] == 255:
    #         count_correct += 1
    # return str((count_correct*100)/len(individual))
    return frw(image, ouro, individua, pasta, path, n, cr)


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

F = 1
CR = [0.5, 0.6, 0.9]
CR = [0.9]
N = [5, 10, 15, 20]
N = [3, 5, 7, 10]
PopulationSize = [10, 20, 30]
PopulationSize = [30]
interation = 10
interation = 1


medias_interacao = []
desvios_interacao = []
for pasta in range(1, interation+1):
    with open('resultados_de/'+str(pasta)+'/resultado/resultado.csv', "w") as \
                resultado:
        output = csv.writer(resultado, quoting=csv.QUOTE_ALL)

        cabecalho_1 = []
        cabecalho_1.append("")
        count = 0
        for cr in CR:
            for n in N:
                for population_size in PopulationSize:
                    titulo = 'F= '+str(F)+', CR= '+str(cr) + \
                             ', Pop= '+str(population_size) + \
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
            for cr in CR:
                for n in N:
                    for population_size in PopulationSize:
                        population = []
                        i = 0
                        while (i < population_size):
                            individual = generateIndividual(max_x, max_y, n)
                            population.append(individual)
                            i += 1

                        i = 0
                        while (i < 3000):
                            i += 1
                            j = 0
                            while (j < population_size):
                                x = random.randint(0, population_size-1)

                                while True:
                                    a = random.randint(0, population_size-1)
                                    if a != x:
                                        break
                                while True:
                                    b = random.randint(0, population_size-1)
                                    if b != x or b != a:
                                        break
                                while True:
                                    c = random.randint(0, population_size-1)
                                    if c != x or c != a or c != b:
                                        break

                                R = random.randint(0, n-1)

                                original = population[x]
                                candidate = original

                                individual1 = population[a]
                                individual2 = population[b]
                                individual3 = population[c]

                                for w in range(0, n-1):
                                    if w == R or random.uniform(0, 1) < cr:
                                        pos = random.randint(0, 1)
                                        candidate[w][pos] = \
                                            (abs(individual1[w][pos]+F*(individual2[w][pos] -
                                                                        individual3[w][pos])) %
                                             tamanho_image[pos])

                                # if fitnessFunction(original, n, image) < \
                                #         fitnessFunction(candidate, n, image):
                                if fitnessFunction1(original, n, image) < \
                                        fitnessFunction1(candidate, n, image) and \
                                        fitnessFunction2(original) >= \
                                        fitnessFunction2(candidate):
                                    population.remove(original)
                                    population.append(candidate)

                                j += 1

                        i = 0
                        bestFitness = [[0, 0]] * n
                        while(i < population_size):
                            individual = population[i]
                            # if fitnessFunction(bestFitness, n, image) < \
                            #         fitnessFunction(individual, n, image):
                            if fitnessFunction1(bestFitness, n, image) < \
                                    fitnessFunction1(individual, n, image) and \
                                    fitnessFunction2(original) >= \
                                    fitnessFunction2(candidate):
                                bestFitness = individual
                            i += 1

                        image_rgb = skimage.color.grey2rgb(image)
                        for i in range(0, n):
                            image_rgb[bestFitness[i][0]][bestFitness[i][1]] = [255, 0, 0]
                            try:
                                image_rgb[bestFitness[i][0]][bestFitness[i][1]-1] = [255, 0, 0]
                            except:
                                pass
                            try:
                                image_rgb[bestFitness[i][0]][bestFitness[i][1]+1] = [255, 0, 0]
                            except:
                                pass
                            try:
                                image_rgb[bestFitness[i][0]+1][bestFitness[i][1]] = [255, 0, 0]
                            except:
                                pass
                            try:
                                image_rgb[bestFitness[i][0]-1][bestFitness[i][1]] = [255, 0, 0]
                            except:
                                pass
                        scipy.misc.imsave('resultados_de/'+str(pasta) +
                                          '/images/'+path+'-'+str(cr) +
                                          '-'+str(n)+'-'+str(population_size) +
                                          '.bmp', image_rgb)
                        percent = avaliar_result(
                            image, ouro, bestFitness,
                            pasta, path, n, cr)
                        row.append(avaliar_result(
                            image, ouro, bestFitness,
                            pasta, path, n, cr))
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


with open('resultados_de/resultado_final.csv', "w") as \
                resultado:
    output = csv.writer(resultado, quoting=csv.QUOTE_ALL)

    cabecalho_1 = ['']
    for cr in CR:
        for n in N:
            for population_size in PopulationSize:
                titulo = 'F= '+str(F)+', CR= '+str(cr) + \
                         ', Pop= '+str(population_size) + \
                         ', Sement='+str(n)
                cabecalho_1.append(titulo)
    output.writerow(cabecalho_1)

    soma = [0] * len(medias_interacao[0])

    for inter in range(0, interation):
        for count, med in enumerate(medias_interacao[inter]):
            soma[count] += med

    row = ['media']
    for som in soma:
        row.append(str(som/interation))
    output.writerow(row)

    soma = [0] * len(desvios_interacao[0])

    for inter in range(0, interation):
        for count, med in enumerate(desvios_interacao[inter]):
            soma[count] += med

    media = []
    for som in soma:
        media.append(som/interation)

    desvio = []
    for col in range(0, len(desvios_interacao[0])):
        somatorio = 0
        for lin in range(0, interation):
            somatorio += (desvios_interacao[lin][col]-media[col])**2

        if somatorio == 0:
            desvio.append(0)
        else:
            desvio.append((somatorio/interation-1)**(1/2))

    row = ['desvio']
    for each in desvio:
        row.append(each)

    output.writerow(row)
