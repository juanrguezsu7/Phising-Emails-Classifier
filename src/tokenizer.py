from nltk import word_tokenize, download
from time import time

class Tokenizer:
  '''
  Class to tokenize a file and generate a vocabulary file with the words found in the file.
  '''
  FORBIDDEN_WORDS = ['<','>']
  SPECIAL_WORDS = ['EMPTY', 'NON-ASCII']

  def __init__(self):
    '''
    Constructor of the Tokenizer class.
    '''
    download('punkt')

  def tokenize(self, fileName: str, delimiter: str, outputFile: str, verbose: bool = False) -> list:
    '''
    Tokenize a file and generate a vocabulary file with the words found in the file.
    '''
    startTime = time()
    if verbose:
      print('Tokenizing file: ' + fileName)
    with open(fileName, 'r', encoding = 'utf8') as file:
      data = file.readlines()
    words = {}
    tokenisedData = []
    for i in data:
      i = i.split(delimiter)
      rawWords = word_tokenize(i[0])
      finalWords = rawWords
      for word in rawWords:
        if word in Tokenizer.FORBIDDEN_WORDS:
          continue
        if word in Tokenizer.SPECIAL_WORDS:
          finalWords = ['<' + word + '>']
          word = '<' + word + '>'
        if word in words:
          words[word] += 1
        else:
          words[word] = 1
      tokenisedData.append([finalWords, i[1].replace('\n', '')])
    listWords = list(words.keys())
    listWords.sort()
    with open(outputFile, 'w', encoding = 'utf8') as file:
      file.write('Numero de palabras: ' + str(len(listWords)) + '\n')
      for word in listWords:
        file.write(word + '\n')
    if verbose:
      finishTime = time()
      print('Tokenization finished on file: ' + outputFile)
      print('Time elapsed: {:.2f} seconds'.format(finishTime - startTime))
    self.vocabSize = len(listWords)
    return tokenisedData
    
  def getVocabularySize(self) -> int:
    '''
    Get the size of the vocabulary.
    '''
    return self.vocabSize