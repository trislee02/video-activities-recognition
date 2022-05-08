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
    createDirIfNotExists(classDir);
    # Cut into smaller 5s video
    if autoCut > 0:
      j = 1;
      for f in range(seg['from'], seg['to'], autoCut):
        t = f + autoCut;
        if t > seg['to']: t = seg['to'];
        segVidPath = classDir+"/"+str(seg['class'])+"-"+rootVidName+"_"+str(seg['from'])+"_"+str(seg['to'])+"("+str(j)+")"+".mp4";
        segVid = rootVid.subclip(f, t);
        segVid.write_videofile(filename=segVidPath,audio=False);
        j+=1;
    else:
      segVidPath = classDir+"/"+str(seg['class'])+"-"+rootVidName+"_"+str(seg['from'])+"_"+str(seg['to'])+".mp4";
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
autoCut = input("Muon tu dong cat thanh video nho hon k giay khong? Co thi nhap so k > 0, khong thi nhap 0: ");
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

idxFile.close();
