from src.tokenizer import Tokenizer

tokenizer = Tokenizer()
data = tokenizer.tokenize('data/PH_train.csv', ';', 'vocabulario.txt', True)
print()
