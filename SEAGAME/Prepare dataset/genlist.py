# Generate trainlist testlist
import os;
import random;

def genList(list, fileName, type = 'train'):
  file = open(fileName, 'w');
  i = 1;
  for classs in list:
    for vid in classs['data']:
      line = vid + ((' '+str(i)) if type=='train' else '') + '\n';
      file.write(line);
    i+=1;
  file.close();

TRAIN_RATIO = 70;
TEST_RATIO = 100 - TRAIN_RATIO;

listRootPath = './traintestlist/';
dataRootPath = "./SEAGS_V1/";

rootList = [];
trainList = [];
testList = [];

cIdxFile = open(listRootPath + 'classInd.txt');

for line in cIdxFile.readlines():
  line = line.replace('\n', '');
  elements = line.split(' ');
  idx = int(elements[0]);
  classs = elements[1];
  vidFileList = os.listdir(dataRootPath + classs);
  for j in range(len(vidFileList)):
    vidFileList[j] = classs + '/' + vidFileList[j];
  rootList.append({'class': classs, 'data': vidFileList});

for obj in rootList:
  data = obj['data'];
  random.shuffle(data);
  trainSize = round((TRAIN_RATIO/100)*len(data));
  trainData = data[:trainSize];
  testData = data[trainSize:];
  trainList.append({'class': obj['class'], 'data': trainData});
  testList.append({'class': obj['class'], 'data': testData});

cIdxFile.close();
genList(trainList, listRootPath + 'trainlist.txt', 'train');
genList(testList, listRootPath + 'testlist.txt', 'test');