
# coding: utf-8

# In[1]:


import re
import random
import math


# In[4]:


class ConverterTextToVector:
    def __init__(self):
        self.dictionary = {}
        self.dictionaryNumberOfOccurrences = {}
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
        return(word)
    
    def getNumberOfWords(self):
        return (index+1)
    
    def getNumberOfWordsSeen(self):
        numberOfWordsSeen = 0
        for word in self.dictionary:
            numberOfWordsSeen += self.dictionary[word]
        return(numberOfWordsSeen)
    
    def considerWord(self,rawWord):
        word = self.clean(rawWord)
        if len(word) > 0:
            if not word in self.dictionary:
                self.dictionary[word] = 1
                self.index += 1
            else:
                self.dictionary[word] += 1
                
        pass
    
    def considerSentence(self,sentence):
        wordList = self.clean(sentence).split();
        for word in wordList:
            self.considerWord(word)
        pass
        
    
    def getIndexOfWord(self,rawWord):
        word = self.clean(rawWord)
        if not word in self.dictionary:
            return(-1)
        else:
            return(self.dictionary[mot])
        pass
    
    
    def getNumberOfWords(self):
        return(len(self.dictionary))
    
    
    def getVectorFromSentence(self,sentence):
        vector = [False]*self.getNumberOfWords()
        wordList = sentence.split()
        for rawWord in wordList:
            indexOfWord = self.getIndexOfWord(rawWord)
            if(indexMotActuel != -1):
                vector[word] = True
        return(vector)
    
    
    def getNumberOccurrencesVectorFromSentence(self,sentence):
        vector = [0]*self.getNumberOfWords()
        wordList = sentence.split()
        for rawWord in wordList:
            indexOfWord = self.getIndexOfWord(rawWord)
            if(indexMotActuel != -1):
                vector[word] = dictionary[word]
        return(vector)
    
    
    def prune(self,percentageToKeep,method = "information"):
        
        numberOfWords = self.getNumberOfWords()
        numberOfWordsSeen = self.getNumberOfWordsSeen()
        
        numberToKeep = int(percentageToKeep*len(self.dictionary))
        
        wordAndEvaluationList =  [None]*numberOfWords
        for word in self.dictionary:
            critera = 0
            if(method == 'information'):
                probability = float(self.dictionary[word])/float(numberOfWordsSeen)
                critera = -probability*math.log(probability)
            
        


# In[5]:


class FacebookMessengerReader:
    
    def __init__(self,pathToMessages):
        
        self.trackedAuthors = []
        
        self.converterTextToVector = None
        self.percentageMessagesToKeep = 1
        self.keepMessagesMethod = "random"
        self.percentageWordsToKeep = 1
        self.keepWordsMethod = "information"
        
        
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
         
    
    
    def getTrackedMessagesDictionnary(self):
        if(len(self.trackedAuthors) == 0):
            print("ERROR : No author is tracked. Please track at least one author with the trackAuthor method and try again")
            return(-1)
        
        
        dictionnaryTrackedMessages = {}
        for author in self.trackedAuthors:
            dictionnaryTrackedMessages[author] = self.messages[author]
        
        return(dictionnaryTrackedMessages)
    
    
    def getTrackedMessagesList(self,authorFormat = "none"):
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
            
    
    def setParametersMessagesToKeep(self,percentageMessagesToKeep, keepMethod = "random"):
        self.percentageMessagesToKeep = percentageMessagesToKeep
        self.keepMessagesMethod = keepMethod
        return(self.percentageMessagesToKeep)
    
    
    def setParametersWordsToKeep(self,percentageWordsToKeep, keepMethod = "information"):
        self.percentageWordsToKeep = percentageWordsToKeep
        self.keepWordsMethod = keepMethod
        return(self.percentageWordsToKeep)
    
    
    def getMatrixTrackedMessages(self,typeOutput = "int"):

        messagesList = self.getTrackedMessagesList("name")
        numberTrackedAuthors = self.getNumberTrackedAuthors()
        
        numberMessagesToKeep = int(self.percentageMessagesToKeep*self.getNumberTrackedMessages())
        messagesToKeep = [None]*numberMessagesToKeep

#        if(numberMessagesToKeep == self.getNumberTrackedMessages()):
#            indexLastMessage = 0
#            for author in self.trackedAuthors:
#                for message in self.messages[author]:
#                    messagesToKeep[indexLastMessage] = (author,message)
#                    indexLastMessage += 1
        
        if(self.keepMessagesMethod == "random"):
            messagesList = self.getTrackedMessagesList("id")
            random.shuffle(messagesList)
            messagesToKeep = messagesList[0:numberMessagesToKeep]
        
        elif(self.keepMessagesMethod == "equiprobability"):
            
            dictionaryTrackedMessages = self.getTrackedMessagesDictionnary()
            minimumNumberOfMessages = len(dictionaryTrackedMessages[self.trackedAuthors[0]])
            for author in self.trackedAuthors:
                minimumNumberOfMessages = min(minimumNumberOfMessages, len(dictionaryTrackedMessages[author]))
            
            
            
            numberIterations = 0
            for numberIterations in range(minimumNumberOfMessages):
                for i in range(numberTrackedAuthors):
                    author = self.trackedAuthors[i]
                    messagesToKeep[numberIterations*numberTrackedAuthors + i] = (i,self.messages[author][numberIterations])
                numberIterations += 1
            
            while(not messagesToKeep[len(messagesToKeep)-1]):
                messagesToKeep.pop()
        
        
        
        print(messagesToKeep)
            
        
        
        
        self.converterTextToVector = ConverterTextToVector()
        for author in self.trackedAuthors:
            for message in self.messages[author]:
                self.converterTextToVector.considerSentence(message)
            
            
