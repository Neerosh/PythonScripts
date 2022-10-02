import os, mutagen, re

def RemoveStartNumbers(oldFile):
    
    folder = oldFile[0:oldFile.rindex('\\')]
    file = oldFile[oldFile.rindex('\\')+1:]
    validation = True
    charIndex = 0
    newName = ''
    while validation:
        if file[charIndex].isnumeric() or file[charIndex] == ' ':
            newName = file[charIndex+1:]
            validation = True
            charIndex += 1
        else:
            validation = False
            
    if charIndex > 0:
        oldFile = folder+'\\'+file
        newFile = folder+'\\'+newName
        os.rename(oldFile,newFile)
        print(f'Renamed File: "{oldFile}" To "{newFile}')
        return newFile
    return oldFile

def RemoveChar(oldFile,char):
    
    folder = oldFile[0:oldFile.rindex('\\')]
    file = oldFile[oldFile.rindex('\\')+1:]
    
    if oldFile.rfind(char) > 0:
        newName = file.replace(char,"")
        if char == '／':
            newName = file.replace(char,"")
            
        oldFile = folder+'\\'+file
        newFile = folder+'\\'+newName
        os.rename(oldFile,newFile)
        print(f'Renamed File: "{oldFile}" To "{newFile}')
        return newFile
    return oldFile

def RenameFile(filePath):
    folder = filePath[0:filePath.rindex('\\')]
    file = filePath[filePath.rindex('\\')+1:]
    extension = filePath[filePath.rindex('.'):]
    try:
        fileProperties = mutagen.File(filePath,easy=True)
        newName = fileProperties["Artist"][0]+' - '+fileProperties["Title"][0]+extension
        
        newName = newName.replace('?','')
        newName = newName.replace('/',' ')
        newName = newName.replace('\t','') # python tab caracter?
        oldFile = folder+'\\'+file
        newFile = folder+'\\'+newName
        if oldFile != newFile:
            print(newName)
            os.rename(oldFile,newFile)
            print(f'Renamed File: "{oldFile}" To "{newFile}')
    except Exception as ex:
        print(f'Error: {ex}, file: "{filePath}"')
        
        
        
        
def ScanFolder(folderPath):
    with os.scandir(folderPath) as entryList:
        for entry in entryList:
            if entry.is_file():
                if entry.path.endswith('.mp3') or entry.path.endswith('.flac'):
                    RenameFile(entry.path)
            if entry.is_dir():
                ScanFolder(entry.path)
                
              
def Main():
    path = r"D:\Music\Games"
    ScanFolder(path)
  
  
if __name__ == "__main__":
    Main()