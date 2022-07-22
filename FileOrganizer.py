
import os,shutil
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

pathDownloads = r"D:\Downloads"
pathVideo = r"D:\Downloads\Videos"
pathMusic = r"D:\Downloads\Musics"
pathImage = r"D:\Downloads\Images"
pathDestination = ""

def CreateUniqueFileName(pathFolder,fileName,copy):
    fileExists = os.path.exists(pathFolder+"\\"+fileName)
    if fileExists == 0:
        return fileName
    
    uniqueFileName = ""
    copy += 1    
    
    if copy > 1:
        sliceBeforeName = fileName[0:fileName.rfind(str(copy-1))]
        sliceAfterName = fileName[fileName.rfind('.'):]
        uniqueFileName = f"{sliceBeforeName}{str(copy)}{sliceAfterName}"
        return CreateUniqueFileName(pathFolder,uniqueFileName,copy)
    
    sliceBeforeName = fileName[0:fileName.rfind('.')]
    sliceAfterName = fileName[fileName.rfind('.'):]
    uniqueFileName = f"{sliceBeforeName} - ({str(copy)}){sliceAfterName}"
    return CreateUniqueFileName(pathFolder,uniqueFileName,copy)
    
def CopyFile(fromPath,toPath,fileName):
    fileExists = os.path.exists(f"{fromPath}\\{fileName}")
    destinationExists = os.path.exists(toPath)
    
    if destinationExists == 0:
        os.mkdir(toPath)
    
    if fileExists:
        fileNameDestination = CreateUniqueFileName(toPath,fileName,0)
        fullpathFrom = f"{fromPath}\\{fileName}"
        fullpathTo = f"{toPath}\\{fileNameDestination}"
        shutil.move(fullpathFrom,fullpathTo)
        logging.info(f'Move file "{fullpathFrom}" to "{fullpathTo}"')
  
class MoveHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with os.scandir(pathDownloads) as directories:
            for file in directories:
                if file.is_file():
                    #print(file.name)     
                    name = file.name
                    pathDestination =''
                    if name.endswith('.mp4') or name.endswith('.mkv'):
                        pathDestination = pathVideo
                    if name.endswith('.mp3') or name.endswith('.flac'):
                        pathDestination = pathMusic
                    if name.endswith('.png') or name.endswith('.jpg') or name.endswith('.jpeg'):
                        pathDestination = pathImage
                    
                    if pathDestination != '':
                        CopyFile(pathDownloads,pathDestination,name)
  
def Main():
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
    # Join threads to avoid termination from exceptions like KeyboardException
    observer.join()
    
  
if __name__ == "__main__":
    Main()