import os,shutil,datetime

def SearchSubdirectory(mainSearchPath,searchPath,listFiles,listDirectories):
    for element in os.scandir(searchPath):
        if element.is_dir():
            listDirectories.append(element.path.replace(mainSearchPath,''))
            SearchSubdirectory(mainSearchPath,element.path,listFiles,listDirectories)
        if element.is_file():
            listFiles.append(element.path)

def CreateDirectories(destinationPath,listDirectories):
    for directory in listDirectories:
        if (os.path.exists(destinationPath+directory) == False):
            os.mkdir(destinationPath+directory)
            print('Directory Created: '+destinationPath+directory)

def CopyFiles(searchPath,destinationPath,listFiles):
    for filepath in listFiles:
        if (os.path.exists(filepath)):
            #fileName = filepath[filepath.rindex('\\')+1:]
            destination = filepath.replace(searchPath,destinationPath)
            
            shutil.copyfile(filepath,destination)
            #print('Copied File From: '+filepath)
            print('Copied File To: '+destination)

def CreateBackup(searchPath,destinationPath,folder):
    listFiles = []
    listDirectories = []
    current_time = datetime.datetime.now()
    #Create Backup Folder
    destinationPath = f"{destinationPath}Backup_{current_time.day}_{current_time.month}_{current_time.year}\\"
    if (os.path.exists(destinationPath) == False):
        os.mkdir(destinationPath)
    #Create Module Folder
    destinationPath = f"{destinationPath}{folder}"
    if (os.path.exists(destinationPath) == False):
        os.mkdir(destinationPath)
    
    SearchSubdirectory(searchPath,searchPath,listFiles,listDirectories)
    CreateDirectories(destinationPath,listDirectories)
    
    #Write Reference File
    with open(destinationPath+'BackupReference.txt', 'a') as file:
        file.write(f"{folder} Original Path: {searchPath}\n")
        
    CopyFiles(searchPath,destinationPath,listFiles)

def Main():
    searchPath = ''
    destinationPath = ''
    
    #Guitar Hero WTDE Save
    searchPath = 'C:\\Users\\Nerrosh\\Documents\\Aspyr\\'
    folder = 'GH WTDE Save\\'
    destinationPath = 'D:\\'
    CreateBackup(searchPath,destinationPath,folder)
    
    #Guitar Hero WTDE Config
    searchPath = 'C:\\Users\\Nerrosh\\AppData\\Local\\Aspyr'
    folder = 'GH WTDE Config\\'
    destinationPath = 'D:\\'
    CreateBackup(searchPath,destinationPath,folder)
    
    #Tekno Parrot Save 
    searchPath = 'C:\\Users\\Nerrosh\\AppData\\Roaming\\TeknoParrot'
    folder = 'Tekno Parrot Save\\'
    destinationPath = 'D:\\'
    CreateBackup(searchPath,destinationPath,folder)

    input("Press Enter to Exit")
   
if __name__ == "__main__":
    Main()