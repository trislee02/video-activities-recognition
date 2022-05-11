import os;

writeRootPath = './traintestlist/';
readRootPath = "./SEAGS7/";

dirList = os.listdir(readRootPath);

cIdxFile = open(writeRootPath + 'classInd.txt', 'w');

i = 1;
for dir in dirList:
  if dir.find('_') == 0: continue;
  p = readRootPath + dir;
  if not os.path.isdir(p): continue;
  #
  line = str(i) + ' ' + dir;
  cIdxFile.write(line + '\n');
  print(line);
  i += 1;

cIdxFile.close();