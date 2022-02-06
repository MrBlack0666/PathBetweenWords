import nltk;
nltk.download('wordnet')
from nltk.corpus import wordnet;
import random
import queue
import os

def getShortestPathBetweenWords(startWord, endWord, banWords, notInFirstLoop, firstWordRelation):
  startWord.replace(" ", "_")
  parentWordDictionary = {}
  visitedWords = set()
  wordsQueue = queue.Queue(1000000)

  wordsQueue.put(startWord)
  parentWordDictionary[startWord] = ""
  firstLoop = notInFirstLoop
  
  while not wordsQueue.empty():
    currentWord = wordsQueue.get()
    visitedWords.add(currentWord)

    synsets = wordnet.synsets(currentWord)
    for synset in synsets:
      if synset.name().split(".")[0] == currentWord:
        #synonimy i antonimy
        if firstWordRelation <= 1:
          for synonym in synset.lemmas():
            synonymWord = synonym.name()
            if (synonymWord not in visitedWords) and (synonymWord not in banWords):
              if not firstLoop or synonymWord != endWord:
                visitedWords.add(synonymWord)
                parentWordDictionary[synonymWord] = currentWord
                wordsQueue.put(synonymWord)
            for antonym in synonym.antonyms():
              antonymWord = antonym.name()
              if (antonymWord not in visitedWords) and (antonymWord not in banWords):
                if not firstLoop or antonymWord != endWord:
                  visitedWords.add(antonymWord)
                  parentWordDictionary[antonymWord] = currentWord
                  wordsQueue.put(antonymWord)
        
        #hipernimy
        if firstWordRelation == 2 or firstWordRelation <= 0:
          hypernyms = synset.hypernyms()
          for hypernym in hypernyms:
            hypernymWord = hypernym.name().split(".")[0]

            if (hypernymWord not in visitedWords) and (hypernymWord not in banWords):
              if not firstLoop or hypernymWord != endWord:
                visitedWords.add(hypernymWord)
                parentWordDictionary[hypernymWord] = currentWord
                wordsQueue.put(hypernymWord)
        
        #hyponimy
        if firstWordRelation == 3 or firstWordRelation <= 0:
          hyponyms = synset.hyponyms()
          for hyponym in hyponyms:
            hyponymWord = hyponym.name().split(".")[0]

            if (hyponymWord not in visitedWords) and (hyponymWord not in banWords):
              if not firstLoop or hyponymWord != endWord:
                visitedWords.add(hyponymWord)
                parentWordDictionary[hyponymWord] = currentWord
                wordsQueue.put(hyponymWord)
        
        #meronimy
        if firstWordRelation == 4 or firstWordRelation <= 0:
          meronyms = synset.part_meronyms()
          for meronym in meronyms:
            meronymWord = meronym.name().split(".")[0]
            
            if (meronymWord not in visitedWords) and (meronymWord not in banWords):
              if not firstLoop or meronymWord != endWord:
                visitedWords.add(meronymWord)
                parentWordDictionary[meronymWord] = currentWord
                wordsQueue.put(meronymWord)

    if endWord in parentWordDictionary:
      break;
    firstLoop = False
    firstWordRelation = 0

  currentWord = endWord
  wordsChain = []
  while(currentWord != ""):
    wordsChain.append(currentWord)
    currentWord = parentWordDictionary.get(currentWord)
  wordsChain.reverse()

  return wordsChain

def findPathWithGivenLength(wordsChain, minLength, isFirstWordRelation):
  if len(wordsChain) >= minLength:
    return wordsChain
  
  while len(wordsChain) < minLength:
    randIndex = -1
    if(isFirstWordRelation):
      randIndex = random.randint(1, len(wordsChain) - 2)
    else:
      randIndex = random.randint(0, len(wordsChain) - 2)


    banWords = []
    firstWord = ""
    secondWord = ""
    for i in range(0, len(wordsChain)):
      if i == randIndex:
        firstWord = wordsChain[i]
      elif i == randIndex + 1:
        secondWord = wordsChain[i]
      else:
        banWords.append(wordsChain[i])
    
    newChain = getShortestPathBetweenWords(firstWord, secondWord, banWords, True, 0)

    for i in range(1, len(newChain) - 1):
      wordsChain.insert(randIndex + i, newChain[i])

  return wordsChain

def findRouteBetweenWords(startWord, endWord, routeLength, firstWordRelation):
  wordsChain = getShortestPathBetweenWords(startWord, endWord, [], False, firstWordRelation)
  wordsChain = findPathWithGivenLength(wordsChain, routeLength, firstWordRelation > 0)
  return wordsChain

def isValid(startWord, endWord, routeLength, firstRelation):
  synsetsStart = wordnet.synsets(startWord)
  synsetsEnd = wordnet.synsets(endWord)
  error = ""

  if(synsetsStart is None or len(synsetsStart) <= 0):
    error += "Złe słowo startowe\n"
  
  if(synsetsEnd is None or len(synsetsEnd) <= 0):
    error += "Złe słowo końcowe\n"

  if(not isinstance(routeLength, int)):
    error += "Długość ścieżki musi być liczbą całkowitą\n"
  
  if(not isinstance(firstRelation, int) or firstRelation < 0 or firstRelation > 4):
    error += "Relacja musi być podana jako liczba całkowita z zakresu <0-4>\n"
  
  return error

def application():
  errorMessage = ""
  while(True):
    os.system('clear')
    if errorMessage != "":
      print("Błąd: " + errorMessage)

    startWord = input("Podaj słowo startowe: ")
    endWord = input("Podaj słowo końcowe: ")
    routeLength = int(input("Podaj minimalną długość ścieżki: "))
    firstRelation = int(input("Jaka relacja:\n0 - brak\n1 - synonim\n2 - hyperonim\n3 - hyponim\n4 - meronim\n"))

    os.system('clear')
    print("łączenie z wordnet")
    wordnet.synsets("none")

    errorMessage = isValid(startWord, endWord, routeLength, firstRelation)

    if errorMessage == "":
      os.system('clear')
      print("wyszukiwanie...")
      wordsChain = findRouteBetweenWords(startWord, endWord, routeLength, firstRelation)
      os.system('clear')
      
      print("Znaleziona ścieżka o minimalnej długości " + str(routeLength) + " między słowami: " + startWord + " - " + endWord)
      print(wordsChain)
      print("\n\n\n Naciśnij Enter...")
      input()

if __name__ == "__main__":
  application()