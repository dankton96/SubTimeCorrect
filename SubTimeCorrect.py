import datetime,os,platform
os.system("python -m pip install -r requirements.txt")
import easygui
def ClearScreen():
    if platform.system()=='Linux':
        os.system("clear")
    if platform.system()=='Windows':
        os.system("cls")
numList=['0','1','2','3','4','5','6','7','8','9']
letterList=['a','b','c','ç','d','e','f','g','i','h','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','Ç','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
FilePath=easygui.fileopenbox("Selecione o arquivo a ser manipulado:")
file=open(FilePath,'r+')
sub=[]
################################################################################################
NumPos=[0,1,3,4,6,7,9,10,11,17,18,20,21,23,24,26,27,28]
CommaPos=[8,25]
ColonPos=[2,5,19,22]
def IsSubTime(tstr):
#    print(tstr)
    if(len(tstr)!=29):
        return False
    if(tstr[12:17]!=" --> "):
        return False
    for i in NumPos:
        if tstr[i] not in numList:
            return False
    for i in CommaPos:
        if tstr[i]!=',':
            return False
    for i in ColonPos:
        if tstr[i]!=':':
            return False
    return True
################################################################################################
#-00:00:00,000
def IsInputTime(tstr):
    if(len(tstr) not in [12,13]):
            return False
    if(tstr[0]=='-'):
        for i in [a+1 for a in NumPos[:9]]:
            if tstr[i] not in numList:
                return False
        j=CommaPos[0]+1
        if tstr[j]!=',':
            return False
        for i in [c+1 for c in ColonPos[:3]]:
            if tstr[i]!=':':
                return False
    else:
        for i in NumPos:
            if tstr[i] not in numList:
                return False
        for i in CommaPos:
            if tstr[i]!=',':
                return False
        for i in ColonPos:
            if tstr[i]!=':':
                return False
    return True
################################################################################################
for sc in file:
    sub.append(sc)
text=''
for i in sub:
    text+=str(i)
i=0
places2calc=[]
lines=text.splitlines()
for l in lines:
    if(IsSubTime(l)):
        places2calc.append(i)
        i+=1
    else:
        i+=1

instructions='''

*se deseja adiantar a legenda, comece o tempo pelo simbolo "-" (menos)
*o tempo a ser ajustado deve ser inserido no formato HH:MM:SS,sss
Onde: H=Horas, M=Minutos, S=Segundos, s=milissegundos

Insira o tempo a ser ajustado:
'''
TimeDifStr='+'
while((not IsInputTime(TimeDifStr)) or TimeDifStr=='\n'):
    ClearScreen()
    try:
        TimeDifStr=input(instructions)
    except:
        input("Tempo em formato invalido\nPressione enter para continuar")

if(TimeDifStr[0]=='-'):
    IsForward=True
    TimeDifStr=TimeDifStr[1:]
else:
    IsForward=False
TimeDifStr='10/10/2000 '+TimeDifStr
TimeDif=datetime.datetime.strptime(TimeDifStr, '%d/%m/%Y %H:%M:%S,%f')
for p in places2calc:
        p1Str='10/10/2000 '+lines[p][:12]
        p2Str='10/10/2000 '+lines[p][17:]
        p1=datetime.datetime.strptime(p1Str, '%d/%m/%Y %H:%M:%S,%f')
        p2=datetime.datetime.strptime(p2Str, '%d/%m/%Y %H:%M:%S,%f')
        if(IsForward):
            newP1=p1-TimeDif
            newP2=p2-TimeDif
            p1Str=str(newP1)
            p2Str=str(newP2)
        else:
            time_zero = datetime.datetime.strptime('00:00:00', '%H:%M:%S')
            newP1=(p1 - time_zero + TimeDif).time()
            newP2=(p2 - time_zero + TimeDif).time()
            p1Str=str(newP1)[:-3]
            p2Str=str(newP2)[:-3]
        newline=p1Str+' --> '+p2Str        
        i=0
        newline=newline.replace('.',',')
        lines[p]=newline
file.close()
ClearScreen()
newFile="CorrectedSub.srt"
file=open(newFile,'w')
for l in lines:
    file.write(l+'\n')
file.close()
