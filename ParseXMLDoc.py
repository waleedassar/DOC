import os,sys,time,base64,zlib
from xml.dom import minidom

def DecompressActiveMime(Content):
    Magic = Content[0:10]
    decompressed = ""
    if Magic == "ActiveMime":
        NewContent = Content[0x32:]
        ZLibMagic = NewContent[0:2]
        if ZLibMagic == "\x78\x01" or ZLibMagic == "\x78\x9C" or ZLibMagic == "\x78\xDA":
            print "ZLib Compression found"
            decompressed = zlib.decompress(NewContent)
            return decompressed

if len(sys.argv)!=2:
    print "Usage: ParseXMLDoc.py input.xml\r\n"
    sys.exit(-1)


xmlX = minidom.parse(sys.argv[1])

listX = xmlX.getElementsByTagName("w:wordDocument")

NumX = len(listX)
MacroPresent = False
EmbeddedObjectPresent = False
if NumX != 0:
    for X in listX:
        try:
            Mx = (X.attributes["w:macrosPresent"].value).lower()
            if Mx == "yes":
                print "Macro found"
                MacroPresent = True
        except:
            MacroPresent = False
        try:
            Ex = (X.attributes["w:embeddedObjXPresent"].value).lower()
            if Ex == "yes":
                print "Embedded object found"
                EmbeddedObjectPresent = True
        except:
            EmbeddedObjectPresent = False
           #print X.childNodes[0].nodeValue
           #print X.hasChildNodes()
           #print type(listX.item(0).nodeValue)
           #i = i + 1

if MacroPresent == True:
    listY = xmlX.getElementsByTagName("w:binData")
    NumY = len(listY)
    if NumY != 0:
        for Y in listY:
            try:
                if Y.attributes["w:name"].value != "":
                    OutFileName = "New.doc" #default name
                    exName = Y.attributes["w:name"].value
                    if exName != "":
                        fileN,fileX = os.path.splitext(exName)
                        OutFileName = fileN + ".doc"
                    fOut = open(OutFileName,"wb")
                    fCon = Y.childNodes[0].nodeValue
                    if fCon != "":
                        NewfCon = ""
                        lenCon = len(fCon)
                        c = 0
                        while c < lenCon:
                            if fCon[c]!="\x0D" and fCon[c]!="\x0A":
                                NewfCon += fCon[c]
                            c = c + 1
                        if NewfCon != 0:
                            NewfCon = NewfCon.lstrip().rstrip()
                            bDec = base64.b64decode(NewfCon)
                            zDec = DecompressActiveMime(bDec)
                            if zDec != "":
                                fOut.write(zDec)
                    fOut.close()
            except:
                print "Can't extract binary data"
