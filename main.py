
import os,time,shutil
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

pathDownloads = "D:\Downloads"
pathVideo = "D:\Downloads\Videos"
pathMusic = "D:\Downloads\Musics"
pathImage = "D:\Downloads\Images"
pathDestination = " "


def CreateUniqueFileName(pathFolder,fileName,copy):
    fileExists = os.path.exists(pathFolder+"\\"+fileName)
    copy += 1    
    if fileExists == 0:
        return fileName
    
    if copy > 1:
        uniqueFileName = fileName[0:fileName.rfind(str(copy-1))]+str(copy)+fileName[fileName.rfind('.'):]
    else:
        uniqueFileName = fileName[0:fileName.rfind('.')]+' - ('+str(copy)+')'+fileName[fileName.rfind('.'):]
    return CreateUniqueFileName(pathFolder,uniqueFileName,copy)
    
def CopyFile(fromPath,toPath,fileName):
    fileExists = os.path.exists(fromPath+"\\"+fileName)
    destinationExists = os.path.exists(toPath)
    
    if destinationExists == 0:
        os.mkdir(toPath)
    
    if fileExists:
        fileNameDestination = CreateUniqueFileName(toPath,fileName,0)
        shutil.move(fromPath+"\\"+fileName, toPath+"\\"+fileNameDestination)
  
class MoveHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with os.scandir(pathDownloads) as directories:
            for file in directories:
                if file.is_file():
                    print(file.name)     
                    name = file.name
                    if name.endswith('.mp4') or name.endswith('.mkv'):
                        pathDestination = pathVideo
                    if name.endswith('.mp3') or name.endswith('.flac'):
                        pathDestination = pathMusic
                    if name.endswith('.png') or name.endswith('.jpg') or name.endswith('.jpeg'):
                        pathDestination = pathImage
                    
                    if pathDestination != '':
                        CopyFile(pathDownloads,pathDestination,name)
  
if __name__ == "__main__":
    # Set the format for logging info
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    path = pathDownloads
    # Initialize logging event handler
    event_handler = MoveHandler()
    # Initialize Observer
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    # Start the observer
    observer.start()
    try:
        while True:
            # Set the thread sleep time
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()