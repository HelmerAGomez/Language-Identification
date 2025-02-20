import os
def convertToOctal(text, octalList):
   for char in text:
       charHex = str(char.encode("utf-8"))[1:].strip()
       if "\\x" in charHex:
           multi = charHex.split("\\x")[1:]
           for each in multi:
               h = each.strip("'")
               decimalValue = int(h, 16)
               octalValue = oct(decimalValue)
               octalList.append("\\"+octalValue[2:])
       else:
           octalList.append(charHex.strip("'"))
def kGrams(filename):
	map = {}
	file = open(filename)
	kLength = 3
	octal_list = []
	wholeText = file.read()
	convertToOctal(wholeText, octal_list)
	for x in range(len(octal_list)-kLength+1):
		currTrigram = ""
		for i in range(kLength):
			currTrigram += octal_list[x+i]
		map[currTrigram] = 1 + map.get(currTrigram, 0)
	file.close()
	return map
def normalize(map):
	normalizeSum = 0
	for key, value in map.items():
		normalizeSum += value**2
	for key,value in map.items():
		map[key] = (value/(normalizeSum**(1.0/2.0)))
def topKProfile(map1):
	kthElements = 41
	listm = []
	newMap = {}
	for key, value in map1.items():
		listm.append((value,key))
	listm.sort(reverse=True)
	for i in range(kthElements):
		newMap[listm[i][1]] = listm[i][0]
	return newMap

def cosineSimilarity(map1, map2):
	cosineSim = 0
	for key,value in map1.items():
		if key in map2:
			cosineSim += (map1[key] * map2[key])
	return cosineSim

def parsingFileToMap(StringFromFile):
	filestring = StringFromFile[:len(StringFromFile)-1]
	chunkString = ""
	twoQuotes = 0
	freqMap = {}
	trigramAndFreqList = []
	#consider " """, where there are more than two "
	for char in filestring:
		chunkString += char
		if char == "\"":
			twoQuotes += 1
		if twoQuotes > 1 and char == ",":
			trigramAndFreqList.append(chunkString)
			twoQuotes = 0
			chunkString = ""
	for m in trigramAndFreqList:
		m = m[:len(m)-1]
		m = m[::-1]
		smallList = m.split(":", 1)
		#reverse trigram
		trigram = smallList[1][::-1]
		#reverse the number
		freqMap[trigram[2:len(trigram)-1]] = float(smallList[0][::-1])
	return freqMap
def buildCorpus():
	allLanguageMaps = []
	languageFiles = os.listdir("corpora")
	os.chdir("corpora")
	languageMap = {}
	for languageFile in languageFiles:
		file3gram = open(languageFile)
		filestring = file3gram.read()
		freqMap = parsingFileToMap(filestring)
		normalize(freqMap)
		normalizeMap = topKProfile(freqMap)
		languageName = languageFile.replace(".3grams", "")
		allLanguageMaps.append((languageName,normalizeMap))
	file3gram.close()
	os.chdir("..")
	return allLanguageMaps

def languageGuess(unknownLanguageMap, ListOfallLanguages):
	mostLikelyLang = "Not enough data"
	highestSimilarity = 0
	for language in ListOfallLanguages:
		currSimilarity = cosineSimilarity(unknownLanguageMap, language[1]) 
		if currSimilarity > highestSimilarity:
			mostLikelyLang = language[0]
			highestSimilarity = currSimilarity
	return mostLikelyLang
def main():
	unkownfilesTexts = []
	ListOfallLanguages = buildCorpus()
	unkownfiles = os.listdir("textToIdentify")
	unkownfiles.sort()
	os.chdir("textToIdentify")
	for unkownFile in unkownfiles:
		print(unkownFile, end = " ")
		map1 = kGrams(unkownFile)
		normalize(map1)
		unknownLanguageMap = topKProfile(map1)
		print(languageGuess(map1, ListOfallLanguages))
	os.chdir("..")

main()
