import os
#removing unwanted characters
pathMusic = r"D:\Downloads\Music"

def RemoveChar(oldFile,char):
    
    folder = oldFile[0:oldFile.rindex('\\')]
    file = oldFile[oldFile.rindex('\\')+1:]
    
    if oldFile.rfind(char) > 0:
        newName = file.replace(char," - ")
        if char == '／':
            newName = file.replace(char,"")
            
        oldFile = folder+'\\'+file
        newFile = folder+'\\'+newName
        os.rename(oldFile,newFile)
        print(f'Renamed File: "{oldFile}" To "{newFile}')
        return newFile
    return oldFile

def CheckEntries(file):
    filePath = file.path
    if file.is_file():
        filePath = RemoveChar(filePath,'—')
        filePath = RemoveChar(filePath,'／')
    if file.is_dir():
        with os.scandir(filePath) as fileList:
            for entry in fileList:
                if entry.is_file():
                    filePath = RemoveChar(entry.path,'—')
                    filePath = RemoveChar(entry.path,'／')
                else:
                    CheckEntries(entry)
            
        
with os.scandir(pathMusic) as fileList:
    for file in fileList:
        CheckEntries(file)