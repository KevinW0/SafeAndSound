import speech_recognition as sr
import pygame
from twilio.rest import Client

pygame.init()
SIZE=(1000,700)
screen=pygame.display.set_mode(SIZE)
state="MAINMENU"
FILE=("das.wav")
x=sr.Recognizer()
x.energy_threshold=4000
with sr.AudioFile(FILE) as feed:
    audioToAnalyze=x.record(feed)

analysisPhraseCount=[]
allHotPhrases=[]

#Pygame Objects
mainMenu=pygame.image.load("MainMenu.png")
posAnalysis=pygame.image.load("AnalysisYes.png")
smallCalibri=pygame.font.SysFont("Calibri",20)



def mainMenuCollisions(x, y, mouseButton, state):
    mouseHitRect=pygame.Rect(x, y , 1, 1)
    hitList=[(0,350,500,150)]
    collide=mouseHitRect.collidelist(hitList)
    if collide != -1 and mouseButton==1:
        if collide==0:
            state="ANALYSIS"
    return state

def posAnalysisCollisions(x, y, mouseButton, state):
    mouseHitRect=pygame.Rect(x, y, 1, 1)
    hitList=[(500,500,500,200),(260,500,240,200),(0,500,240,200)]
    collide=mouseHitRect.collidelist(hitList)
    if collide != -1 and mouseButton==1:
        if collide==0:
            state="MAINMENUBUTCLEAR"
            print ("MAINMENUWORKINGNNGNGNGJDNAIDSJBDIUASHIUDSAH")
        elif collide==1:
            state="WRITETRANS"
            print ("MAINMENUWORKINGNNGNGNGJDNAIDSJBDIUASHIUDSAH")
        elif collide==2:
            state="VIEWTRANS"
            print ("MAINMENUWORKINGNNGNGNGJDNAIDSJBDIUASHIUDSAH")
    return state

def clearAllLists():
    global allHotPhrases, analysisPhraseCount, queryList
    allHotPhrases=[]
    analysisPhraseCount=[]
    queryList=[]

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

def getVal(tup):
    """ getVal returns the (position+1) of the first 1 within a tuple.
        This is used because MOUSEBUTTONDOWN and MOUSEMOTION deal with
        mouse events differently
    """
    for i in range(3):
        if tup[i]==1:
            return i+1
    return 0


def pasteText (listPass):
    cx=300
    cy=300
    for x in listPass:
        x=str(x)
        final=smallCalibri.render(x, 1, (0,0,0))
        screen.blit(final,(cx, cy,100,100))
        cx+=10
        cx+=10

def pasteTextHorz(listPass):
    cx=0
    cy=200
    for x in listPass:
        x=str (x)
        final=smallCalibri.render(x, 1, (0,0,0))
        screen.blit(final,(cx, cy,100,100))
        cx+=100
        cy+=10




allHotPhrases, analysisPhraseCount= hotListCreation()
running=True
while running:
    button=0
    mx=-1
    my=-1
    for evnt in pygame.event.get():
        if evnt.type==pygame.QUIT:
            running=False
        elif evnt.type==pygame.MOUSEBUTTONDOWN:
            mx, my=evnt.pos
            button=evnt.button
            print ("WORKING")
        elif evnt.type==pygame.MOUSEMOTION:
            button=getVal(evnt.buttons)
            mx,my=evnt.pos
            print ("WORKING")

    if state=="ANALYSIS":
        screen.blit(posAnalysis,(0,0,1000,700))
        pygame.display.flip()
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
                 state="POSANALYSIS"
                 print ("stateChanged")
            print (queryList)
        except sr.UnknownValueError:
            final=""
            print (final)
        except sr.RequestError as e:
            final=""
            print (final)

    elif state=="POSANALYSIS":
        screen.blit(posAnalysis,(0,0,1000,700))
        state=posAnalysisCollisions(mx, my,button, state)
        pasteText (finalFlags)
        pygame.display.flip()


    elif state=="VIEWTRANS":
        screen.blit(posAnalysis,(0,0,1000,700))
        pasteTextHorz (queryList)
        state=posAnalysisCollisions(mx, my,button, state)
        pygame.display.flip()
        pygame.time.wait(3000)
        # state=="MAINMENUBUTCLEAR"

    elif state=="WRITETRANS":
        screen.blit(posAnalysis,(0,0,1000,700))
        transfile=open("trans.dat","w")
        newList=[]
        for x in queryList:
            newList.append(str(x)+"\n")
        transfile.write(x)
        transfile.close()
        state=posAnalysisCollisions(mx, my,button, state)
        # state="MAINMENUBUTCLEAR"

    elif state=="MAINMENUBUTCLEAR":
        clearAllLists()
        state="MAINMENU"
    elif state=="MAINMENU":
        screen.blit(mainMenu,(0,0,1000,700))
        state=mainMenuCollisions(mx, my, button, state)
    pygame.display.flip()
    print (state)
pygame.quit()
