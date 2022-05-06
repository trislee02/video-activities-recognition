from moviepy.editor import *
import os;

def createDirIfNotExists(dir):
  if not os.path.isdir(dir):
    os.mkdir(dir);

def cutSegments(vidPath, segments):
  rootVid = VideoFileClip(vidPath) ;
  rootVidName = vidPath.split(".")[0];
  for seg in segments:
    classDir = "./"+str(seg['class']);
    segVidPath = classDir+"/"+str(seg['class'])+"-"+rootVidName+"_"+str(seg['from'])+"_"+str(seg['to'])+".mp4";
    createDirIfNotExists(classDir);
    segVid = rootVid.subclip(seg['from'], seg['to']);
    segVid.write_videofile(filename=segVidPath,audio=False);

def fTime2Sec(fTimeStr):
  tElements = fTimeStr.split(":");
  n = len(tElements);
  sec = 0;
  for i in range(n):
    sec += int(tElements[n-i-1])*pow(60,i);
  return sec;

idxFilePath = input("Nhap duong dan file index (*.txt): ");
idxFile = open(idxFilePath);

lines = idxFile.readlines();
for l in lines:
  l = l.replace("\r", "").replace("\n", "");
  if (l.find("\n") == 0): continue;
  #
  elements = l.split();
  vidPath = elements[0];
  segAmount = int(elements[1]);
  segments = [];
  for i in range(2, 2+segAmount*3,3):
    seg = {};
    seg['from'] = fTime2Sec(elements[i]);
    seg['to'] = fTime2Sec(elements[i+1]);
    seg['class'] = elements[i+2];
    segments.append(seg);
  # handle with index info
  cutSegments(vidPath, segments);