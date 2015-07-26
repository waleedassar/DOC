import os,sys,time,re,base64
from random import randint


if len(sys.argv) != 2:
    print "Usage: SplitByBoundary.py input_file_here\r\n"
    sys.exit(-1)


inF = sys.argv[1]

if os.path.exists(inF)==False or os.path.getsize(inF)==0:
    print "File does not exist or empty\r\n"
    sys.exit(-1)

def IsHexChar(CharX):
    if CharX != "0" and CharX != "1" and CharX != "2" and CharX != "3" and CharX != "4" and CharX != "5" and CharX != "6" and CharX != "7" and CharX != "8" and CharX != "9" and CharX != "A" and CharX != "a" and CharX != "B" and CharX != "b" and CharX != "C" and CharX != "c" and CharX != "D" and CharX != "d" and CharX != "E" and CharX != "e" and CharX != "F" and CharX != "f":
        return False
    return True

def NormalizeFile(FileName):
    fileName,fileExt = os.path.splitext(FileName)
    NewFileName = fileName + ".tmp"
    fOut = open(NewFileName,"w")
    fIn = open(FileName,"r")
    fCon = fIn.read()
    fIn.close()
    LenX = len(fCon)
    i = 0
    while i < LenX:
        if i + 3 <= LenX:
            Con_ = fCon[i:i+2]
            Con__ = fCon[i:i+3]
            if Con_ == "\r\t" or Con_ == "\n\t":
                fOut.write(" ")
                i = i + 1
                continue
            elif Con__ == "\r\n\t":
                fOut.write(" ")
                i = i + 3
                continue
            else:
                fOut.write(fCon[i])
        else:
            fOut.write(fCon[i])
        i = i + 1
        
    fOut.close()
    return NewFileName


inFF = NormalizeFile(inF)

fIn = open(inFF,"r")

boundary = ""


def DecodeQuotedPrintable(PayLoad,NewFileName):
    fOut = open(NewFileName,"w")
    lenX = len(PayLoad)
    NewPayLoad = ""
    i = 0
    while i < lenX:
        if PayLoad[i]=="=":
            if i + 3 <= lenX:
                HuH = PayLoad[i+1:i+3]
                if IsHexChar(HuH[0])==True and IsHexChar(HuH[1])==True:
                    HuH_x = int(HuH,16)
                    HuH_xx = chr(HuH_x)
                    fOut.write(HuH_xx)
                    NewPayLoad += HuH_xx
                    i = i + 3
                    continue
                if HuH[0] == "\r" and HuH[1] == "\n":
                    i = i + 3
                    continue
                i = i + 1
            fOut.write(PayLoad[i])
            NewPayLoad += HuH_xx
            i = i + 1
        else:
            fOut.write(PayLoad[i])
            NewPayLoad += HuH_xx
            i = i + 1
    fOut.close()
    return NewPayLoad
    

    
def DecodeByContentType(Type,PayLoad,NewFileName):
    TypeX = Type.lower().rstrip().lstrip()
    if TypeX == "quoted-printable":
        print "Decoding and dumping \"quoted-printable\""
        fOut = open(NewFileName,"w")
        lenX = len(PayLoad)
        i = 0
        while i < lenX:
            if PayLoad[i]=="=":
                if i + 3 <= lenX:
                    HuH = PayLoad[i+1:i+3]
                    if IsHexChar(HuH[0])==True and IsHexChar(HuH[1])==True:
                        HuH_x = int(HuH,16)
                        HuH_xx = chr(HuH_x)
                        fOut.write(HuH_xx)
                        i = i + 3
                        continue
                    if HuH[0] == "\r" and HuH[1] == "\n":
                        i = i + 3
                        continue
                    i = i + 1
                fOut.write(PayLoad[i])
                i = i + 1
            else:
                fOut.write(PayLoad[i])
                i = i + 1
        fOut.close()
    elif TypeX == "base64":
        print "Decoding and dumping \"base64\""
        fOut = open(NewFileName,"wb")
        #remove newlines
        PayLoadX = ""
        LenXZ = len(PayLoad)
        i = 0
        while i < LenXZ:
            if PayLoad[i]!="\r" and PayLoad[i]!="\n":
                PayLoadX += PayLoad[i]
            i = i + 1
        decoded = base64.b64decode(PayLoadX)
        fOut.write(decoded)
        fOut.close()      
    return 0
                
def GetFile(Content):
    Lines = []
    LenXX = len(Content)
    i = 0
    c = 0
    while i < LenXX:
        if Content[i]=="\x0D" or Content[i]=="\x0A":
            Lines.append(Content[c:i])
            while i < LenXX and (Content[i]=="\x0D" or Content[i]=="\x0A"):
                i = i + 1
            c = i # update for second line
        else:
            i = i + 1

    TheNewFileName = ""
    if len(Lines)!=0:
        for lineX in Lines:
            lineXX = lineX.lower().rstrip().lstrip()
            if lineXX.find("content-transfer-encoding:")!=-1:
                lineXXX = lineX.split(":")
                Type =  (lineXXX[1]).rstrip().lstrip()
            elif lineXX.find("content-location:")!=-1:
                lineLLL = lineX.split(":")
                leN = len(lineLLL)
                #Take cate of ":" after http or https
                if leN >= 1:
                    if (lineLLL[1]).lower().rstrip().lstrip()=="http" or \
                    (lineLLL[1]).lower().rstrip().lstrip()=="https" or \
                    (lineLLL[1]).lower().rstrip().lstrip()=="file":
                        print leN
                        if leN >= 3:
                            print "shit"
                            Location = (lineLLL[-1]).rstrip().lstrip()
                            LocationX = Location.split("/")
                            leNN = len(LocationX)
                            if leNN >= 2:
                                if LocationX[leNN-1]!="":
                                    TheNewFileName = LocationX[leNN-1]
                                else:
                                    TheNewFileName = "index"
                
                
    i = 0
    while i < LenXX:
        XX = ""
        YY = ""
        if i + 2 <= LenXX:
            XX = Content[i:i+2]
        if i + 4 <= LenXX:
            YY = Content[i:i+4]

        if XX == "\r\r" or XX == "\n\n" or XX == "\n\r" or YY == "\r\n\r\n":
            break
        i = i + 1
    if i == LenXX:
        print "Can't find payload"
        return 0
    else:
        while Content[i]=="\r" or Content[i]=="\n":
            i = i + 1
        print "Payload found at " + str(i)
        Payload = Content[i:]

        if TheNewFileName == "":
            TheNewFileName = "part" + str(randint(0,65535))+".bin"
        ret = DecodeByContentType(Type,Payload,TheNewFileName)
        return ret

for f in fIn:
    ff = f
    f_x = f.lower().rstrip().lstrip()
    if f_x.find("mime-version:")!=-1:
        mv = ff.split(":")
        if len(mv)>= 2:
            m_x = mv[1].lstrip().rstrip()
            print "MIME-Version: " + m_x
    elif f_x.find("content-type:")!=-1:
        ct = ff.split(":")
        if len(ct) >= 2:
            c_x = ct[1].lstrip().rstrip()
            c_xyz = []
            c_xx = c_x.split(";")
            for cY in c_xx:
                cY_ = cY.rstrip().lstrip()
                c_xyz.append(cY_)
            Found = False
            for c_xxx in c_xyz:
                c_xxxx = c_xxx[0:8]
                if c_xxxx.lower()=="boundary":
                    Found = True
                    lenX = len(c_xxx)
                    i = 0
                    while i < lenX:
                        if c_xxx[i]=="=":
                            break
                        i = i + 1
                    if c_xxx[i]=="=":
                        z = c_xxx[i+1:]
                        z_x = z.lstrip().rstrip()
                        z_xx = re.findall("\".*?\"",z_x)
                        y_xx = re.findall("\'.*?\'",z_x)
                        if len(z_xx) >= 1:
                            boundary = z_xx[0].rstrip("\"").lstrip("\"")
                        if len(y_xx) >= 1:
                            boundary = y_xx[0].rstrip("\"").lstrip("\"")

fIn.close()

if boundary == "":
    print "A boundary was not found\r\n"
    sys.exit(-1)
else:
    print "Boundary: " + "--" + boundary
    boundaryX = "--" + boundary
    fInn = open(inFF,"rb")
    fCon = fInn.read()
    fInn.close()
    fConX = fCon.split(boundaryX)
    lenXX = len(fConX)
    tLast = str(fConX[lenXX-1])
    tLast = tLast.rstrip().lstrip()
    if tLast == "--" or tLast =="":
        lenXX = lenXX - 1
    #the first segment is false, contains metadata
    lenXX = lenXX - 1

    print "Document has " + str(lenXX) + " parts\r\nNow splitting..."
    i = 1
    while i <= lenXX:
        if len(fConX[i]) != 0:
            fyf = fConX[i]
            fyf_x = fyf.lower()
            if fyf_x.find("content-transfer-encoding")!=-1 and fyf_x.find("content-type")!=-1:
                GetFile(fyf)
        i = i + 1

if os.path.exists(inFF)==True:
    os.remove(inFF)
