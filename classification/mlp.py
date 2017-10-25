# mlp.py
# -------------

# mlp implementation
import util
import math
from numpy import random, dot, exp, array, tanh, outer, subtract
PRINT = True

class Layer:
  def __init__(self, neurons, inputs):
    self.weights = 2 * random.random((inputs, neurons)) -1

class MLPClassifier:
  """
  mlp classifier
  """
  def __init__( self, legalLabels, max_iterations):
    self.legalLabels = legalLabels
    self.type = "mlp"
    self.max_iterations = max_iterations
    self.hidden = util.Counter() #Counter of hidden layer weights by label
    self.output = util.Counter() #Counter of output layer weights by label
    """
    self.hiddenWeights = util.Counter()
    self.weights = util.Counter()
    hidden = 2 * random.random((784, 100)) - 1
    output = 2 * random.random((100,1)) - 1
    for label in legalLabels:       #Initialize weights for each label, all with the same randomized values
      self.hiddenWeights[label] = hidden
      self.weights[label] = output
    """
  def setLayers(self, label, hidden, output):
    self.hidden[label] = hidden
    self.output[label] = output

  def sigmoid(self, x, derivative = False):
    if derivative:
      return x * (1-x)
    #return 1 / (1+exp(-x))
    return .5 * (1 + tanh(.5 * x))

  
  def train( self, trainingData, trainingLabels, validationData, validationLabels ):
    random.seed(1)
    hidden = Layer(100, 784)
    output = Layer(1, 100)
    labels = util.Counter() #Stores which training label # go into 0-9
    for l in self.legalLabels:
      self.setLayers(l, hidden, output)
      labels[l] = []
      #print self.hidden[l].weights
      #print self.output[l].weights
    for i in range(len(trainingLabels)):
      labels[trainingLabels[i]].append(i)
      

    for iteration in range(self.max_iterations):
      print "Starting iteration ", iteration, "..."
      correctLabel = 0
      for i in range(len(trainingData)):
        for label in self.legalLabels:
          if i in labels[label]:
            correctLabel = label
        #print "Dataset number: " , i
        #print "Correctlabel: ", correctLabel
        trainingInput = array(trainingData[i].values())
        trainingOutput = array(trainingLabels[i])

        hiddenOutput, realOutput = self.think(correctLabel, trainingInput)
        realError = subtract(trainingOutput, realOutput)#trainingOutput - realOutput
        realError = array(realError)
        realDelta = realError * self.sigmoid(realOutput, True)

        hiddenError = realDelta.dot(self.output[correctLabel].weights.T)
        hiddenDelta = hiddenError * self.sigmoid(hiddenOutput, True)

        adjustH =  outer(trainingInput.T, hiddenDelta)#trainingInput.dot(hiddenDelta) #
        adjustR =  outer(hiddenOutput.T, realDelta)#hiddenOutput.dot(realDelta) #
        """
        print hiddenOutput
        print hiddenError
        print hiddenDelta
        print realOutput
        print realError
        print realDelta
        print "adjustH: ", adjustH
        print "adjustR: ", adjustR
        """
        for labs in self.legalLabels:
          if labs != correctLabel:
            #print "weights -= with value: ", labs, " correctlabel: ", correctLabel
            self.hidden[labs].weights -= adjustH
            self.output[labs].weights -= adjustR
          else:
            #print "weights += with value: ", correctLabel
            self.hidden[correctLabel].weights += adjustH
            self.output[correctLabel].weights += adjustR
        
      """
      data = [] #5000 x 784
      for i in range(len(trainingData)):
          data.append(trainingData[i].values())
      data = array(data)
      outputs = array([trainingLabels])
      outputs = outputs.T

      hiddenOutput, outputOutput = self.think(data)
      outputE = outputs - outputOutput
      outputDelta = outputE * self.sigmoid(outputOutput, True)

      hiddenE = outputDelta.dot(self.output.weights.T)
      hiddenDelta = hiddenE * self.sigmoid(hiddenOutput, True)
      
      adjustH = data.T.dot(hiddenDelta)
      adjustO = hiddenOutput.T.dot(outputDelta)
      #print adjustH
      #print adjustO
      #print self.hidden.weights
      #print self.output.weights
      self.hidden.weights += adjustH
      self.output.weights += adjustO
      #print self.hidden.weights
      #print self.output.weights
      """
  def think(self, label, input):
    output1 = self.sigmoid(dot(input, self.hidden[label].weights))
    output2 = self.sigmoid(dot(output1, self.output[label].weights))
    return output1, output2
      
        

  def classify(self, data ):
    #for l in self.legalLabels:
     # print self.hidden[l].weights
      #print self.output[l].weights
    guesses = []
    """
    print self.hidden.weights
    print self.output.weights
    for datum in data:
      # fill predictions in the guesses list
        
        vectors = util.Counter()
        for l in self.legalLabels:
          outHidden = self.sigmoid(dot(datum.values(), self.hiddenWeights[l])) 
          #List of feature values of the given datum
          vectors[l] = self.sigmoid(dot(outHidden, self.weights[l]))
        guesses.append(vectors.argMax())
        
        print type(datum)
        print datum.values()
        break
        hidden, guess = self.think(array(datum.values()))
        guesses.append(round(guess))
    print round(guess)
    """
    for datum in data:
      vectors = util.Counter()
      for l in self.legalLabels:
        hid, guess = self.think(l, array(datum.values()))
        vectors[l] = guess
      #print vectors
      guesses.append(vectors.argMax())
    return guesses