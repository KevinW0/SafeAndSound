import speech_recognition as sr
import pygame
from twilio.rest import Client

pygame.init()
SIZE=(1000,700)
screen=pygame.display.set_mode(SIZE)
frontEndState="MAINMENU"
FILE=("das.wav")
x=sr.Recognizer()
x.energy_threshold=4000
with sr.AudioFile(FILE) as feed:
    audioToAnalyze=x.record(feed)
state="ANALYSIS"

analysisPhraseCount=[]
allHotPhrases=[]


def hotListCreation():
    hotlist=[]
    hotListFile=open("hotwords.dat","r")
    while True:
        dataLine=hotListFile.readline().rstrip("\n")
        if dataLine=="":
            break
        else:
            tempList=[]
            tempList=dataLine.split(" ")
            phraseCount=len(tempList)
            analysisPhraseCount.append(phraseCount)
            allHotPhrases.append (tempList)
    return allHotPhrases,analysisPhraseCount

def algorithmCheck(fulltranscript,hotphraselist,corrospondingphrasequantitylist):
    resultList=[]
    for x in range (0,len(hotphraselist)):
        hotphrasecurrent=hotphraselist[x]
        #print (hotphrasecurrent)
        wordgroupquantity=corrospondingphrasequantitylist[x]
        secondrange=wordgroupquantity
        firstrange=0
        while secondrange != len(fulltranscript)+1:
            comparison=fulltranscript[firstrange:secondrange]
            if comparison==hotphrasecurrent:
                resultList.append(comparison)
                print ("WORKING")
                firstrange+=1
                secondrange+=1
            elif comparison[firstrange:secondrange]!=hotphraselist[0:]:
                firstrange+=1
                secondrange+=1
    return resultList

def text(message):
  account_sid = "REDACTED"
  auth_token = "REDACTED"

  client = Client(account_sid, auth_token)

  client.messages.create(from_="REDACTED",
                        to="REDACTED",
                        body=message)


allHotPhrases, analysisPhraseCount= hotListCreation()
while True:
    if state=="ANALYSIS":
        words=""
        try:
            final=x.recognize_sphinx(audioToAnalyze)
            queryList=final.split(" ")
            finalFlags=algorithmCheck(queryList,allHotPhrases, analysisPhraseCount)
            if len(finalFlags)!=0:
                 print (finalFlags)
                 for x in finalFlags:
                     words+=str(x)+" "
                 text("WARNING: YOUR FOLLOWING FLAGS HAVE BEEN HEARD @ BRAMPTON CITY HALL:"+words)
                 break
            print (queryList)
        except sr.UnknownValueError:
            final=""
            print (final)
        except sr.RequestError as e:
            final=""
            print (final)
