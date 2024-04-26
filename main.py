from src.tokenizer import Tokenizer
from src.csvFormatter import CSVFormatter
from src.wordProbabilities import WordProbabilities
from src.predictor import Predictor

import sys

### CSV FORMATTER ###
'''csvFormatter = CSVFormatter()
csvFormatter.format('PH_train_1.csv', 'PH_train_1_formatted.csv', ';', True)

### TOKENIZER ###
tokenizer = Tokenizer()
data = tokenizer.tokenize('PH_train_1_formatted.csv', ';', 'vocabulario.txt', True)

wordProbabilities = WordProbabilities(tokenizer.getVocabularySize())
wordProbabilities.calculateWordProbabilities(data)
wordProbabilities.laplaceSmoothing()
wordProbabilities.dumpToFile('modelo_lenguaje_P.txt', 'Phishing Email')
wordProbabilities.dumpToFile('modelo_lenguaje_S.txt', 'Safe Email')
print()'''

### PREDICTOR ###
if len(sys.argv) != 4:
  print('Usage: python main.py <safeModelFilename> <phishingModelFilename> <corpusToClassifyFilename>')
  sys.exit(1)
predictor = Predictor(sys.argv[1], sys.argv[2])
predictor.predictFile(sys.argv[3], 'clasificacion_alu0101477596.csv', 'resumen_alu0101477596.csv')
