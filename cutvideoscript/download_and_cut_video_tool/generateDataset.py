from moviepy.editor import *
import os;
import json
import urllib.parse as urlparse
from os import listdir
from pytube import YouTube # download video from youtube
from TikTokApi import TikTokApi #download video from Tiktok

def createDirIfNotExists(dir):
  if not os.path.isdir(dir):
    os.mkdir(dir);

cookie = {
"s_v_web_id": "verify_4063f05a313c39c4e3c2963177cfdd53",
"ttwid": "7CAT6DrOCg98cjrZtcT_Aq4t2GeA3zARecg36mI6tl1Xc"
}

api = TikTokApi(cookie=cookie)

def cutSegments(original_url, segments):
    videoJsonFile = "videos.json"
    videosDict = {}
    with open(videoJsonFile, 'r') as openfile:
        # Reading from json file
        videosDict = json.load(openfile)

    vidPath = videosDict[original_url]['file_name']

    createDirIfNotExists('dataset')
    print('Start cutting video: ',vidPath)
    
    rootVid = VideoFileClip('original_videos/' + vidPath) ;
    rootVidName = vidPath.split(".")[0];
    for seg in segments:
        classDir = str(seg['class']);
        createDirIfNotExists('dataset/' + classDir);
        # Cut into smaller 5s video
        j = 1;
        for f in range(seg['from'], seg['to'], 5):
            t = f + 5;
            if t > seg['to']: t = seg['to'];
            segVidPath = './dataset/' + classDir+"/"+str(seg['class'])+"-"+rootVidName+"_"+str(seg['from'])+"_"+str(seg['to'])+"("+str(j)+")"+".mp4";
            segVid = rootVid.subclip(f, t);
            segVid.write_videofile(filename=segVidPath,audio=False);
            j+=1;

    videosDict[original_url]['cut'] = True

    newVideosDict = videosDict.copy()

    videosDict = json.dumps(videosDict, indent = 4)
    # Writing to sample.json
    with open(videoJsonFile, "w") as outfile:
        outfile.write(videosDict)

    print('Video has been cut: ', vidPath)
    print()

    return newVideosDict

def fTime2Sec(fTimeStr):
  tElements = fTimeStr.split(":");
  n = len(tElements);
  sec = 0;
  for i in range(n):
    sec += int(tElements[n-i-1])*pow(60,i);
  return sec;

def download_youtube_video(original_url):
    # original_url = 'http://youtube.com/watch?v=2lAe1cqCOXo'
    videoJsonFile = "videos.json"
    videosDict = {}
    with open(videoJsonFile, 'r') as openfile:
        # Reading from json file
        videosDict = json.load(openfile)

    print('Start downloading video ', original_url)

    createDirIfNotExists('original_videos');

    new_video_file_name = '#'
    new_video_file_path = '#'
    if('tiktok.com' in original_url):
        video = api.get_video_by_url(original_url)
        new_video_file_name = original_url.split('/')[-1] + '.mp4'
        new_video_file_path = 'original_videos/' + new_video_file_name

        out_file = original_url
        with open(new_video_file_path, 'wb') as output:
            output.write(video)

    elif('youtube.com' in original_url):
        yt = YouTube(original_url)
        out_file = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download('original_videos')

        query = urlparse.parse_qs(urlparse.urlparse(original_url).query)
        new_video_file_name = query["v"][0] + '.mp4'
        new_video_file_path = 'original_videos/' + new_video_file_name

        if(os.path.exists(new_video_file_path)):
            os.remove(new_video_file_path)

        os.rename(out_file, new_video_file_path)

    # save data
    if(original_url not in videosDict):
        videosDict[original_url] = {
            "downloaded": True,
            "cut": False,
            "file_name": new_video_file_name
        }
    else:
        videosDict[original_url]['downloaded'] = True
        videosDict[original_url]['file_name'] = new_video_file_name

    newVideosDict = videosDict.copy()
    videosDict = json.dumps(videosDict, indent = 4)
    
    # Writing to sample.json
    with open(videoJsonFile, "w") as outfile:
        outfile.write(videosDict)

    print('Video downloaded: ' + out_file +' ~> ' + new_video_file_path)
    print()
    
    return newVideosDict

def removeVideo(original_url):
    videoJsonFile = "videos.json"
    videosDict = {}
    with open(videoJsonFile, 'r') as openfile:
        # Reading from json file
        videosDict = json.load(openfile)

    if(original_url not in videosDict):
        return videosDict

    file_name = videosDict[original_url]['file_name'].split('.')[0]
    print('Removing ', original_url, ' ~> ', file_name)

    os.remove('original_videos/' + videosDict[original_url]['file_name'])

    datasetFolder = 'dataset'
    onlyfolders = [f for f in listdir(datasetFolder) if not os.path.isfile(os.path.join(datasetFolder, f))]
    # print(onlyfolders)

    for class_folder in onlyfolders:
        files = [f for f in listdir(datasetFolder + "/" + class_folder) if os.path.isfile(os.path.join(datasetFolder + "/" +  class_folder, f))]
        for video_file in files:
            if(file_name in video_file):
                os.remove(datasetFolder + "/" + class_folder + "/" + video_file)

        # print(class_folder,' :')
        # print(files)

    if(original_url in videosDict):
        del videosDict[original_url]

    newVideosDict = videosDict.copy()
    videosDict = json.dumps(videosDict, indent = 4)
    
    # Writing to sample.json
    with open(videoJsonFile, "w") as outfile:
        outfile.write(videosDict)

    print('Video ',original_url, ' removed!')
    print()

    return newVideosDict


# removeVideo('https://www.tiktok.com/@sikatako133twins/video/7061826818545814810')
# removeVideo('https://www.tiktok.com/@shaniyahhday/video/6962788712673463558')
# removeVideo('https://www.youtube.com/watch?v=l6RhM7wKODI')

if __name__ == "__main__":

    # idxFilePath = input("Nhap duong dan file index (*.txt): ");
    idxFilePath = "videolist.txt"

    # read dictionary of videos
    videoJsonFile = "videos.json"
    videosDict = {}
    with open(videoJsonFile, 'r') as openfile:
        # Reading from json file
        videosDict = json.load(openfile)
    
    # read the text file
    idxFile = open(idxFilePath);

    lines = idxFile.readlines();
    for lineId in range(len(lines)):
        l = lines[lineId]
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

        print(str(lineId + 1) + '.', vidPath)
        print()

        # download the video
        if(vidPath not in videosDict or (vidPath in videosDict and videosDict[vidPath]['downloaded'] == False)):
            videosDict = download_youtube_video(vidPath)

        # print(vidPath)
        # print(segments)

        # # cut the video
        if(not videosDict[vidPath]['cut']):
            videosDict = cutSegments(vidPath, segments);
        
    idxFile.close();

    videosDict = json.dumps(videosDict, indent = 4)
    
    # Writing to sample.json
    with open(videoJsonFile, "w") as outfile:
        outfile.write(videosDict)

    print('\n### Finished! Video dictionary written to ' + videoJsonFile)


