import os,sys,time,base64



def Normalize(Content):
    NewCon = ""
    if Content == "":
        return NewCon
    lenX = len(Content)
    if lenX == 0:
        return NewCon
    i = 0
    while i < lenX:
        if Content[i]!= "\x0D" and Content[i]!= "\x0A":
            NewCon += Content[i]
        i = i + 1
    NewCon = NewCon.lstrip().rstrip()
    return NewCon

AllowedB64Chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def IsValidBase64(StrX):
    BeforeLast = "="
    Last = "="
    if StrX == "":
        return False
    lenX = len(StrX)
    if lenX == 0:
        return False
    i = 0
    while i < lenX:
        if AllowedB64Chars.find(StrX[i])== -1:
            #Only allowed if the filler
            if i != lenX-1 and i != lenX-2:
                return false
            elif i == lenX-2 and StrX[i]!="=":
                BeforeLast = StrX[i]
            elif i == lenX-1 and StrX[i]!="=":
                Last = StrX[i]
        i = i + 1
    if BeforeLast != Last:
       return False
    return True


if len(sys.argv)!=2:
    print "Usage: Base64Decode.py input.txt\r\n"
    sys.exit(-1)

inF = sys.argv[1]

fIn = open(inF,"rb")
fCon = fIn.read()
fIn.close()


fCon_n = Normalize(fCon)
#fOut = open("Normalized.txt","w")
#fOut.write(fCon_n)
#fOut.close()

if IsValidBase64(fCon_n)==False:
    print "Not a valid base64 string\r\n"
    sys.exit(-1)
decX = ""
try:
    decX = base64.b64decode(fCon_n)
except:
    print "Error: seems like it is not valid base64 string\r\n"
    sys.exit(-1)
    

print decX
fOut = open("output.bin","wb")
fOut.write(decX)
fOut.close()
