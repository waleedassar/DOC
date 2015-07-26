import os,sys,time,subprocess,hashlib,zipfile
from xml.dom import minidom

Defaults = {}
Overrides = {}
CTParsed = False
CoreParsed = False
AppParsed = False

XMLFiles = []
BinFiles = []
rIds = []

#returns true on http,https, and file://
def IsUrlOrFile(UrlX):
    if UrlX == 0:
        return False
    lenURLx = len(UrlX)
    if lenURLx <= 7:  #At least http://
        return False
    h = UrlX[0:4]
    hs = UrlX[0:5]
    if h.lower()=="http" or h.lower()=="file":
        nx = UrlX[4:7]
        if nx == "://":
            return True
    elif hs.lower()=="https":
        nxs = UrlX[5:8]
        if nxs == "://":
            return True
    return False


def IsUrl(UrlX):
    if UrlX == 0:
        return False
    lenURLx = len(UrlX)
    if lenURLx <= 7:  #At least http://
        return False
    h = UrlX[0:4]
    hs = UrlX[0:5]
    if h.lower()=="http":
        nx = UrlX[4:7]
        if nx == "://":
            return True
    elif hs.lower()=="https":
        nxs = UrlX[5:8]
        if nxs == "://":
            return True
    return False


def ReplaceSlashWithBackSlash(StrSL):
    if StrSL == "":
        return ""
    return StrSL.replace("/","\\")

def AppendBackSlash(StrX):
    StrX = StrX.replace("/","\\")
    if StrX[-1]!="\\":
        StrX += "\\"
    return StrX
def RemoveDotFromExtension(Fx):
    if Fx == "":
        return ""
    if Fx[0]==".":
        return Fx[1:]
    
def StripParentDirectory(FullPath):
    if FullPath == "":
        return ""
    lenFP = len(FullPath)
    if lenFP == 0:
        return ""
    FullPathX = FullPath
    if FullPathX[0]=="\\":
        FullPathX = FullPathX[1:]
    FullPath_l = FullPathX.split("\\")
    NumX = len(FullPath_l)
    if NumX == 1:
        return FullPath
    NewPath = "\\"
    for iff in range(1,NumX):
        NewPath += FullPath_l[iff]
        if iff != NumX-1:
            NewPath += "\\"
    return NewPath

def ScanForExternalTargets(inFile):
    inXML = minidom.parse(inFile)
    N = 0
    try:
        relX = inXML.getElementsByTagName("Relationship")
        try:
            if len(relX) != 0:
                for rel in relX:
                    TargetX = rel.attributes["Target"].value
                    if TargetX != "" and IsUrlOrFile(TargetX)==True:
                        print "File: " + inFile + " has External Target: " + TargetX
                        N += 1
        except:
            N = N
    except:
        return 0
    return N

def ParseCoreProperties(CoreFile):
    print CoreFile + " ------------------ "
    coreXML = minidom.parse(CoreFile)
    # Extract creator
    Creator = ""
    try:
        CoreProps = coreXML.getElementsByTagName("dc:creator")
        for CoreProp in CoreProps:
            Creator = CoreProp.childNodes[0].data
    except:
        Creator = ""
    print "Creator: " + Creator
    # Extract lastModifiedBy
    LastModifiedBy = ""
    try:
        CoreProps = coreXML.getElementsByTagName("cp:lastModifiedBy")
        for CoreProp in CoreProps:
            LastModifiedBy = CoreProp.childNodes[0].data
    except:
        LastModifiedBy= ""
    print "LastModifiedBy: " + LastModifiedBy
    # Extract Revision
    Revision = ""
    try:
        CoreProps = coreXML.getElementsByTagName("cp:revision")
        for CoreProp in CoreProps:
            Revision = CoreProp.childNodes[0].data
    except:
        Revision= ""
    print "Revision: " + Revision
    # Extract CreationTime
    CreationTime = ""
    try:
        CoreProps = coreXML.getElementsByTagName("dcterms:created")
        for CoreProp in CoreProps:
            CreationTime = CoreProp.childNodes[0].data
    except:
        CreationTime= ""
    print "CreationTime: " + CreationTime
    # Extract ModificationTime
    ModificationTime = ""
    try:
        CoreProps = coreXML.getElementsByTagName("dcterms:modified")
        for CoreProp in CoreProps:
            ModificationTime = CoreProp.childNodes[0].data
    except:
        ModificationTime= ""
    print "ModificationTime: " + ModificationTime
    # Extract Title
    Title = ""
    try:
        CoreProps = coreXML.getElementsByTagName("dc:title")
        for CoreProp in CoreProps:
            Title = CoreProp.childNodes[0].data
    except:
        Title = ""
    print "Title: " + Title
    # Extract Subject
    Subject = ""
    try:
        CoreProps = coreXML.getElementsByTagName("dc:subject")
        for CoreProp in CoreProps:
            Subject = CoreProp.childNodes[0].data
    except:
        Subject= ""
    print "Subject: " + Subject
    # Extract Keywords
    Keywords = ""
    try:
        CoreProps = coreXML.getElementsByTagName("cp:keywords")
        for CoreProp in CoreProps:
            Keywords = CoreProp.childNodes[0].data
    except:
        Keywords= ""
    print "Keywords: " + Keywords
    # Extract Description
    Description = ""
    try:
        CoreProps = coreXML.getElementsByTagName("dc:description")
        for CoreProp in CoreProps:
            Description = CoreProp.childNodes[0].data
    except:
        Description= ""
    print "Description/Comment: " + Description
    # Extract Category
    Category = ""
    try:
        CoreProps = coreXML.getElementsByTagName("cp:category")
        for CoreProp in CoreProps:
            Category = CoreProp.childNodes[0].data
    except:
        Category= ""
    print "Category: " + Category
    # Extract ContentStatus
    ContentStatus = ""
    try:
        CoreProps = coreXML.getElementsByTagName("cp:contentStatus")
        for CoreProp in CoreProps:
            ContentStatus = CoreProp.childNodes[0].data
    except:
        ContentStatus = ""
    print "ContentStatus: " + ContentStatus
    return


def ParseAppExtendedProperties(AppFile):
    print AppFile + " ------------------ "
    appXML = minidom.parse(AppFile)
    # Extract Template
    Template = ""
    try:
        AppProps = appXML.getElementsByTagName("Template")
        for AppProp in AppProps:
            Template = AppProp.childNodes[0].data
    except:
        Template = ""
    print "Template: " + Template
    
    # Extract TotalTime
    TotalTime = ""
    try:
        AppProps = appXML.getElementsByTagName("TotalTime")
        for AppProp in AppProps:
            TotalTime = AppProp.childNodes[0].data
    except:
        TotalTime = ""
    print "TotalTime: " + TotalTime
    
    # Extract Pages
    Pages = ""
    try:
        AppProps = appXML.getElementsByTagName("Pages")
        for AppProp in AppProps:
            Pages = AppProp.childNodes[0].data
    except:
        Pages = ""
    print "Pages: " + Pages
    # Extract Words
    Words = ""
    try:
        AppProps = appXML.getElementsByTagName("Words")
        for AppProp in AppProps:
            Words = AppProp.childNodes[0].data
    except:
        Words = ""
    print "Words: " + Words
    # Extract Characters
    Characters = ""
    try:
        AppProps = appXML.getElementsByTagName("Characters")
        for AppProp in AppProps:
            Characters = AppProp.childNodes[0].data
    except:
        Characters = ""
    print "Characters: " + Characters
    # Extract Application
    Application = ""
    try:
        AppProps = appXML.getElementsByTagName("Application")
        for AppProp in AppProps:
            Application = AppProp.childNodes[0].data
    except:
        Application = ""
    print "Application: " + Application
    # Extract DocSecurity
    DocSecurity = ""
    try:
        AppProps = appXML.getElementsByTagName("DocSecurity")
        for AppProp in AppProps:
            DocSecurity = AppProp.childNodes[0].data
    except:
        DocSecurity = ""
    print "DocSecurity: " + DocSecurity
    # Extract Lines
    Lines = ""
    try:
        AppProps = appXML.getElementsByTagName("Lines")
        for AppProp in AppProps:
            Lines = AppProp.childNodes[0].data
    except:
        Lines = ""
    print "Lines: " + Lines
    # Extract Paragraphs
    Paragraphs = ""
    try:
        AppProps = appXML.getElementsByTagName("Paragraphs")
        for AppProp in AppProps:
            Paragraphs = AppProp.childNodes[0].data
    except:
        Paragraphs = ""
    print "Paragraphs: " + Paragraphs
    # Extract ScaleCrop
    ScaleCrop = ""
    try:
        AppProps = appXML.getElementsByTagName("ScaleCrop")
        for AppProp in AppProps:
            ScaleCrop = AppProp.childNodes[0].data
    except:
        ScaleCrop = ""
    print "ScaleCrop: " + ScaleCrop
    # Extract Company
    Company = ""
    try:
        AppProps = appXML.getElementsByTagName("Company")
        for AppProp in AppProps:
            Company = AppProp.childNodes[0].data
    except:
        Company = ""
    print "Company: " + Company
    # Extract LinksUpToDate
    LinksUpToDate = ""
    try:
        AppProps = appXML.getElementsByTagName("LinksUpToDate")
        for AppProp in AppProps:
            LinksUpToDate = AppProp.childNodes[0].data
    except:
        LinksUpToDate = ""
    print "LinksUpToDate: " + LinksUpToDate
    # Extract CharactersWithSpaces
    CharactersWithSpaces = ""
    try:
        AppProps = appXML.getElementsByTagName("CharactersWithSpaces")
        for AppProp in AppProps:
            CharactersWithSpaces = AppProp.childNodes[0].data
    except:
        CharactersWithSpaces = ""
    print "CharactersWithSpaces: " + CharactersWithSpaces
    # Extract SharedDoc
    SharedDoc = ""
    try:
        AppProps = appXML.getElementsByTagName("SharedDoc")
        for AppProp in AppProps:
            SharedDoc = AppProp.childNodes[0].data
    except:
        SharedDoc = ""
    print "SharedDoc: " + SharedDoc
    # Extract HyperlinksChanged
    HyperlinksChanged = ""
    try:
        AppProps = appXML.getElementsByTagName("HyperlinksChanged")
        for AppProp in AppProps:
            HyperlinksChanged = AppProp.childNodes[0].data
    except:
        HyperlinksChanged = ""
    print "HyperlinksChanged: " + HyperlinksChanged
    # Extract AppVersion
    AppVersion = ""
    try:
        AppProps = appXML.getElementsByTagName("AppVersion")
        for AppProp in AppProps:
            AppVersion = AppProp.childNodes[0].data
    except:
        AppVersion = ""
    print "AppVersion: " + AppVersion
    return

def ParsevbData(vbDataFile):
    print vbDataFile + " ------------------ "
    vbdataXML = minidom.parse(vbDataFile)
    # Check For Existence of wne:vbaSuppData
    vbaSuppData_found = False
    try:
        vbaSuppData = vbdataXML.getElementsByTagName("wne:vbaSuppData")
        if len(vbaSuppData) != 0:
            vbaSuppData_found = True
    except:
        vbaSuppData_found = False
    if vbaSuppData_found == False:
        return
    # Check For Existence of wne:mcds
    mcds_found = False
    try:
        mcds = vbdataXML.getElementsByTagName("wne:mcds")
        if len(mcds) != 0:
            mcds_found = True
    except:
        mcds_found = False
    if mcds_found == False:
        return
    mcdXX = vbdataXML.getElementsByTagName("wne:mcd")
    if len(mcdXX) != 0:
        print len(mcdXX)
        for mCdX in mcdXX:
            Name = ""
            MacroName = ""
            IsEncrypted = False
            cmg = "0"
            try:
                Name = mCdX.attributes["wne:name"].value
                MacroName = mCdX.attributes["wne:macroName"].value
                IsEncrypted = bool(int(mCdX.attributes["wne:bEncrypt"].value))
                cmg = mCdX.attributes["wne:cmg"].value
            except:
                Name = ""
                MacroName = ""
                IsEncrypted = False
                cmg = 0
            print "Name: " + Name
            print "MacroName: " + MacroName
            print "IsEncrypted: " + str(IsEncrypted)
            print "cmg: " + str(cmg)
    
def ParseWebSettings(WebFile):
    print WebFile + " ------------------ "
    webXML = minidom.parse(WebFile)
    # Extract OptimizeForBrowser
    OptimizeForBrowser = False
    try:
        WebProps = webXML.getElementsByTagName("w:optimizeForBrowser")
        for WebProp in WebProps:
            OptimizeForBrowser = WebProp.childNodes[0].data
    except:
        OptimizeForBrowser = False
    print "OptimizeForBrowser: " + str(OptimizeForBrowser)

def ParseSettings(SettingsFile):
    print SettingsFile + " ------------------ "
    settXML = minidom.parse(SettingsFile)
    Lang = ""
    BidiLang = ""

    try:
        ThemeFontLang = settXML.getElementsByTagName("w:themeFontLang")
        if len(ThemeFontLang) != 0:
            for TFLang in ThemeFontLang:
                Lang = TFLang.attributes["w:val"].value
                BidiLang = TFLang.attributes["w:bidi"].value
    except:
        Lang = ""
        BidiLang = ""
    
    print "Lang: " + Lang
    print "Bidi Lang: " + BidiLang
    return

    
def ParseContentTypes(inXMLFile):
    XMLX = minidom.parse(inXMLFile)
    try:
        Defs = XMLX.getElementsByTagName("Default")
        for Def in Defs:
            XXXXX = Def.attributes
            Ext = XXXXX["Extension"].value
            #print Ext
            ConType = XXXXX["ContentType"].value
            #print ConType
            Defaults[Ext]=ConType
    except:
        print "Can't parse Default Tags"
        return -1
    try:
        Overs = XMLX.getElementsByTagName("Override")
        for Over in Overs:
            OOOOO = Over.attributes
            Part = ReplaceSlashWithBackSlash(OOOOO["PartName"].value)
            #print Part
            ConType = OOOOO["ContentType"].value
            #print ConType
            Overrides[Part]=ConType
    except:
        print "Can't parse Override Tags"
        return -1
    return 0


def main(inF):
    tgt = inF
    fIn  = open(inF,"rb")
    fCon = fIn.read()
    fIn.close()
    ZipBased = False
    if fCon[0]=="P" and fCon[1]=="K":
        if fCon[2]== "\x03":
            if fCon[3]== "\x04":
                ZipBased = True
        elif fCon[2]=="\x05":
            if fCon[3]== "\x06":
                ZipBased = True
        elif fCon[2]=="\x07":
            if fCon[3]== "\x08":
                ZipBased = True
    if ZipBased == False:
        print "Error: input file is not zip-based"
        sys.exit(-2)
    filename,fileext = os.path.splitext(tgt)
    try:
        ZipZ = zipfile.ZipFile(tgt)
        ZipZ.extractall(filename)
        ZipZ.close()
        print "Extracted successfully"
    except:
        print "Error: unable to extract " + tgt + " \r\n"

    if os.path.exists(filename)==True and os.path.isdir(filename)==True:
        fn  = os.walk(filename)
        for f in fn:
            Files = f[2]
            Dir = f[0]
            NumFiles = len(Files)
            if NumFiles != 0:
                for FileX in Files:
                    fullFileName = AppendBackSlash(Dir) + FileX
                    if os.path.isfile(fullFileName) == True:
                        #Scan for external targets in all files (Or we can just only scan .rels files, later)
                        #print "################################"
                        ScanForExternalTargets(fullFileName)
                        #print "################################"
                        if FileX.lower()=="[content_types].xml":
                            XMLFiles.append(fullFileName)
                            #print "Now parsing " + fullFileName
                            ret = ParseContentTypes(fullFileName)
                            if ret == -1:
                                print "Error parsing [Content_Type].xml"
                            else:
                                CTParsed = True
                        else:
                            fileNameXXX,fileExtXXX = os.path.splitext(fullFileName)
                            fileExtNoDot_s = RemoveDotFromExtension(fileExtXXX).lower()
                            if fileExtNoDot_s == "xml":
                                XMLFiles.append(fullFileName)
                            elif fileExtNoDot_s == "bin":
                                BinFiles.append(fullFileName)
                            ft =  StripParentDirectory(fullFileName)
                            
                            if CTParsed == True:
                                Con_Type = ""
                                #Check Overrides
                                Found = False
                                for K in Overrides:
                                    if K.lower() == (unicode(ft)).lower():
                                        #print ft
                                        Con_Type = Overrides[K]
                                        #print Con_Type
                                        if Con_Type == "application/vnd.openxmlformats-package.core-properties+xml":
                                            ParseCoreProperties(fullFileName)
                                            CoreParsed = True
                                        elif Con_Type == "application/vnd.openxmlformats-officedocument.extended-properties+xml":
                                            ParseAppExtendedProperties(fullFileName)
                                            AppParsed = True
                                        elif Con_Type == "application/vnd.ms-word.document.macroEnabled.main+xml" or \
                                             Con_Type.lower().find("macroenabled")!=-1 or \
                                             Con_Type == "application/vnd.ms-office.vbaProject" or \
                                             Con_Type.lower().find("vbaproject")!=-1:
                                            print "Document has embedded macro(s)"
                                        elif Con_Type == "application/vnd.ms-word.vbaData+xml":
                                            print "Document has embedded macro(s)"
                                            ParsevbData(fullFileName)
                                        elif Con_Type == "application/vnd.openxmlformats-officedocument.oleObject" or \
                                             Con_Type.lower().find("oleobject") != -1:
                                             print "Document has embedded OLE object(s)"
                                        elif Con_Type == "application/vnd.openxmlformats-officedocument.wordprocessingml.webSettings+xml":
                                            ParseWebSettings(fullFileName)
                                        elif Con_Type == "application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml":
                                            ParseSettings(fullFileName)
                                        print "--------------------------------"
                                        Found = True
                                        break
                                if Found == False:
                                    #Check Default extensions
                                    Found = False
                                    for KK in Defaults:
                                            ftName,ftExt = os.path.splitext(ft)
                                            if ftExt == "" and ftName.lower()=="\\_rels\\.rels":
                                                ftExt = ".rels"
                                            if KK.lower() == unicode((RemoveDotFromExtension(ftExt)).lower()) or ftName.lower()=="\\rels\\.rels":
                                                #print ft
                                                Con_Type = Defaults[KK]
                                                #print Con_Type
                                                if Con_Type == "application/vnd.openxmlformats-package.core-properties+xml":
                                                    ParseCoreProperties(fullFileName)
                                                elif Con_Type == "application/vnd.openxmlformats-officedocument.extended-properties+xml":
                                                    ParseAppExtendedProperties(fullFileName)
                                                elif Con_Type == "application/vnd.ms-word.document.macroEnabled.main+xml" or \
                                                     Con_Type.lower().find("macroenabled")!=-1 or \
                                                     Con_Type == "application/vnd.ms-office.vbaProject" or \
                                                     Con_Type.lower().find("vbaproject")!=-1:
                                                    print "Document has embedded macro(s)"
                                                elif Con_Type == "application/vnd.ms-word.vbaData+xml":
                                                    print "Document has embedded macro(s)"
                                                    ParsevbData(fullFileName)
                                                elif Con_Type == "application/vnd.openxmlformats-officedocument.oleObject" or \
                                                     Con_Type.lower().find("oleobject") != -1:
                                                     print "Document has embedded OLE object(s)"
                                                elif Con_Type == "application/vnd.openxmlformats-officedocument.wordprocessingml.webSettings+xml":
                                                    ParseWebSettings(fullFileName)
                                                elif Con_Type == "application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml":
                                                    ParseSettings(fullFileName)
                                                print "--------------------------------"
                                                Found = True
                                                break
                                    if Found == False:
                                        print ft
                                        print "N/A"
                                        print "--------------------------------"
                                
                                
                
    return





                


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: ParseDOCX.py parent_dir_here\r\n"
        sys.exit(-1)
    else:
        main(sys.argv[1])
