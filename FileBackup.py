import os,shutil,datetime,zipfile,sys

def ListDirectory(mainSearchPath,searchPath,listFiles,listDirectories):
    for element in os.scandir(searchPath):
        if element.is_dir():
            listDirectories.append(element.path.replace(mainSearchPath,''))
            ListDirectory(mainSearchPath,element.path,listFiles,listDirectories)
        if element.is_file():
            listFiles.append(element.path)

def CreateDirectories(destinationPath,listDirectories):
    for directory in listDirectories:
        if (os.path.exists(destinationPath+directory) == False):
            os.mkdir(destinationPath+directory)
            print('Directory Created: '+destinationPath+directory)

def CopyFiles(mainSearchPath,destinationPath,listFiles):
    for filepath in listFiles:
        if (os.path.exists(filepath)):
            #fileName = filepath[filepath.rindex('\\')+1:]
            destination = filepath.replace(mainSearchPath,destinationPath)
            
            shutil.copyfile(filepath,destination)
            #print('Copied File From: '+filepath)
            print('Copied File To: '+destination)

def ListBackupDirectory(searchPath,listFiles,listDirectories):
    for element in os.scandir(searchPath):
        if element.is_dir():
            listDirectories.append(element.path)
            ListBackupDirectory(element.path,listFiles,listDirectories)
        if element.is_file():
            listFiles.append(element.path)

def ZipFiles(destinationPath,destinationFolder):
    listFiles = []
    listDirectories = []
    
    ListBackupDirectory(destinationPath,listFiles,listDirectories)
    
    # write files and folders to a zipfile
    ZipPath = destinationPath[0:destinationPath.rindex('\\')]+'.zip'
    zip_file = zipfile.ZipFile(ZipPath, 'w',zipfile.ZIP_DEFLATED, compresslevel=9)
    with zip_file:
        # write each Directory
        for directory in listDirectories:
            #print('create directory zip: '+directory)
            zip_file.write(directory, directory[len(destinationPath):])
        # write each File
        for file in listFiles:
            #print('create file zip: '+file)
            zip_file.write(file, file[len(destinationPath):])
        
    if zip_file.filename != None:
        print(zip_file.filename+' zip created successfully!')
 
def CreateBackup(searchPath,destinationPath,folder):
    listFiles = []
    listDirectories = []
    
    #Write Reference File
    with open(destinationPath+'BackupReference.txt', 'a') as file:
        file.write(f"{folder} | Original Path: {searchPath}\n")
    
    #Create Module Folder
    destinationPath = f"{destinationPath}{folder}"
    if (os.path.exists(destinationPath) == False):
        os.mkdir(destinationPath)
    
    mainPath = ''
    #folder before selected folder
    if searchPath.rindex('\\') > 0:
        mainPath = searchPath[0:searchPath.rindex('\\')]
        listDirectories.append(searchPath.replace(mainPath,''))
    else:
        mainPath = searchPath
        
    ListDirectory(mainPath,searchPath,listFiles,listDirectories)
    CreateDirectories(destinationPath,listDirectories)
    CopyFiles(mainPath,destinationPath,listFiles)

def Main():
    searchPath = ''
    destinationPath = ''
    current_time = datetime.datetime.now()
    destinationFolder = f"Backup_{current_time.day}_{current_time.month}_{current_time.year}"
    
    #Create Backup Folder
    destinationPath = sys.executable[:sys.executable.rindex('\\')]
    destinationPath += f"\\{destinationFolder}\\"
    if (os.path.exists(destinationPath) == False):
        os.mkdir(destinationPath)
    
    #Kamidori Alchemy Meister Save
    searchPath ='C:\\Users\\Nerrosh\\AppData\\Local\\Eushully'
    folder = 'Kamidori Alchemy Meister Save'
    CreateBackup(searchPath,destinationPath,folder)
    
    #Guitar Hero WTDE Save
    searchPath = 'C:\\Users\\Nerrosh\\Documents\\Aspyr'
    folder = 'GH WTDE Save'
    CreateBackup(searchPath,destinationPath,folder)
    
    #Guitar Hero WTDE Config
    searchPath = 'C:\\Users\\Nerrosh\\AppData\\Local\\Aspyr'
    folder = 'GH WTDE Config'
    CreateBackup(searchPath,destinationPath,folder)
    
    #Tekno Parrot Save 
    searchPath = 'C:\\Users\\Nerrosh\\AppData\\Roaming\\TeknoParrot'
    folder = 'Tekno Parrot Save'
    CreateBackup(searchPath,destinationPath,folder)
    
    #HOLOCURE Save
    searchPath = 'C:\\Users\\Nerrosh\\AppData\\Local\\HoloCure'
    folder = 'Holocure Save'
    CreateBackup(searchPath,destinationPath,folder)
    
    #Create Zip
    ZipFiles(destinationPath,destinationFolder)
    #input("Press Enter to Exit")
   
if __name__ == "__main__":
    Main()