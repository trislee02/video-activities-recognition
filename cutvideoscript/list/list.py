from moviepy.editor import VideoFileClip;
import os
import json

vidTypeMap = {
  '0-2': 0,
  '2-5': 1,
  '5-10': 2,
  '>10': 3
}

collection = {};
minLen = 999;
maxLen = -1;
meanLen = 0;

def getVideoLength(filename):
    clip = VideoFileClip(filename)
    duration       = clip.duration
    fps            = clip.fps
    width, height  = clip.size
    clip.close();
    return duration, fps, (width, height);

def getVidTypeIdx(dura):
  if dura < 2: return vidTypeMap['0-2'];
  if dura < 5: return vidTypeMap['2-5'];
  if dura < 10: return vidTypeMap['5-10'];
  return vidTypeMap['>10'];

path = "./"
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
  vidTypeCount = [0,0,0,0];
  for v in vidFileList:
    vidPath = (p + '/' + v);
    dura = getVideoLength(vidPath)[0];
    sumOfDuration += dura;
    vidTypeCount[getVidTypeIdx(dura)] += 1;
    if dura > maxLen: maxLen = dura;
    if dura < minLen: minLen = dura;
  avgDura = sumOfDuration/videoAmount;
  #
  print(f"Class {dir}: {videoAmount} videos, duration = {sumOfDuration} seconds, video type count:", vidTypeCount);
  collection[dir] = {'videos': videoAmount, 'sum_dura': sumOfDuration, 'avg_dura': avgDura, 'type_count': vidTypeCount};

print(collection);

totalVideos = 0;
totalDurations = 0;
for k in collection:
  obj = collection[k];
  totalVideos += obj['videos'];
  totalDurations += obj['sum_dura'];
meanLen = totalDurations/totalVideos;

print('minLen:', minLen);
print('maxLen:', maxLen);
print('meanLen:', meanLen);
print('totalVideos:', totalVideos);
print('totalDurations:', totalDurations);

outputJson = {
  'collection': collection,
  'minLen:': minLen,
  'maxLen:': maxLen,
  'meanLen:': meanLen,
  'totalVideos:': totalVideos,
  'totalDurations:': totalDurations
}
f = open('output.json', 'w');
json.dump(outputJson, f);
f.close();