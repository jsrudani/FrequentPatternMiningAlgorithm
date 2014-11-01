#!/usr/bin/python -tt
#**********************
#* Author: Jigar S. Rudani
#* Progam Name: Dictionary for Vocab.txt
#* Current file: rudani2_apriori.py
#* Version: 1.0
#* 
#***********************
import sys
import math
import re
import os
from collections import defaultdict
from collections import Counter
from itertools import combinations
from operator import itemgetter

# Define a parseInputfile() function which parsed the Vocab file and get the Output as Key-Value Pair.
def parseInputfile(inputFilename):
    dictVocab = {}
    filePointer = open(inputFilename,"r")
    inputLine = filePointer.read().splitlines()
    for keyValue in inputLine:
        key = keyValue.split('\t')[0]
        dictVocab[key] = keyValue.split('\t')[1]
    filePointer.close()
    return dictVocab

# Define a parseTopicFile() function which parsed the TopicFile and get the Frequent Pattern out of each Topic.
def parseTopicFile(inputFilename,min_support_count):

    print("Topic file Name", inputFilename)
    transactionList = list()
    filePointer = open(inputFilename,"r")
    inputLine = filePointer.read().splitlines()
    for value in inputLine:
        transactions = frozenset([int(number) for number in value.rstrip().split(' ')])
        transactionList.append(transactions)
    listLen = len(transactionList)
    print("Item->Frequency",listLen)
    min_support = func_Mul(min_support_count,listLen)
    print("Item->Frequency",min_support)
    return transactionList,min_support,listLen

# Define a func_Mul() function which performs multiplication.
def func_Mul(min_support_count,listLen):
    a = (min_support_count * listLen)
    return int(a)

# Define a func_Powerset() function which produces all subsets for a given set.
def func_Powerset(iterable,itemSize):
  tempSet = list(iterable)  
  return list(combinations((tempSet), itemSize))  

# Define a func_PruneItems() function which performs pruning of ItemSet.
def func_PruneItems(transactionList,itemSet,listItemwithFreq,min_support):

    tempItemSet = set()
    itemsDict = defaultdict(int)

    for itm in itemSet:        
        for trans in transactionList:
            if(itm.issubset(trans)):
                itemsDict[itm] += 1

    for itm,freq in itemsDict.items():
        if(freq >= min_support):
            tempItemSet.add(itm)
            listItemwithFreq[itm] = freq
    
    return tempItemSet,listItemwithFreq

# Define a func_JoinItems() function which performs self join operation
def func_JoinItems(itemSet,tempItemSet,itemSize):

    tempSet = set()
    for item_1 in itemSet:
        for item_2 in itemSet:
            if (item_1 != item_2):
                if (len(item_1.intersection(item_2)) == (itemSize - 2)):
                    pwrSet = func_Powerset(item_1.union(item_2),itemSize - 1)
                    for eachSubset in pwrSet:
                        chkPwrSet = set(eachSubset).difference(set([]))
                        if (chkPwrSet in tempItemSet and chkPwrSet not in item_1 and chkPwrSet not in item_2):
                            tempSet.add(item_1.union(item_2))                    
    return tempSet

# Define a funcAprioriFreqPattern() function which parsed the Transaction and get the Frequent Patterns out of each Topic.
def funcAprioriFreqPattern(transactionList,min_support):

    itemSet = set()
    listItemwithFreq = defaultdict(int)
    itemSize = 2
    tempItemSet = set()
    tempCandidateItem = set()
    
    for trans in transactionList:
        for items in trans:
            itemSet.add(frozenset([items]))
    
    #print "\n<-- C1 Candidate Set -->\n"
    #func_DisplayCandidate(itemSet)
    LItemSet,listItemwithFreq = func_PruneItems(transactionList,itemSet,listItemwithFreq,min_support)
    #print "\n<-- L1 ItemSet -->\n"
    #func_DisplayListItemFreq(LItemSet,listItemwithFreq,itemSize - 1)
    while (LItemSet != set([])):
        tempItemSet = LItemSet
        tempCandidateItem = func_JoinItems(LItemSet,tempItemSet,itemSize)
        #print "\n<-- C(%d) Candidate Set -->\n" % itemSize
        #func_DisplayCandidate(tempCandidateItem)
        LItemSet,listItemwithFreq = func_PruneItems(transactionList,tempCandidateItem,listItemwithFreq,min_support)
        #print "<-- L(%d) ItemSet -->\n" % (itemSize)
        #func_DisplayListItemFreq(LItemSet,listItemwithFreq,itemSize)
        itemSize += 1
    return tempItemSet,listItemwithFreq

# Define a func_DisplayListItemFreq() function which displays the Frequent Item Sets.
def func_DisplayListItemFreq(LItemSet,listItemwithFreq,itemSize):
    if (LItemSet != set([])):
        print("<-- L(%d) ItemSet -->\n" % (itemSize))
        for item in LItemSet:
            for itm,freq in listItemwithFreq.items():
                if (list(item) == list(itm)):
                    print(itm,freq)
    print("\n")

# Define a func_DisplayCandidate() function which displays the Candidate Item Sets.
def func_DisplayCandidate(tempCandidateItem):
    if (tempCandidateItem != set([])):
        for candidateItem in tempCandidateItem:
            print(candidateItem)
    print("\n")

# Define a func_FormatFreqPattern() function which formats the Frequent Pattern [s] (space) [t1 (space) t2 (space) t3 (space) ...]
def func_FormatFreqPattern(listItemwithFreq,dt,indx,outputFreqPatternName,dictVocab):

    tempList = []
    patternDigitObj = re.compile('\d+')
    for items,freq in listItemwithFreq.items():
        tempList.append([freq,items])
    sorted_items= sorted(tempList,key=itemgetter(0),reverse=True)
    tempList = []

    for listItems in sorted_items:
        tempList.append([listItems[0],patternDigitObj.findall(str(listItems[1]))])
    func_redirecttoOutputFolder(tempList,dt,indx,outputFreqPatternName,dictVocab)

# Define a func_ClosedMaxPattern() function to find Closed and Maximal Pattern
def func_ClosedMaxPattern(listItemwithFreq,dt,indx,outputClosedPatternName,outputMaxPatternName,dictVocab):

    closedPattern = []
    maxPattern = []
    tempList = []
    isAppendClosedPattern = None
    isAppendMaxPattern = None
    patternDigitObj = re.compile('\d+')
    for items,freq in listItemwithFreq.items():
        tempList.append([freq,items])
    sorted_items= sorted(tempList,key=itemgetter(0),reverse=True)

    for listItems_1 in sorted_items:
        isAppendClosedPattern = True
        isAppendMaxPattern = True
        for listItems_2 in sorted_items:
            if (listItems_1[1] not in listItems_2[1]):
                if (listItems_2[1] > listItems_1[1]):
                    isAppendMaxPattern = False
                    if (listItems_2[0] == listItems_1[0]):
                        isAppendClosedPattern = False
        if (isAppendClosedPattern):
            closedPattern.append([listItems_1[0],patternDigitObj.findall(str(listItems_1[1]))])
        if (isAppendMaxPattern):
            maxPattern.append([listItems_1[0],patternDigitObj.findall(str(listItems_1[1]))])
    func_redirecttoOutputFolder(closedPattern,dt,indx,outputClosedPatternName,dictVocab)
    func_redirecttoOutputFolder(maxPattern,dt,indx,outputMaxPatternName,dictVocab)
        
# Define a func_Purity() function which purify the frequent pattern
def func_Purity(allTopicFreqPattern,indx,dtList,outputPurityFileName,dictVocab):

    purityDict = {}
    d_t = dtList[indx][0]
    maxLogTerm = 0.0
    pattern2bsearch = []
    f_t_p = 0.0
    topicIndex = 0
    f_tdash_p = 0.0
    d_t_tdashdict = []
    d_t_tdash = 1.0
    tempMaxLogTerm = 0.0
    purity = 0.0
    tempTopicPurityList = []
    sortbysupport = []
    finalpuritylist = []
    puritylist = []
    isAppend = False
    purtiy_support_combine = 0.0

    for items in allTopicFreqPattern:
        maxLogTerm = 0.0
        firstfactor = 0.0
        purity = 0.0
        if (items[0] == indx):
            pattern2bsearch = items[2]
            f_t_p = items[1]
            for allItems in allTopicFreqPattern:
                if (allItems[0] != indx):
                    topicIndex = allItems[0]
                    if ((len(frozenset(pattern2bsearch).intersection(frozenset(allItems[2])))) == len(pattern2bsearch)):
                        f_tdash_p = allItems[1]
                    else:
                        f_tdash_p = 0.0
                    d_t_tdashdict = dtList[indx][1]
                    for value in d_t_tdashdict:
                        for key,val in value.items():
                            if(key == topicIndex):
                                d_t_tdash = val
                                break
                    tempMaxLogTerm = float((float(f_t_p) + float(f_tdash_p))/float(d_t_tdash))
                    if(float(tempMaxLogTerm) > float(maxLogTerm)):
                        maxLogTerm = float(tempMaxLogTerm)
            firstfactor = float(f_t_p)/float(d_t)
            purity = math.log(float(firstfactor)) - math.log(float(maxLogTerm))
            purtiy_support_combine = (float(purity) * math.log10(float(f_t_p)))
            tempTopicPurityList.append([round(purity,4),purtiy_support_combine,items[2]])
            #puritylist.append(round(purity,4))
    #purityDict = Counter(puritylist)
    #for key in purityDict.keys():
    #    sortbysupport = []
    #    for (index, tlist) in enumerate(tempTopicPurityList):
    #        if index < len(tempTopicPurityList) - 1:
    #            current = tlist
    #            if(key == current[0]):
    #                sortbysupport.append(current)
    #        elif(key == tlist[0]):
    #            sortbysupport.append(tlist)
    tempTopicPurityList = sorted(tempTopicPurityList, key=itemgetter(1), reverse=True)
    for items in tempTopicPurityList:
        finalpuritylist.append([items[0],items[2]])
    #finalpuritylist = sorted(finalpuritylist,reverse=True)
    func_redirecttoOutputFolder(finalpuritylist,dtList,indx,outputPurityFileName,dictVocab)

# Define a func_Completeness() function which finds the completeness of the pattern.
def func_Completeness(listItemwithFreq,dt,indx,outputCompletenessFileName,dictVocab):

    completenessList = []
    patternDigitObj = re.compile('\d+')
    tempsortbysupportList = []
    completenessDict = {}
    tempcompletenessList = []
    sortbysupport = []

    for item1,freq1 in listItemwithFreq.items():
        f_t_p = freq1
        freqList = []
        for item2,freq2 in listItemwithFreq.items():
            if (item1 not in item2):
                if (item2 > item1):
                    freqList.append(freq2)
        if (len(freqList) == 0):
            maxfreq = 0
        else:
            maxfreq = max(freqList)
        result = 1 - (maxfreq/f_t_p)
        tempcompletenessList.append([float(result), f_t_p, patternDigitObj.findall(str(item1))])
        tempsortbysupportList.append(float(result))
    tempsortbysupportList = sorted(tempsortbysupportList,reverse=True)
    #print("tempsortbysupportList",tempsortbysupportList)
    completenessDict = Counter(tempsortbysupportList)
    #print(completenessDict)
    for key in completenessDict.keys():
        sortbysupport = []
        for (index, tlist) in enumerate(tempcompletenessList):
            if index < len(tempcompletenessList) - 1:
                current = tlist
                if(key == current[0]):
                    sortbysupport.append(current)
            elif(key == tlist[0]):
                sortbysupport.append(tlist)
        sortbysupport = sorted(sortbysupport,key=itemgetter(1),reverse=True)
        #print(sortbysupport)
        for items in sortbysupport:
            completenessList.append([round(items[0],4),items[2]])
    #print(completenessList)
    completenessList = sorted(completenessList,key=itemgetter(0),reverse=True)
    #print(completenessList)
    func_redirecttoOutputFolder(completenessList,dt,indx,outputCompletenessFileName,dictVocab)

# Define a func_Phraseness() function which re-rank the frequent pattern based on phraseness.
def func_Phraseness(allTopicFreqPattern,indx,dtList,outputPhrasenessFileName,dictVocab):

    d_t = dtList[indx][0]
    f_t_w = 0.0
    firstfactor = 0.0
    secondfactor = 0.0
    sumsecondfactor = 0.0
    result = 0.0
    f_t_p = 0.0
    f_t_w = 0.0
    phraseness = []
    tempphraseness = []
    sortbysupport = []
    phrasenessDict = {}
    for items in allTopicFreqPattern:
        firstfactor = 0.0
        if (items[0] == indx):
            pattern2bsearch = items[2]
            f_t_p = items[1]
            for word in pattern2bsearch:
                word2bsearch = [word]
                for trans in allTopicFreqPattern:
                    if (trans[0] == indx):
                        if ((len(frozenset(trans[2]).difference(frozenset(word2bsearch)))) == 0):
                            f_t_w = trans[1]
                secondfactor = math.log((float(f_t_w)/float(d_t)))
                sumsecondfactor = float(float(sumsecondfactor) + float(secondfactor))
            firstfactor = math.log((float(f_t_p)/float(d_t)))
            result = round(float(firstfactor) - float(sumsecondfactor),4)
            secondfactor = 0.0
            sumsecondfactor = 0.0
            tempphraseness.append([float(result), f_t_p, items[2]])
            sortbysupport.append(float(result))
    phrasenessDict = Counter(sortbysupport)
    for key in phrasenessDict.keys():
        sortbysupport = []
        for (index, tlist) in enumerate(tempphraseness):
            if index < len(tempphraseness) - 1:
                current = tlist
                if(key == current[0]):
                    sortbysupport.append(current)
            elif(key == tlist[0]):
                sortbysupport.append(tlist)
        sortbysupport = sorted(sortbysupport, key=itemgetter(1), reverse=True)
        for items in sortbysupport:
            phraseness.append([items[0], items[2]])
    phraseness = sorted(phraseness,key = itemgetter(0),reverse=True)
    func_redirecttoOutputFolder(phraseness, dtList, indx, outputPhrasenessFileName, dictVocab)

# Define a func_redirecttoOutputFolder() function which redirects the output to respective folder
def func_redirecttoOutputFolder(listItemwithFreq,dt,indx,outputFileName,dictVocab):

    phrase = "phrase"
    tempVocabList = []
    listlength = dt[indx][0]

    if(re.search(r'\bpattern\b',outputFileName)):
        filePath = os.getcwd()+"/Pattern/"+outputFileName
        filePathPhrase = os.getcwd()+"/Pattern/"+outputFileName+phrase
        dirPath = os.getcwd()+"/Pattern/"
    elif(re.search(r'\bclosed\b',outputFileName)):
        filePath = os.getcwd()+"/Closed/"+outputFileName
        filePathPhrase = os.getcwd()+"/Closed/"+outputFileName+phrase
        dirPath = os.getcwd()+"/Closed/"
    elif(re.search(r'\bmax\b',outputFileName)):
        filePath = os.getcwd()+"/Max/"+outputFileName
        filePathPhrase = os.getcwd()+"/Max/"+outputFileName+phrase
        dirPath = os.getcwd()+"/Max/"
    elif(re.search(r'\bpurity\b',outputFileName)):
        filePath = os.getcwd()+"/Purity/"+outputFileName
        filePathPhrase = os.getcwd()+"/Purity/"+outputFileName+phrase
        dirPath = os.getcwd()+"/Purity/"
    elif(re.search(r'\bpurityphraseness\b',outputFileName)):
        filePath = os.getcwd()+"/PhrasenessCompleteness/"+outputFileName
        filePathPhrase = os.getcwd()+"/PhrasenessCompleteness/"+outputFileName+phrase
        dirPath = os.getcwd()+"/PhrasenessCompleteness/"
    elif(re.search(r'\bcompleteness\b',outputFileName)):
        filePath = os.getcwd()+"/PhrasenessCompleteness/"+outputFileName
        filePathPhrase = os.getcwd()+"/PhrasenessCompleteness/"+outputFileName+phrase
        dirPath = os.getcwd()+"/PhrasenessCompleteness/"
    else:
        print("Not a valid expected file name\n")
        print("Expected either 1. pattern-0.txt 2. closed-0.txt 3. max-0.txt\n")
            
    if not os.path.exists(os.path.dirname(dirPath)):
        os.makedirs(dirPath)
    if((re.search(r'\bpurity\b',outputFileName)) or (re.search(r'\bpurityphraseness\b',outputFileName)) or (re.search(r'\bcompleteness\b',outputFileName))):
        with open(filePath, "w+") as f:
            for listItems in listItemwithFreq:
                f.write("%s\n" % listItems)

        with open(filePathPhrase, "w+") as f:
            for listItems in listItemwithFreq:
                tempVocabList = []
                for listSet in listItems[1]:
                    tempVocabList.append(dictVocab[listSet])
                f.write("%s %s\n" % (listItems[0],tempVocabList))
    else:
        with open(filePath, "w+") as f:
            for listItems in listItemwithFreq:
                f.write("%s %s\n" % (round(listItems[0]/listlength,4),listItems[1]))

        with open(filePathPhrase, "w+") as f:
            for listItems in listItemwithFreq:
                tempVocabList = []
                for listSet in listItems[1]:
                    tempVocabList.append(dictVocab[listSet])
                f.write("%s %s\n" % (round(listItems[0]/listlength,4),tempVocabList))

def main():

    allTopicFreqPattern = []
    patternDigitObj = re.compile('\d+')
    if len(sys.argv) <= 2:
        progName = sys.argv[0]
        print('\nusage: [%s] Vocab File Name Min_Support\n' % (progName))
        print('Vocab FileName: File in which mapping of number to word is stored')
        print('Min_Support: Minimum Support count required to find Frequent Pattern\n')
        exit
    else:
        inputFilename = sys.argv[1]
        min_support_count = sys.argv[2]
        print('InputFileName: ',inputFilename)
        dictVocab = parseInputfile(inputFilename)
    #Parse the topic0~4.txt
    fileIndex = [0,1,2,3,4]
    dt = [
            [10047,[{1:17326},{2:17988},{3:17999},{4:17820}]],
            [9674,[{0:17326},{2:17446},{3:17902},{4:17486}]],
            [9959,[{0:17988},{1:17446},{3:18077},{4:17492}]],
            [10161,[{0:17999},{1:17902},{2:18077},{4:17912}]],
            [9845,[{0:17820},{1:17486},{2:17492},{3:17912}]]
         ]
    for indx in fileIndex:
        transactionList,min_support,listLen = parseTopicFile('topic-'+str(indx)+'.txt',float(min_support_count))
        freqItemSet,listItemwithFreq = funcAprioriFreqPattern(transactionList,min_support)
        outputFreqPatternName = 'pattern-'+str(indx)+'.txt'
        outputClosedPatternName = 'closed-'+str(indx)+'.txt'
        outputMaxPatternName = 'max-'+str(indx)+'.txt'
        outputCompletenessFileName = 'completeness-'+str(indx)+'.txt'
        
        for key,value in listItemwithFreq.items():            
            allTopicFreqPattern.append([indx,value,patternDigitObj.findall(str(key))])

        func_FormatFreqPattern(listItemwithFreq,dt,indx,outputFreqPatternName,dictVocab)
        func_ClosedMaxPattern(listItemwithFreq,dt,indx,outputClosedPatternName,outputMaxPatternName,dictVocab)
        func_Completeness(listItemwithFreq,dt,indx,outputCompletenessFileName,dictVocab)

    Index = [0,1,2,3,4]
    for indx in Index:
        outputPurityFileName = 'purity-'+str(indx)+'.txt'
        outputPhrasenessFileName = 'purityphraseness-'+str(indx)+'.txt'
        func_Purity(allTopicFreqPattern,indx,dt,outputPurityFileName,dictVocab)
        func_Phraseness(allTopicFreqPattern,indx,dt,outputPhrasenessFileName,dictVocab)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()