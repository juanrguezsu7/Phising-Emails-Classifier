import re

def divideDataset(filename, limit, firstOutputFilename, secondOutputFilename, keepFirstId, keepSecondId):
  delimiter = ';'
  data = []
  with open(filename, 'r', encoding = 'utf8') as file:
    data = file.readlines()
  data.remove(data[0])
  data = ''.join(data)
  data = data.split(delimiter)
  fullData = []
  for i in range(0, len(data), 2):
    if i + 2 >= len(data):
      break
    id = data[i + 2]
    id = re.sub(r'\n\d*', '', id)
    content = data[i + 1]
    content = re.sub(r'\n', '', content)
    fullData.append([content, id])
  firstData = fullData[:limit]
  secondData = fullData[limit:]
  with open(firstOutputFilename, 'w', encoding = 'utf8') as file:
    counter = 0
    if keepFirstId:
      file.write('Number;EmailText;EmailType\n')
    for i in firstData:
      if keepFirstId:
        file.write(str(counter) + delimiter + i[0] + delimiter + i[1] + '\n')
      else:
        file.write(i[0] + '\n')
      counter += 1
  with open(secondOutputFilename, 'w', encoding = 'utf8') as file:
    counter = 0
    if keepSecondId:
      file.write('Number;EmailText;EmailType\n')
    for i in secondData:
      if keepSecondId:
        file.write(str(counter) + delimiter + i[0] + delimiter + i[1] + '\n')
      else:
        file.write(i[0] + '\n')
      counter += 1

def comparePredictions(predictionFilename, correctFilename):
  with open(predictionFilename, 'r', encoding = 'utf8') as file:
    predictions = file.readlines()
  with open(correctFilename, 'r', encoding = 'utf8') as file:
    correct = file.readlines()
  correct = correct[1:]
  correct = [i.split(';')[2] for i in correct]
  correctCounter = 0
  for i in range(len(predictions)):
    if (predictions[i] == 'S\n' and correct[i] == 'Safe Email\n') or (predictions[i] == 'P\n' and correct[i] == 'Phishing Email\n'):
      correctCounter += 1
  print('Correct predictions: ' + str(correctCounter))
  print('Total predictions: ' + str(len(predictions)))
  print('Accuracy: {:.2f}%'.format(correctCounter / len(predictions) * 100))

#divideDataset('data/PH_train.csv', 15000, 'PH_train_1_test.csv', 'delete.csv', False, True)
comparePredictions('resumen_alu0101477596.csv', 'models/10000-5000/PH_train_2.csv')