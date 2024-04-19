from src.tokenizer import Tokenizer
from src.csvFormatter import CSVFormatter
from src.wordProbabilities import WordProbabilities

### CSV FORMATTER ###
# csvFormatter = CSVFormatter()
# csvFormatter.format('data/PH_train.csv', 'data/PH_train_formatted.csv', ';', True)

### TOKENIZER ###
tokenizer = Tokenizer()
data = tokenizer.tokenize('data/PH_train_formatted.csv', ';', 'vocabulario.txt', True)

wordProbabilities = WordProbabilities(tokenizer.getVocabularySize())
wordProbabilities.calculateWordProbabilities(data)
wordProbabilities.laplaceSmoothing()
wordProbabilities.dumpToFile('modelo_lenguaje_P.txt', 'Phishing Email')
wordProbabilities.dumpToFile('modelo_lenguaje_S.txt', 'Safe Email')
print()
