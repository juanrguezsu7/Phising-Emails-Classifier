from math import log

class WordProbabilities:
  CLASSES_NAMES = ['Safe Email', 'Phishing Email']

  def __init__(self, vocabularySize):
    self.wordProbabilities = {}
    self.vocabulary = vocabularySize
    self.totalWords = {}
    self.totalEntries = {}

  def calculateWordProbabilities(self, tokenisedData, unknownParameter = 2):
    '''
    Calculate the probabilities of each word in the vocabulary to be in a class.
    '''
    for className in WordProbabilities.CLASSES_NAMES:
      self.totalWords.update({className: 0})
    for className in WordProbabilities.CLASSES_NAMES:
      self.totalEntries.update({className: 0})
    words = {}
    for i in tokenisedData:
      actualClass = i[1]
      self.totalEntries[actualClass] += 1
      for word in i[0]:
        self.totalWords[actualClass] += 1
        if words.get(word) == None:
          words.update({word: {}})
          for className in WordProbabilities.CLASSES_NAMES:
            words[word].update({className: 0})
        words[word][actualClass] += 1
    unknown = {'<UNK>': {}}
    for className in WordProbabilities.CLASSES_NAMES:
      unknown['<UNK>'].update({className: 0})
    toDelete = []
    for word in words:
      sum = 0
      for className in WordProbabilities.CLASSES_NAMES:
        sum += words[word][className]
      if sum < unknownParameter:
        toDelete.append(word)
        for className in WordProbabilities.CLASSES_NAMES:
          unknown['<UNK>'][className] += words[word][className]
    for word in toDelete:
      words.pop(word)
    words.update(unknown)
    self.wordProbabilities = words

  def laplaceSmoothing(self):
    '''
    Apply Laplace smoothing to the word probabilities.
    '''
    for word in self.wordProbabilities:
      for className in WordProbabilities.CLASSES_NAMES:
        self.wordProbabilities[word][className] += 1
        self.totalWords[className] += 1

  def getTotalWords(self):
    '''
    Get the total number of words.
    '''
    sum = 0
    for classSize in self.totalEntries:
      sum += self.totalWords[classSize]
    return sum

  def getWordProbabilities(self):
    '''
    Get the word probabilities.
    '''
    return self.wordProbabilities
  
  def getWordsClassified(self):
    '''
    Get the words classified.
    '''
    return self.totalWords

  def getEntriesClassified(self):
    '''
    Get the entries classified.
    '''
    return self.totalEntries

  def getTotalEntries(self):
    '''
    Get the total number of entries.
    '''
    sum = 0
    for classSize in self.totalEntries:
      sum += self.totalEntries[classSize]
    return sum

  def dumpToFile(self, filename, className):
    '''
    Dump the word probabilities to a file.
    '''
    with open(filename, 'w', encoding = 'utf8') as file:
      file.write('Numero de documentos (noticias) del corpus: {0}\n'.format(self.getEntriesClassified()[className]))
      file.write('Numero de palabras del corpus: {0}\n'.format(self.getWordsClassified()[className]))
      sortedWords = sorted(self.wordProbabilities.keys())
      for word in sortedWords:
        prob = log(self.wordProbabilities[word][className] / self.getWordsClassified()[className])
        file.write('Palabra: {0} Frec: {1} LogProb: {2:.2f}\n'.format(word, self.wordProbabilities[word][className], prob))
