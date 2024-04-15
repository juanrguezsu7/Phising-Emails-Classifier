from nltk import word_tokenize, download
import re

class Tokenizer:
  '''
  Class to tokenize a file and generate a vocabulary file with the words found in the file.
  '''
  STOP_WORDS = ['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear', 'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may', 'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor', 'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since', 'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet', 'you', 'your']
  CLEAN_REGEXS = [
    r'[-,.?¿!¡´~{}/\'#^\\+$%&()*_:<>=@\[\]`]',
    r'\d',
    r'https?:\/\/|www',
    r'<.*?>',
    r'\w{20,}',
    r'[\x00-\x1F\x7F]'
  ]

  def __init__(self):
    '''
    Constructor of the Tokenizer class.
    '''
    download('punkt')

  def tokenize(self, fileName: str, delimiter: str, outputFile: str, verbose: bool = False) -> list:
    '''
    Tokenize a file and generate a vocabulary file with the words found in the file.
    '''
    if verbose:
      print('Tokenizing file: ' + fileName)
    data = []
    with open(fileName, 'r', encoding = 'utf8') as file:
      data = file.readlines()
    data.remove(data[0])
    data = "".join(data)
    data = data.split(delimiter)
    fullData = []
    for i in range(0, len(data), 2):
      if i + 2 >= len(data):
        break
      id = data[i + 2]
      id = re.sub(r'\n\d*', '', id)
      fullData.append([data[i + 1], id])
    words = {}
    for i in fullData:
      i[0] = i[0].lower()
      for regex in self.CLEAN_REGEXS:
        i[0] = re.sub(regex, '', i[0])
      stopWordsRegex = '|'.join(Tokenizer.STOP_WORDS)
      i[0] = re.sub(r'\b(' + stopWordsRegex + r')\b', '', i[0])
      i[0] = re.sub(r'\s+', ' ', i[0])
      if len(i[0]) == 0:
        fullData.remove(i)
        continue
      if not i[0].isascii():
        fullData.remove(i)
        continue
      rawWords = word_tokenize(i[0])
      for word in rawWords:
        if word in words:
          words[word] += 1
        else:
          words[word] = 1
    listWords = list(words.keys())
    listWords.sort()
    with open(outputFile, 'w', encoding = 'utf8') as file:
      file.write('Numero de palabras: ' + str(len(listWords)) + '\n')
      for word in listWords:
        file.write(word + '\n')
    if verbose:
      print('Tokenization finished on file: ' + outputFile)
    return fullData
    
