import os, mutagen

def RenameFile(filePath):
    folder = filePath[0:filePath.rindex('\\')]
    file = filePath[filePath.rindex('\\')+1:]
    extension = filePath[filePath.rindex('.'):]
    try:
        fileProperties = mutagen.File(filePath,easy=True)
        newName = fileProperties["Artist"][0]+' - '+fileProperties["Title"][0]+extension
        newName = newName.replace('"','')
        newName = newName.replace("'",' ')        
        newName = newName.replace('?','')
        newName = newName.replace(':','')
        newName = newName.replace('*',' ')
        newName = newName.replace('/',' ')
        newName = newName.replace('\t','') # python tab character?
        oldFile = folder+'\\'+file
        newFile = folder+'\\'+newName
        if oldFile != newFile:
            os.rename(oldFile,newFile)
            print(f'Renamed File: "{oldFile}" To "{newFile}')

        if 'comment' in fileProperties.keys():
            fileProperties['comment'] = ''
            fileProperties.save()
    except Exception as ex:
        print(f'Error: {ex}, file: "{filePath}"')
        
def ScanFolder(folderPath):
    with os.scandir(folderPath) as entryList:
        for entry in entryList:
            if entry.is_file():
                if entry.path.lower().__contains__("(off vocal version)") or entry.path.lower().__contains__("(instrumental)") or entry.path.lower().__contains__("[instrumental]"):
                    os.remove(entry.path)
                else: 
                    if entry.path.endswith('.mp3') or entry.path.endswith('.flac'):
                        RenameFile(entry.path)
                    else:
                        os.remove(entry.path)
            if entry.is_dir():
                ScanFolder(entry.path)
                     
                     
def Main():
    path = r"D:\Music\Anime"
    ScanFolder(path)
    path = r"D:\Music\Games"
    ScanFolder(path)
  
  
if __name__ == "__main__":
    Main()