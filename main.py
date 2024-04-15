from tokenizer import Tokenizer

tokenizer = Tokenizer()
data = tokenizer.tokenize('PH_train.csv', ';', 'vocabulario.txt', True)
print()
