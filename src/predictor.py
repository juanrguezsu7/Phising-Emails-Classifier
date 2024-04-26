from math import log
import re
from src.model import Model

class Predictor:
  STOP_WORDS = ['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear', 'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may', 'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor', 'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since', 'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet', 'you', 'your']
  CLEAN_REGEXS = [
    r'[-,.?¿!¡´~{}/\'#^\\+$%&()*_:<>=@\[\]`]',
    r'\d',
    r'https?:\/\/|www',
    r'<.*?>',
    r'\w{20,}',
    r'[\x00-\x1F\x7F]'
  ]

  def __init__(self, safeModelFilename, phishingModelFilename):
    self.safeModel = Model(safeModelFilename, 'Safe')
    self.phishingModel = Model(phishingModelFilename, 'Phishing')

  def predictFile(self, filename, outputFilename, summaryFilename = ''):
    summaryFile = None
    if summaryFilename != '':
      summaryFile = open(summaryFilename, 'w', encoding = 'utf8')
    with open(filename, 'r', encoding = 'utf8') as file:
      emails = file.readlines()
    with open(outputFilename, 'w', encoding = 'utf8') as file:
      for email in emails:
        formattedEmail = self.__formatEmail(email)
        prediction, emailSafeProb, emailPhishingProb = self.predict(formattedEmail)
        finalString = ''
        emailCharacters = email[0:10]
        emailCharacters = re.sub(r'\n', ' ', emailCharacters)
        emailCharacters = re.sub(r'<|>', '?', emailCharacters)
        finalString = '{0},{1},{2},{3}\n'.format(emailCharacters, emailSafeProb, emailPhishingProb, prediction)
        file.write(finalString)
        if summaryFilename != '':
          summaryFile.write('{0}\n'.format(prediction))
    if summaryFilename != '':
      summaryFile.close()
        
  def predict(self, text):
    text = text.split()
    safeProb = 0
    phishingProb = 0
    for word in text:
      safeProb += self.safeModel.getWordProbability(word)
      phishingProb += self.phishingModel.getWordProbability(word)
    totalMails = self.safeModel.totalMails + self.phishingModel.totalMails
    safeProb += log(self.safeModel.totalMails / totalMails)
    phishingProb += log(self.phishingModel.totalMails / totalMails)
    safeProbString = '{:.2f}'.format(safeProb)
    phishingProbString = '{:.2f}'.format(phishingProb)
    if safeProb > phishingProb:
      return 'S', safeProbString, phishingProbString
    return 'P', safeProbString, phishingProbString
  
  def __formatEmail(self, email):
    email = email.lower()
    for regex in Predictor.CLEAN_REGEXS:
      email = re.sub(regex, '', email)
    stopWordsRegex = '|'.join(Predictor.STOP_WORDS)
    email = re.sub(r'\b(' + stopWordsRegex + r')\b', ' ', email)
    email = re.sub(r'\s+', ' ', email)
    email = email.strip()
    if len(email) == 0:
      email = '<EMPTY>'
    if not email.isascii():
      email = '<NON-ASCII>'
    return email