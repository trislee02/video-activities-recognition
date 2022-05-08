from moviepy.editor import VideoFileClip;
import os

def getVideoLength(filename):
    clip = VideoFileClip(filename)
    duration       = clip.duration
    fps            = clip.fps
    width, height  = clip.size
    return duration, fps, (width, height);

path = "./dataset/"
dirList = os.listdir(path)
 
for dir in dirList:
  if dir.find('_') == 0: continue;
  p = path + dir;

  if not os.path.isdir(p):
    continue;
  #
  vidFileList = os.listdir(p);
  sumOfDuration = 0;
  videoAmount = len(vidFileList);
  for v in vidFileList:
    vidPath = (p + '/' + v);
    # print(vidPath)
    dura = getVideoLength(vidPath)[0];
    sumOfDuration += dura;
  #
  print(f"Class {dir}: {videoAmount} videos, duration = {sumOfDuration} seconds")