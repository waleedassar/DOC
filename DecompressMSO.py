import os,sys,time,zlib


if len(sys.argv) != 2:
    print "Usage: DecompressMSO.py input_file_here\r\n"
    sys.exit(-1)


inF = sys.argv[1]

if os.path.exists(inF)==False or os.path.getsize(inF)==0:
    print "File does not exist or empty\r\n"
    sys.exit(-1)


fIn = open(inF,"rb")
fCon = fIn.read()
fIn.close()


Magic = fCon[0:10]
if Magic == "ActiveMime":
    NewfCon = fCon[0x32:]
    ZLibMagic = NewfCon[0:2]
    if ZLibMagic == "\x78\x01" or ZLibMagic == "\x78\x9C" or ZLibMagic == "\x78\xDA":
        print "ZLib Compression found"
        decompressed = zlib.decompress(NewfCon)
        fOut = open("ZlibDecompressed.bin","wb")
        fOut.write(decompressed)
        fOut.close()
