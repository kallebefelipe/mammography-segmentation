from skimage import io
import scipy.misc
import random
import skimage
import csv


def fitnessFunction(individual, N, image):
    soma = 0
    for i in range(0, N):
        soma += image[individual[i][0]][individual[i][1]]

    return soma


def generateIndividual(max_x, max_y, N):
    individual = []

    for i in range(0, N):
        x = random.randint(0, max_x-1)
        y = random.randint(0, max_y-1)
        individual.append([x, y])
    return individual


def avaliar_result(ouro, individual):
    count_correct = 0
    for semente in individual:
        if ouro[semente[0]][semente[1]] == 255:
            count_correct += 1
    return (count_correct*100)/len(individual)


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
N = [5, 10, 15, 20]
PopulationSize = [10, 20, 30]

interation = 10

for pasta in range(1, 11):
    with open('resultados/'+str(pasta)+'/resultado/resultado.csv', "w") as \
                resultado:
            output = csv.writer(resultado, quoting=csv.QUOTE_ALL)

            cabecalho_1 = []
            cabecalho_1.append("")
            for cr in CR:
                for n in N:
                    for population_size in PopulationSize:
                        titulo = 'F= '+str(F)+', CR= '+str(CR) + \
                                 ', Pop= '+str(PopulationSize) + \
                                 ', Sement='+str(N)
                        cabecalho_1.append(titulo)
                        cabecalho_1.append('')
            output.writerow(cabecalho_1)

with open('resultados.csv', 'w') as fp:
    file = csv.writer(fp, quoting=csv.QUOTE_ALL)
    file.writerow(['parametros', 'percentual_acerto', 'desvio_padrao'])

    planilha = []
    for path in images:
        population = []
        image = io.imread('../data/imagens/'+path+'.bmp')
        max_x = image.shape[0]
        max_y = image.shape[1]
        tamanho_image = [max_x, max_y]

        i = 0
        while (i < PopulationSize):
            individual = generateIndividual(max_x, max_y, N)
            population.append(individual)
            i += 1

        i = 0
        while (i < 3000):
            print(i)
            i += 1
            j = 0
            while (j < PopulationSize):
                x = random.randint(0, PopulationSize-1)

                while True:
                    a = random.randint(0, PopulationSize-1)
                    if a != x:
                        break
                while True:
                    b = random.randint(0, PopulationSize-1)
                    if b != x or b != a:
                        break
                while True:
                    c = random.randint(0, PopulationSize-1)
                    if c != x or c != a or c != b:
                        break

                R = random.randint(0, N-1)

                original = population[x]
                candidate = original

                individual1 = population[a]
                individual2 = population[b]
                individual3 = population[c]

                for w in range(0, N-1):
                    if w == R or random.uniform(0, 1) < CR:
                        pos = random.randint(0, 1)
                        candidate[w][pos] = \
                            (abs(individual1[w][pos]+F*(individual2[w][pos] -
                                                        individual3[w][pos])) %
                             tamanho_image[pos])

                if fitnessFunction(original, N, image) < \
                        fitnessFunction(candidate, N, image):
                    population.remove(original)
                    population.append(candidate)

                j += 1

        i = 0
        bestFitness = [[0, 0]] * N
        while(i < PopulationSize):
            individual = population[i]
            if fitnessFunction(bestFitness, N, image) < \
                    fitnessFunction(individual, N, image):
                bestFitness = individual
            i += 1

        image = skimage.color.grey2rgb(image)
        for i in range(0, N):
            image[bestFitness[i][0]][bestFitness[i][1]] = [255, 0, 0]
        scipy.misc.imsave('output/'+path+'.bmp', image)

        lista.append('F= '+str(F)+', CR= '+str(CR) +
                     ', Pop= '+str(PopulationSize)+', Sement='+str(N))
        lista.writerows(lista)
