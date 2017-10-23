# svm.py
# -------------

# svm implementation
import util
from sklearn import svm
PRINT = True

class SVMClassifier:
  """
  svm classifier
  """
  def __init__( self, legalLabels):
    self.legalLabels = legalLabels
    self.type = "svm"
    self.svm = svm.LinearSVC()
      
  def train( self, trainingData, trainingLabels, validationData, validationLabels ):
    # print "Starting iteration ", iteration, "..."
    data = []
    for i in range(len(trainingData)):
      data.append(trainingData[i].values())
    self.svm.fit(data, trainingLabels)
        
    
  def classify(self, data ):
    '''guesses = []
    for datum in data:
      # fill predictions in the guesses list
      vectors = util.Counter()
      for l in self.legalLabels:
        vectors[l] = self.svm.predict(datum.values())
      guesses.append(vectors.argMax())
      
    return guesses
    '''
    guesses = []
    for i in range(len(data)):
      guesses.append(data[i].values())
    results = self.svm.predict(guesses)
    return results

