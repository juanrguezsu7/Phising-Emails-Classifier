class Model:
  def __init__(self, modelFilename, modelLabel):
    self.label = modelLabel
    with open(modelFilename, 'r') as file:
      self.totalMails = int(file.readline().split(':')[1])
      self.totalWords = int(file.readline().split(':')[1])
      self.words = {}
      for line in file:
        wordsInLine = line.split()
        self.words[wordsInLine[1]] = {'frec': int(wordsInLine[3]), 'prob': float(wordsInLine[5])}
  
  def getWordProbability(self, word):
    if word in self.words:
      return self.words[word]['prob']
    return self.words['<UNK>']['prob']
  
  def containsWord(self, word):
    return word in self.words
