# mlp.py
# -------------

# mlp implementation
import util
PRINT = True

class MLPClassifier:
  """
  mlp classifier
  """
  def __init__( self, legalLabels, max_iterations):
    self.legalLabels = legalLabels
    self.type = "mlp"
    self.max_iterations = max_iterations
    self.hiddenWeights = {}
    for label in legalLabels:
      self.hiddenWeights[label] = util.Counter()

    
  def train( self, trainingData, trainingLabels, validationData, validationLabels ):
    for iteration in range(self.max_iterations):
      print "Starting iteration ", iteration, "..."
      for i in range(len(trainingData)):
          "*** YOUR CODE HERE ***"
          util.raiseNotDefined()
    
  def classify(self, data ):
    guesses = []
    for datum in data:
      # fill predictions in the guesses list
        vectors = util.Counter()
        for l in self.legalLabels:
          outHidden = self.sigmoid(dot(datum.values(), self.hiddenWeights[l])) 
          #List of feature values of the given datum
          vectors[l] = self.sigmoid(dot(outHidden, self.Weights[l]))
        guesses.append(vectors.argMax())
    return guesses