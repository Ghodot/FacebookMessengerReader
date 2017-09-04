# FacebookMesssengerReader


##What is this ?

With this python class you can extract messages from your Facebook archive in an easy to process way.
It is mainly geared towards data science, as it allows you to get messages as bags of words, and allows different methods for selecting which words to use.
The data science section is at the end of the typical workflow section. You don't need to follow it if you just want to get messages as is.




##Requirements

This class is written in Python 3. It doesn't require any package.

To download your archive, you need to have a Facebook account, and to follow the instructions [https://www.facebook.com/help/131112897028467](here).



##Importing the class

Download the FacebookMesssengerReader.py file and place it where your main python file is. Then import it with the command

`import facebookMessengerReader`


##Typical workflow

The class has several methods you can use; you will find the exaustive list at the end of this guide. Here I will show you a typical workflow for working with the class.


###Instanciation
First, you need to instantiate the class. The constructor takes as only argument the path to the file 'messages.htm' from your archive, so don't forget to unzip it.

`fmr = facebookMessengerReader.FacebookMesssengerReader(path-to-your-messages-files)`

###Setting tracked authors
FacebookMesssengerReader works with the notion of tracked author. That is you will have to specify the authors present in your archive you want to study.
By default, no author is tracked.

If you want to get only the messages from "John Smith" and "Tommy Atkins" , run the following commands :

```
fmr.trackAuthor("John Smith")
fmr.trackAuthor("Tommy Atkins")
```

Or you can also run the equivalent :

```
fmr.trackMultipleAuthors(["John Smith","Tommy Atkins"])
```

If you want to track all the authors, that is every person / page you ever exchanged a message with through Facebook, you can run :
```
fmr.trackAllAuthors()
```

Finally, to remove authors from the tracked Authors list, you have access to the following methods :
```
fmr.stopTrackAuthor("John Smith")
fmr.stopTrackSeveralAuthors(["John Smith","Tommy Atkins"])
fmr.clearTrackedAuthors()
```


###Getting messages

As of today the class provides two methods to get messages.

####Getting messages as a dictionary
Simply run 
```
dictionary = fmr.getTrackedMessagesDictionary()
```
The keys of the dictionary are the tracked authors, and the element a list of all the messages found for this author

####Getting messages as a list
The method to get messages as a list,
```
list = fmr.getTrackedMessagesList(authorFormat)
```

takes one optionnal argument, specifying the format the authors are to be displayed in. This argument can be :
| `authorFormat` value | Element of the list format |
| --- | --- |
|`'name'` (default) | (Name of the author, message) |
|`'id'` | (id of the author in the list, message) |
|`'none'` | message |

If you choose the `id` option, number associated to an author is simply its position in the trackedAuthors list. You can read it with `fmr.trackedAuthors`


##Data science
This class was created with data science in mind, so it allows several methods to format your messages in order to easily feed them to a machine learning system.

###Settings parameters
You can specify parameters for 3 aspects : which words to keep, which messages to keep, and the format of the output.

####Parameters for words
You set the parameters for the words to keep with the `fmr.setParametersWordsToKeep(proportionWordsToKeep, keepMethod)` method.
The first argument is the proportion of words you want to keep out of the total number of words.
The `keepMethod` will determine a ranking method among the different words, and only the best `totalNumberOfWords*proportionWordsToKeep` will be kept.


| `keepMethod` value | Score used |
| --- | --- |
|`'frequency'` (default) | Total number of occurences of the word in all the kept messages |
|`'reversedFrequency'` | The opposite of the frequency |
|`'information'` | Probability of the word times the logarith of the probability |
|`'meanDistance'` | The opposite of the absolute value of the difference between the number of occurences of the word and the mean number of occurences over all the words |
|`'random'` | A random number |


####Parameters for messages
You set the parameters for the messages to keep with the `fmr.setParametersWordsToKeep(proportionMessagesToKeep, keepMethod)` method.
The first argument is the proportion of words you want to keep out of the total number of words.
The `keepMethod` will determine the way the messages will be kept.


| `keepMethod` value | Method used |
| --- | --- |
|`'random'` (default) | A random set of messages is chosen |
|`'equiprobability'` | Every tracked author will have the same number of messages in the set. With `numberMinMessages` the number of messages of the tracked author with the LESS messages, the number of messages kept is `min(numberMessages*proportionMessagesToKeep,numberMinMessages*numberTrackedAuthors)`|
|`'equiprobabilityNoShuffle'` | Same as `'equiprobability'`, but each group of `numberTrackedAuthors` messages will have only one message from each author |


####Parameters for the output
You set the parameters for the output with the `fmr.setParametersOutput(typeOutput)` method.
The type of the output corresponds to the values in the output matrix,where each column corresponds to a word and each line to a message.
The element of the matrix can be the following :

| `typeOutput` value | Matrix element |
| --- | --- |
|`'boolean'` (default) | The element (i,j) is True if the message i contains the word j , False if not|
|`'int'` | The element (i,j) is 1 if the message i contains the word j , 0 if not|
|`'numberOccurences'` | The element (i,j) is the number of times the word j appears in the message i|
|`'frequency'` | The element (i,j) is the number of times the word j appears in the message i, divided by the number of words in the message i|


###Data science workflow
Assuming you already took care of the tracked authors in the precedent workflow, here's an exemple to compute the matrix of messages :

```
fmr.setParametersMessagesToKeep(0.1,'equiprobability')
fmr.setParametersWordsToKeep(0.5,'meanDistance')
fmr.setParametersOutput('int')
output = fmr.compute()
```

The `fmr.compute()` returns a dictionary with the following elements :

* `matrixMessages` : The matrix described in the "Parameters for the output" part
* `arrayClasses` : An array describing the class of each kept messages as an int
* `intToAuthor` : A dictionary with the equivalence between the classes and the name of the authors
* `authorToInt` : A dictionary with the equivalence between the name of the authors and the corresponding class
* `textMessages` : An array of the original messages


