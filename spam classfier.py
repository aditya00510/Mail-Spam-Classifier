#import Modules
import os
import re
import math
#from collections import Counter


#Pre-processing
def decontracted(phrase):
    phrase = re.sub(r"won't", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase

def preprocessFile(filename):
	words = []
	with open(filename, "r", errors="ignore") as file:
		filedata = file.readlines()
		for line in filedata:
			sent = decontracted(line)
			sent = sent.replace('\\r', ' ')
			sent = sent.replace('\\"', ' ')
			sent = sent.replace('\\n', ' ')
			sent = re.sub('[^A-Za-z0-9]+', ' ', sent)
			sent = ' '.join(e.lower() for e in sent.split())
			words += list(sent.strip().split())
	return words

def preprocess(filenames):
	words = []
	for filename in filenames:
		words += preprocessFile(filename)
	return words

def createFromWords(words):
	frequencies = [words.count(word) for word in words]
	return dict(list(zip(words, frequencies)))

def saveToCSV(dic, filename):
	with open(filename, "w+") as file:
		for word in dic.keys():
			file.write("%s %d\n" % (word, dic[word]))

def read_CSV(filename, datatype="float"):
	dic = {}
	with open(filename, "r") as file:
		filedata = file.readlines()
		for line in filedata:
			word, frequency = line.split(" ")
			if(datatype == "float"):
				dic[str(word)] = float(frequency)
			elif(datatype == "int"):
				dic[str(word)] = int(frequency)
			else:
				dic[str(word)] = frequency
	return dic

"""

# Train
print("Training : Started")
spamTrainPath = ".\\train\\spam\\"
hamTrainPath = ".\\train\\non-spam\\"
spamFilesList = [(spamTrainPath + fname) for fname in os.listdir(spamTrainPath)]
hamFilesList = [(hamTrainPath + fname) for fname in os.listdir(hamTrainPath)]


def create_dictionary(spamFilesList, isSpam):
	Dict1 = createDictionaryFromWords(preprocessFiles(spamFilesList))
	Dict2 = {}
	if isSpam:
		Dict2 = read_CSV(".\\main\\spam.csv", "int")
		Dict = Counter(Dict1) + Counter(Dict2)
		Dict = dict(Dict.most_common(5000))
		saveDictionaryToCSV(Dict, ".\\main\\spam.csv")
	else:
		Dict2 = read_CSV(".\\main\\non-spam.csv", "int")
		Dict = Counter(Dict1) + Counter(Dict2)
		Dict = dict(Dict.most_common(5000))
		saveDictionaryToCSV(Dict, ".\\main\\non-spam.csv")

def create_vocab():
	Dict1 = read_CSV(".\\main\\spam.csv", "int")
	Dict2 = read_CSV(".\\main\\non-spam.csv", "int")
	Dict = dict(Counter(Dict1) + Counter(Dict2))
	saveDictionaryToCSV(Dict, ".\\main\\vocabulary.csv")


# Progressive Learning
print("Training : Processing")
create_dictionary(spamFilesList, True)
create_dictionary(hamFilesList, False)
create_vocab()
print("Training : Completed")
"""
#Test

vocabulary = read_CSV(".\\main\\vocabulary.csv")
spam = read_CSV(".\\main\\spam.csv")
nonspam = read_CSV(".\\main\\non-spam.csv")

WordsCount = len(vocabulary)
CountSpam = len(spam)
Countnonspam = len(nonspam)
spampriorProb = 0.5
nonspampriorProb = 0.5
def predict(filename):
	testDict = createFromWords(preprocessFile(filename))

	testSpamProb = spampriorProb
	testnonspamProb = nonspampriorProb

	for word in testDict.keys():
		if word in spam.keys():
			wordSpamProb = (spam[word] + 1.0) / (CountSpam + WordsCount)
		else:
			wordSpamProb = (0.0 + 1.0) / (CountSpam + WordsCount)
		testSpamProb += math.log(wordSpamProb)
	
		if word in nonspam.keys():
			wordnonspamProb = (nonspam[word] + 1.0) / (Countnonspam + WordsCount)
		else:
			wordnonspamProb = (0.0 + 1.0) / (Countnonspam + WordsCount)
		testnonspamProb += math.log(wordnonspamProb)
	if(testSpamProb > testnonspamProb):
		print("Spam!")
		return 1
	else:
		print("Non-spam!")
		return 0

#prediction
print("Predicting the emails of test file:")
path = ".\\test\\"
for file in os.listdir(path):
	predict(path + file)
