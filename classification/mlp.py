# mlp.py
# -------------

# mlp implementation
import util
from numpy import random, exp
PRINT = True
     
class MLPClassifier:
  """
  mlp classifier
  """
  def __init__( self, legalLabels, max_iterations):
    self.legalLabels = legalLabels
    self.type = "mlp"
    self.max_iterations = max_iterations
    self.layerWeights = [100] #Number of neurons in layer
    self.outputWeights = {}
    for label in legalLabels:
      self.outputWeights[label] = util.Counter()
    for neuron in range(100):
      self.layerWeights[neuron] = {}
      for label in legalLabels:
        self.layerWeights[neuron][label] = util.Counter()
        for i in range(784):
          self.layerWeights[neuron][label] = 2*random.random() - 1  #Each neuron has a randomized Counter of weights for 784 features (28^2). Approx in range -1<x<1

  def sigmoid(self, x):
    return 1/(1+exp(-x))

  def sigmoid_derivative(self, x):
    return x*(1-x)

  def train( self, trainingData, trainingLabels, validationData, validationLabels ):
    for iteration in range(self.max_iterations):
      print "Starting iteration ", iteration, "..."
      for i in range(len(trainingData)):
          "*** YOUR CODE HERE ***"
          #util.raiseNotDefined()
          for neuron in range(self.layerWeights):
            scores = util.Counter()
            for label in legalLabels:
              scores[label] = sigmoid(self.layerWeights[neuron][label] * trainingData[i])

            guess = scores.argMax()
            correct = trainingLabels[i]

            if guess != correct:
              #Back propagation adjustment

    
  def classify(self, data ):
    guesses = []
    for datum in data:
      # fill predictions in the guesses list
      "*** YOUR CODE HERE ***"
      util.raiseNotDefined()
    return guesses