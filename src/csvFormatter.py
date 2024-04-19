from time import time
import re

class CSVFormatter:
  '''
  Class to format a CSV file.
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

  def format(self, inputFile: str, outputFile: str, delimiter: str, verbose: bool = False):
    '''
    Format a CSV file.
    '''
    startTime = time()
    if verbose:
      print('Formatting CSV file: ' + inputFile)
    data = []
    with open(inputFile, 'r', encoding = 'utf8') as file:
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
    finalData = []
    deleted = 0
    for i in fullData:
      content = i[0]
      content = content.lower()
      for regex in CSVFormatter.CLEAN_REGEXS:
        content = re.sub(regex, '', content)
      stopWordsRegex = '|'.join(CSVFormatter.STOP_WORDS)
      content = re.sub(r'\b(' + stopWordsRegex + r')\b', '', content)
      content = re.sub(r'\s+', ' ', content)
      content = content.strip()
      if len(content) == 0:
        deleted += 1
        continue
      if not content.isascii():
        deleted += 1
        continue
      finalData.append([content, i[1]])
    with open(outputFile, 'w', encoding = 'utf8') as file:
      for i in finalData:
        file.write(i[0] + delimiter + i[1] + '\n')
    if verbose:
      finishTime = time()
      print('Formatting CSV file finished on file: ' + outputFile)
      print('Deleted rows: ' + str(deleted))
      print('Time elapsed: {:.2f} seconds'.format(finishTime - startTime))