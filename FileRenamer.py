import os
#removing unwanted characters
pathMusic = "D:\Music"

def RemoveChar(oldFile,char):
    
    folder = oldFile[0:oldFile.rindex('\\')]
    file = oldFile[oldFile.rindex('\\')+1:]
    
    if oldFile.rfind(char) > 0:
        newName = file[0:file.rfind(char)]+'-'+file[file.rfind(char)+1:]
        if char == '／':
            newName = file[0:file.rfind(char)]+file[file.rfind(char)+2:]
            
        oldFile = folder+'\\'+file
        newFile = folder+'\\'+newName
        os.rename(oldFile,newFile)
        print('Renamed file: '+oldFile+' to '+newFile)

def CheckEntries(file):
    if file.is_dir():
        with os.scandir(file.path) as fileList:
            for entry in fileList:
                if entry.is_file():
                    RemoveChar(entry.path,'—')
                    RemoveChar(entry.path,'／')
                else:
                    CheckEntries(entry)
    if file.is_file():
        RemoveChar(entry.path,'—')
        RemoveChar(entry.path,'／')
            
         
        
with os.scandir(pathMusic) as fileList:
    for file in fileList:
        CheckEntries(file)