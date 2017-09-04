# coding: utf-8

import re
import random
import math


class ConverterTextToVector:
    def __init__(self):
        self.wordToInt = {}
        self.intToWord = {}
        self.wordToNumberOfOccurrences = {}
        self.index = 0
        pass
    
    
    def clean(self,word):
        word = word.lower()
        word = word.replace('ç','c')
        word = word.replace('é','e')
        word = word.replace('è','e')
        word = word.replace('ê','e')
        word = word.replace('à','a')
        word = word.replace('â','a')
        word = word.replace('ù','u')
        word = word.replace('û','u')
        word = word.replace('î','i')
        word = word.replace('ô','o')
        word = word.replace('œ','oe')
        word = word.replace("&quot;","")
        word = re.sub('[^0-9a-zA-Z]+', ' ', word)
        word = word.strip()
        if(len(word) > 0 and (word[len(word)-1]== 's' or word[len(word)-1] == 'x')):
            word = word[0:(len(word)-1)]
        return(word)
    
    def getNumberOfWords(self):
        return (len(self.wordToInt))
    
    def getNumberOfWordsSeen(self):
        numberOfWordsSeen = 0
        for word in self.wordToInt:
            numberOfWordsSeen += self.wordToNumberOfOccurrences[word]
        return(numberOfWordsSeen)
    
    def considerWord(self,rawWord):
        word = self.clean(rawWord)
        if len(word) > 0:
            if not word in self.wordToInt:
                self.wordToNumberOfOccurrences[word] = 1
                self.wordToInt[word] = self.index
                self.intToWord[self.index] = word
                self.index += 1
            else:
                self.wordToNumberOfOccurrences[word] += 1
                
        pass
    
    def considerSentence(self,sentence):
        wordList = self.clean(sentence).split();
        for word in wordList:
            self.considerWord(word)
        pass
    
    def consider(self,sentenceOrWord):
        self.considerSentence(sentenceOrWord)
        
    
    def getIndexOfWord(self,rawWord):
        word = self.clean(rawWord)
        if not word in self.wordToInt:
            return(-1)
        else:
            return(self.wordToInt[word])
        pass
    
    def changeIndex(self,oldIndex,newIndex):
        wordToChange = self.intToWord[oldIndex]
        self.wordToInt[wordToChange] = newIndex
        self.intToWord[newIndex] = wordToChange
        
        self.intToWord.pop(oldIndex)
    
    
    def getNumberOfWords(self):
        return(len(self.wordToInt))
    
    
    def getBooleanVectorFromSentence(self,sentence):
        vector = [False]*self.getNumberOfWords()
        wordList = sentence.split()
        for rawWord in wordList:
            word = self.clean(rawWord)
            indexOfWord = self.getIndexOfWord(word)
            if(indexOfWord != -1):
                vector[indexOfWord] = True
        return(vector)
    
    
    def getNumberOccurrencesVectorFromSentence(self,sentence):
        vector = [0]*self.getNumberOfWords()
        wordList = self.clean(sentence).split();
        for rawWord in wordList:
            word = self.clean(rawWord)
            indexOfWord = self.getIndexOfWord(word)
            if(indexOfWord != -1):
                vector[indexOfWord] += 1
        return(vector)
    
    
    def prune(self,proportionToKeep,method = 'frequency'):
        
        numberOfWords = self.getNumberOfWords()
        numberOfWordsSeen = self.getNumberOfWordsSeen()
        mean = float(numberOfWordsSeen)/float(numberOfWords)
        
        numberToKeep = int(proportionToKeep*len(self.wordToInt))

        
        wordAndEvaluationList =  [None]*numberOfWords
        
        indexWord = 0
        for word in self.wordToInt:
            critera = 0
            if(method == 'information'):
                probability = float(self.wordToNumberOfOccurrences[word])/float(numberOfWordsSeen)
                critera = -probability*math.log(probability)
            elif(method == 'frequency'):
                critera = self.wordToNumberOfOccurrences[word]
            elif(method == 'reversedFrequency'):
                critera = -self.wordToNumberOfOccurrences[word]
            elif(method == 'meanDistance'):
                critera = -abs(self.wordToNumberOfOccurrences[word]-mean)
            elif(method == 'random'):
                critera = int(random.random())
                
            
            wordAndEvaluationList[indexWord] = (critera,self.wordToInt[word],word)
            indexWord += 1
        
        wordAndEvaluationList.sort(reverse = True)
        
        
        oldIntToWord = self.intToWord.copy()
        
        numberWordsRemoved = 0
        if(numberToKeep != numberOfWords):
            for i in range(numberToKeep,numberOfWords):
                wordToRemove = oldIntToWord[wordAndEvaluationList[i][1]]
                indexToRemove = self.wordToInt[wordToRemove]
            
                
                self.wordToInt.pop(wordToRemove)
                self.wordToNumberOfOccurrences.pop(wordToRemove)
                self.intToWord.pop(indexToRemove)
                
                if(indexToRemove != self.index - 1):
                    self.changeIndex(self.index-1,indexToRemove)
                self.index -= 1
                    
                numberWordsRemoved += 1
        
        
        return(numberWordsRemoved)
            
        


class FacebookMessengerReader:
    
    def __init__(self,pathToMessages):
        
        self.trackedAuthors = []
        
        self.converterTextToVector = None
        self.proportionMessagesToKeep = 1
        self.keepMessagesMethod = 'random'
        self.proportionWordsToKeep = 1
        self.keepWordsMethod = 'meanDistance'
        self.typeOutput = 'boolean'
        
        
        self.messages = {}
        self.faultyMessages = []
        
        with open(cheminHistorique, 'r', encoding="utf8") as myfile:
            data=myfile.read().replace('\n', '').replace('&#039;','\'')
            
        stringStartAuthor = "<span class=\"user\">"
        stringEndAuthor = "</span>"
        stringStartMessage = "<p>"
        stringEndMessage = "</p><div class=\"message\">"
                
        lenSA = len(stringStartAuthor)
        lenSM = len(stringStartMessage)
        lenEM = len(stringEndMessage)
        
        previousAuthor = "NONE"
        startOfSearchArea = 0
        
        numberCorrectMessages = 0
        

        while (data.find(stringStartAuthor,startOfSearchArea) != -1 and data.find(stringEndMessage,startOfSearchArea) != -1):
            indexBeginningAuthor = data.find(stringStartAuthor,startOfSearchArea)
            indexEndAuthor = data.find(stringEndAuthor,startOfSearchArea)
            indexBeginningMessage = data.find(stringStartMessage,startOfSearchArea)
            indexEndMessage = data.find(stringEndMessage,startOfSearchArea)
    
            author = data[(indexBeginningAuthor+lenSA):indexEndAuthor]
            if(author == ''):
                author = previousAuthor
            else:
                previousAuthor = author
    
            message = data[(indexBeginningMessage+lenSM):indexEndMessage]
        
    
            if(message.find('div') == -1 and len(message) > 0):
                numberCorrectMessages += 1
                if(author in self.messages):
                    self.messages[author].append(message)
                else:
                    self.messages[author] = [message]
            elif len(message) > 0:
                self.faultyMessages.append((author,message))

    
            startOfSearchArea = indexEndMessage + lenEM
        
        print("Number of messages integrated :",numberCorrectMessages)
        print("Number of faulty messages found :",len(self.faultyMessages))
        if(len(self.faultyMessages) > 0):
            print("You can review them invoking the .faultyMessages argument of the FacebookMessengerReader object.")
        
        print("Number of authors found : ",len(self.messages))
        
        
        pass
    
    def setEquivalent(self,authorToKeep,authorToDelete):
        if(not authorToKeep in self.messages):
            print("The first author provided didn't appear in the studied messages")
            return -1
        
        if(not authorToDelete in self.messages):
            print("The second author provided didn't appear in the studied messages")
            return -2
        
        if(authorToDelete in self.trackedAuthors):
            self.trackedAuthors.remove(authorToDelete)
            if not authorToKeep in self.trackedAuthors:
                print("WARNING : The deleted author",authorToDelete," was tracked, but the replacing author(",authorToKeep,"isn't. Maybe you'll want to track",authorToKeep)
            else:
                print("WARNING : The deleted author",authorToDelete," was tracked, however the replacing author",authorToKeep,"is tracked. No action is required")
        
        self.messages[authorToKeep].extend(self.messages[authorToDelete])
        numberMessagesTransferred = len(self.messages[authorToDelete])
        self.messages.pop(authorToDelete)
            
        print(numberMessagesTransferred,"messages successfully transfered from",authorToDelete,"to",authorToKeep)
        return(numberMessagesTransferred)
        
    
    def computeIntEquivalence(self):
        self.intToAuthor = {}
        self.authorToInt = {}
        
        i = 0
        for author in self.trackedAuthors:
            self.intToAuthor[i] = author
            self.authorToInt[author] = i
            i += 1
        
        pass
        
        
    def getNumberTrackedMessages(self):
        numberTrackedMessages = 0
        for author in self.trackedAuthors:
            numberTrackedMessages += len(self.messages[author])
        return(numberTrackedMessages)
    
    
    
    def trackAuthor(self,author):
        if not author in self.messages:
            print("ERROR : The author",author,"didn't appear in the studied messages")
            return(-1)
        elif author in self.trackedAuthors:
            print("WARNING : The author",author," is already tracked. Ignored")
            return(-2)
        else:
            self.trackedAuthors.append(author)
            return(0)
    
    def stopTrackAuthor(self,author):
        if(author in self.trackedAuthors):
            self.trackedAuthors.remove(author)
            return(0)
        else:
            print("ERROR : The author",author,"wasn't tracked")
            return(-1)
        
    
    def stopTrackMultipleAuthors(self,listAuthors):
        for author in listAuthors:
            self.stopTrackAuthor(author)
        return(len(self.trackedAuthors))
    
    
    def isAuthorTracked(self,author):
        return(author in self.trackedAuthor)
    
    def getNumberTrackedAuthors(self):
        return(len(self.trackedAuthors))
    
    def trackMultipleAuthors(self,listAuthors):
        for author in listAuthors:
            self.trackAuthor(author)
        return(len(self.trackedAuthors))
    
    def trackAllAuthors(self):
        for author in messages:
            self.trackAuthor(author)
        return(len(self.trackedAuthors))
    
        
    def getTrackedAuthors(self):
        return(self.trackedAuthors)
    
    def getNumberTrackedAuthors(self):
        return(len(self.trackedAuthors))
    
    
    def clearTrackedAuthors(self):
        self.trackedAuthors = []
        pass
         
    
    
    def getTrackedMessagesDictionary(self):
        if(len(self.trackedAuthors) == 0):
            print("ERROR : No author is tracked. Please track at least one author with the trackAuthor method and try again")
            return(-1)
        
        
        dictionaryTrackedMessages = {}
        for author in self.trackedAuthors:
            dictionaryTrackedMessages[author] = self.messages[author]
        
        return(dictionaryTrackedMessages)
    
    
    def getTrackedMessagesList(self,authorFormat = "name"):
        trackedMessagesList = [None]*self.getNumberTrackedMessages()
        indexCurrentMessage = 0
        
        if(authorFormat == "none"):
            for author in self.trackedAuthors:
                for message in self.messages[author]:
                    trackedMessagesList[indexCurrentMessage] = message
                    indexCurrentMessage += 1
        
        elif(authorFormat == "name"):
            for author in self.trackedAuthors:
                for message in self.messages[author]:
                    trackedMessagesList[indexCurrentMessage] = (author,message)
                    indexCurrentMessage += 1
                    
        elif(authorFormat == "id"):
            self.computeIntEquivalence()
            for author in self.trackedAuthors:
                idAuthor = self.authorToInt[author]
                for message in self.messages[author]:
                    trackedMessagesList[indexCurrentMessage] = (idAuthor,message)
                    indexCurrentMessage += 1
        
        else:
            print("ERROR : argument",authorFormat,"not recognized. Please refer to the documentation")
            return(-1)
        
        return(trackedMessagesList)
            
    
    def setParametersMessagesToKeep(self,proportionMessagesToKeep, keepMethod = "random"):
        self.proportionMessagesToKeep = proportionMessagesToKeep
        self.keepMessagesMethod = keepMethod
        return(self.proportionMessagesToKeep)
    
    
    def setParametersWordsToKeep(self,proportionWordsToKeep, keepMethod = 'meanDistance'):
        self.proportionWordsToKeep = proportionWordsToKeep
        self.keepWordsMethod = keepMethod
        return(self.proportionWordsToKeep)
    
    def setParametersOutput(self,typeOutput = 'boolean'):
        self.typeOutput = typeOutput
        pass
    
    
    
    def compute(self):

        messagesList = self.getTrackedMessagesList("name")
        numberTrackedAuthors = self.getNumberTrackedAuthors()
        
        numberMessagesToKeep = int(self.proportionMessagesToKeep*self.getNumberTrackedMessages())
        messagesTuplesToKeep = [None]*numberMessagesToKeep

        
        if(self.keepMessagesMethod == "random"):
            messagesList = self.getTrackedMessagesList("id")
            random.shuffle(messagesList)
            messagesTuplesToKeep = messagesList[0:numberMessagesToKeep]
        
        elif(self.keepMessagesMethod == "equiprobability" or self.keepMessagesMethod == "equiprobabilityNoShuffle"):
            dictionaryTrackedMessages = self.getTrackedMessagesDictionary()
            minimumNumberOfMessages = len(dictionaryTrackedMessages[self.trackedAuthors[0]])
            for author in self.trackedAuthors:
                minimumNumberOfMessages = min(minimumNumberOfMessages, len(dictionaryTrackedMessages[author]))
            
            
            numberIterations = 0
            while(numberIterations < minimumNumberOfMessages and numberIterations*numberTrackedAuthors + numberTrackedAuthors < numberMessagesToKeep):
                for i in range(numberTrackedAuthors):
                    author = self.trackedAuthors[i]
                    messagesTuplesToKeep[numberIterations*numberTrackedAuthors + i] = (i,self.messages[author][numberIterations])
                numberIterations += 1
            
            while(not messagesTuplesToKeep[len(messagesTuplesToKeep)-1]):
                messagesTuplesToKeep.pop()
            
            if(self.keepMessagesMethod == "equiprobability"):
                random.shuffle(messagesTuplesToKeep)
        
        
        
        self.converterTextToVector = ConverterTextToVector()
        
        for messageTuple in messagesTuplesToKeep:
            self.converterTextToVector.consider(messageTuple[1])
            
        print(len(self.converterTextToVector.intToWord))
        print(len(self.converterTextToVector.wordToInt))
        self.converterTextToVector.prune(self.proportionWordsToKeep,self.keepWordsMethod)
        print(len(self.converterTextToVector.intToWord))
        print(len(self.converterTextToVector.wordToInt))
        
        
        matrixMessages = []
        textMessages = []
        arrayClasses = []
        
        sizeVectors = self.converterTextToVector.getNumberOfWords()
        
        if(self.typeOutput == 'boolean'):
            for messageTuple in messagesTuplesToKeep:
                arrayClasses.append(messageTuple[0])
                matrixMessages.append(self.converterTextToVector.getBooleanVectorFromSentence(messageTuple[1]))
                textMessages.append(messageTuple[1])
                
        elif(self.typeOutput == 'int'):
            for messageTuple in messagesTuplesToKeep:
                arrayClasses.append(messageTuple[0])
                boolVector = self.converterTextToVector.getBooleanVectorFromSentence(messageTuple[1])
                for i in range(sizeVectors):
                    boolVector[i] = int(boolVector[i])
                matrixMessages.append(boolVector)
                textMessages.append(messageTuple[1])
                
        elif(self.typeOutput == 'numberOccurences'):
            for messageTuple in messagesTuplesToKeep:
                arrayClasses.append(messageTuple[0])
                matrixMessages.append(self.converterTextToVector.getNumberOccurrencesVectorFromSentence(messageTuple[1]))
                textMessages.append(messageTuple[1])
                
        elif(self.typeOutput == 'frequency'):
            numberOfWordsSeen = float(converterTextToVector.getNumberOfWordsSeen())
            for messageTuple in messagesTuplesToKeep:
                arrayClasses.append(messageTuple[0])
                numberOccurencesVector = self.converterTextToVector.getNumberOccurrencesVectorFromSentence(messageTuple[1])
                for i in range(sizeVectors):
                    numberOccurencesVector[i] = numberOccurencesVector[i]/len(messageTuple[1].split())
                matrixMessages.append(numberOccurencesVector)
                textMessages.append(messageTuple[1])
            
            
            
        
        
        
        return{'matrixMessages' : matrixMessages, 'arrayClasses' : arrayClasses, 'textMessages':textMessages,'intToAuthor' : self.intToAuthor, 'authorToInt' : self.authorToInt}
        
