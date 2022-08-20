
import os,shutil,datetime

def SearchSubdirectory(directory,listFiles):
    for element in os.scandir(directory):
        if element.is_dir():
            SearchSubdirectory(element,listFiles)
        if element.is_file():
            elementLower = element.name.lower()
            if elementLower.endswith('.app'):
                listFiles.append(element.path)
                listFiles.append(element.path.replace('.app','.exe'))
           
def CopyFiles(listFiles,destinationPath):
    for filepath in listFiles:
        if (os.path.exists(filepath)):
            fileName = filepath[filepath.rindex('\\')+1:]
            shutil.copyfile(filepath,destinationPath+"\\"+fileName)
            print('Copied File: '+filepath)

def Main():
    searchPath = ''
    destinationPath = ''
    listFiles = []
    current_time = datetime.datetime.now()

    pathExists = False
    while pathExists == False:
        searchPath = input("\nFolder path to search '.app' files: (ex: G:\\)\n")
        if os.path.exists(searchPath):
            pathExists = True
        else:
            print("ERROR: Invalid folder path.")
            pathExists = False

    
    pathExists = False
    while pathExists == False:
        destinationPath = input("\nFolder where the backup folder will be created: (ex: G:\\)\n")
        if os.path.exists(destinationPath):
            pathExists = True
        else:
            print("ERROR: Invalid folder path.")
            pathExists = False

    destinationPath = f"{destinationPath}\\Backup_{current_time.day}_{current_time.month}_{current_time.year}"
    
    SearchSubdirectory(searchPath,listFiles)
    CopyFiles(listFiles)
    input("Press Enter to Exit")
   
if __name__ == "__main__":
    Main()