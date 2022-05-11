# v_<FolderName>_<index>.mp4
import os;

path = "./SEAGS7/";
dirList = os.listdir(path);

for dir in dirList:
  if dir.find('_') == 0: continue;
  p = path + dir;
  if not os.path.isdir(p): continue;
  #
  vidFileList = os.listdir(p);
  index = 0;
  for v in vidFileList:
    vidPath = (p + '/' + v);
    newVidPath = (p + '/v_' + dir + '_' + str(index) + '.mp4');
    print(vidPath, ' <=> ', newVidPath);
    os.rename(vidPath, newVidPath);
    index += 1;