import random
import numpy as np
import cv2
import matplotlib as plt

def sortByFitness(genomes):
    tuples = [(fitness(g), g) for g in genomes]
    tuples.sort()
    sortedFitnessValues = [f for (f, g) in tuples]
    sortedGenomes = [g for (f, g) in tuples]
    return sortedGenomes, sortedFitnessValues


# (x, y, height, width, img)

def randomGenome(windowHeight, windowWidth, image):
    x = random.randrange(0, windowWidth, 1)
    y = random.randrange(0, windowHeight, 1)
    height = random.randrange(0, windowHeight, 1)
    width = random.randrange(0, windowWidth, 1)
    return (x, y, height, width, image)

def makePopulation(size, windowHeight, windowWidth, images):
    pop = []
    website = []
    for i in range(size): #eg 5 websites
        for j in range(4):
            website.append(randomGenome(windowHeight, windowWidth, images[j]))
        pop.append(website)
    return pop

def fitness(website):
    fitness = 0
    for genome1 in website:
        for genome2 in website:
            if genome2 != genome1:
               #print(genome1[0])
#               print(genome1[0] - genome2[0])
               if (genome1[0] - genome2[0]) < 0:
                    fitness = fitness -1
               else:
                    fitness = fitness + 1
#    print(fitness)
    return fitness

def evaluateFitness(population):
    avgFitness = 0
    bestFitness = 0
    for website in population:
        fitnessLevel = fitness(website)
        avgFitness += fitnessLevel
        if fitnessLevel > bestFitness:
            bestFitness = fitnessLevel
    avgFitness = avgFitness / len(population)
    return avgFitness, bestFitness

#Function to crossover two genomes. 
def crossover(genome1, genome2):
    """
    :param genome1:
    :param genome2:
    :return: two new genomes produced by crossing over the given genomes at a random crossover point.
    """
    crossoverPoint = random.randint(1, len(genome1)-1) #Creates a random crossover point between one from the start of the genome and one from the end. 
    newgenome1 = genome1[0:crossoverPoint] + genome2[crossoverPoint:] #Creates a new genome using the first part of genome 1 and the second part of genome 2. 
    newgenome2 = genome2[0:crossoverPoint] + genome1[crossoverPoint:] #Creates a new genome using the first part of genome 2 and the second part of genome 1. 
    return newgenome1, newgenome2 #Returns the new genomes.

def mutate(genome, mutationRate, windowHeight, windowWidth):
    newGenome = []
    randNum = 0
    newElement = []
    for element in genome:
        randNum = random.random()
        if randNum < mutationRate:
            newElement.append(randomGenome(windowHeight, windowWidth, element[-1]))
            newGenome.append(newElement)
        else:
            newGenome.append(element)
#            element = randomGenome(windowHeight, windowWidth)
#        newGenome.append(element)
#    print(newGenome)
    return [newGenome]

#Function to select a pair of the population 
def selectPair(population):
    """

    :param population:
    :return: two genomes from the given population using fitness-proportionate selection.
    This function should use RankSelection,
    """
    cost = [] #List to hold the cost for each item in the population 
    weight = list(range(len(population)-1)) #List of weights that is essentially a list of numbers from 0 to the length of the population. 
    total = sum([w**2 for w in weight]) #Total sum of the weights squared.
    #Computes the cost based on each weight so that the greater values will have more weight. This works because the population is already sorted
    cost = [w**2/total for w in weight] 
    cost = [0] + cost #Sets the first element to have a cost of 0. 
    randNum = np.random.choice(population, p = cost) #Chooses a random element from the population based on the costs calculated above. 
    randNumTwo = np.random.choice(population, p = cost) #Chooses a random element from the population based on the costs calculated above. 
    return randNum, randNumTwo #Returns the random numbers

def add_obj(background, img, x, y):
    '''
    Arguments:
    background - background image in CV2 RGB format
    img - image of object in CV2 RGB format
    mask - mask of object in CV2 RGB format
    x, y - coordinates of the center of the object image
    0 < x < width of background
    0 < y < height of background
    
    Function returns background with added object in CV2 RGB format
    
    CV2 RGB format is a numpy array with dimensions width x height x 3
    '''
    
    bg = background.copy()
    
    h_bg, w_bg = bg.shape[0], bg.shape[1]
    
    h, w = img.shape[0], img.shape[1]
    
    # Calculating coordinates of the top left corner of the object image
    x = x[0] - int(w/2)
    y = y - int(h/2)    
        
    if x >= 0 and y >= 0:
    
        h_part = h - max(0, y+h-h_bg) # h_part - part of the image which overlaps background along y-axis
        w_part = w - max(0, x+w-w_bg) # w_part - part of the image which overlaps background along x-axis

        bg[y:y+h_part, x:x+w_part, :] = bg[y:y+h_part, x:x+w_part, :] + img[0:h_part, 0:w_part, :]
        
    elif x < 0 and y < 0:
        
        h_part = h + y
        w_part = w + x
        
        bg[0:0+h_part, 0:0+w_part, :] = bg[0:0+h_part, 0:0+w_part, :] + img[h-h_part:h, w-w_part:w, :]
        
    elif x < 0 and y >= 0:
        
        h_part = h - max(0, y+h-h_bg)
        w_part = w + x
        
        bg[y:y+h_part, 0:0+w_part, :] = bg[y:y+h_part, 0:0+w_part, :] + img[0:h_part, w-w_part:w, :]
        
    elif x >= 0 and y < 0:
        
        h_part = h + y
        w_part = w - max(0, x+w-w_bg)
        
        bg[0:0+h_part, x:x+w_part, :] = bg[0:0+h_part, x:x+w_part, :] + img[h-h_part:h, 0:w_part, :]
    
    return bg

#Function to run the genetic algorithm 
def runGA(populationSize, crossoverRate, mutationRate, windowHeight, windowWidth, logFile=""):
    """

    :param populationSize: :param crossoverRate: :param mutationRate: :param logFile: :return: xt file in which to
    store the data generated by the GA, for plotting purposes. When the GA terminates, this function should return
    the generation at which the string of all ones was found.is the main GA program, which takes the population size,
    crossover rate (pc), and mutation rate (pm) as parameters. The optional logFile parameter is a string specifying
    the name of a te
    """
    images = ["abstract image.png", "call to action.png", "developer image.png", "navbar.png"]
    background = cv2.imread('design background.png')
    background = cv2.cvtColor(background, cv2.COLOR_BGR2RGB)
    img = [cv2.imread(i) for i in images]
    img = [cv2.cvtColor(i, cv2.COLOR_BGR2RGB) for i in img]
    pop = makePopulation(populationSize, windowHeight, windowWidth, images) #Creates a population of the desired input size and with a genome length of 243. 
    print(pop)
#    if logFile != "": f = open(logFile, "w") #Opens a file if one is provided
    for j in range(3): #Loops through 300 iterations
        newPop = [] #Array to store the new population after selection, crossover, and mutation. 
        genList, fit = sortByFitness(pop) #Sorts the population using the provided function. 
 #       if not j%10:
  #          x = str(str(j) + '\t' + str(round(np.mean(fit), 2)) + "\t" + str(round(max(fit), 2))) + "\t" + genList[-1] + "\n"
   #         if logFile != "": f.write(x) #Writes the current values to the file
    #        print(x) #Prints the values to the terminal. 
        for i in range(int(populationSize/2)): #Loops through half of the population size
            #pair1, pair2 = selectPair(genList[int(cutoff*populationSize):]) #Selects a pair based on the performance of the population (it selects from the cutoff and onwards ).
            pair1 = genList[0]
            pair2 = genList[1]
  #          if random.random() < crossoverRate: #If a random number is less than the desired crossover rate, 
   #             pair1, pair2 = crossover(pair1, pair2) #Perform a crossover operation with the selected pairs
            pair1 = mutate(pair1, mutationRate, windowHeight, windowWidth) #Mutates based on the input mutation rate
            pair2 = mutate(pair2, mutationRate, windowHeight, windowWidth) #Mutates based on the input mutation rate
            #print(pair1)
            newPop.append(pair1) #Appends the new values to the new population
            newPop.append(pair2) 
#            print(pop[i][1])
#            composition_1 = [add_obj(background, a, pop[i][0], pop[i][1]) for a in img]
#            plt.figure(figsize=(15,15))
 #           [plt.imshow(c) for c in composition_1]
#            print(pair1)
        pop = newPop #Sets pop to equal the new population.
#    if logFile != "": f.close()
        print(newPop)
    return None


def test_FitnessFunction(strategy):
    f = fitness(strategy)
    print("Fitness for Strategy : {0}".format(f))


#rw.demo(rw.strategyM)
#test_FitnessFunction()
#rw.graphicsOff()
runGA(2, 1.0, 0.005, 500, 500) #Runs the GA with a population of 300, crossover of 1.0, and mutation rate of 0.5%
#rw.demo("655653226256251011354352015156153612150253603154063556053350206052652345235064452051050250055261443355136326104054624356660651153153142006303653250000366102505562156135250253252253614104406152114254150133253035114563635132115161653606166062344")

#Testing my best result against strategyM. I got fairly similar results. 
#test_FitnessFunction("655653226256251011354352015156153612150253603154063556053350206052652345235064452051050250055261443355136326104054624356660651153153142006303653250000366102505562156135250253252253614104406152114254150133253035114563635132115161653606166062344")
#print("==========================================")
#test_FitnessFunction(rw.strategyM)
