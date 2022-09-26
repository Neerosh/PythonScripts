import os,shutil,datetime,sys

def ListFilesEXE(searchPath,listFilesTIDSCI):
    for element in os.scandir(searchPath):
        if element.is_dir():
            if element.path.endswith('BIBLIO'):
                ListFilesDLL(element.path,listFilesTIDSCI)
            else:
                if element.path.endswith('C#'):
                    continue
                else:
                    ListFilesEXE(element.path,listFilesTIDSCI)
        if element.is_file():
            if element.name.endswith('.exe'):
                listFilesTIDSCI.append(element.path)

def ListFilesDLL(searchPath,listFilesTIDSCI):
    for element in os.scandir(searchPath):
        if element.is_dir():
            ListFilesDLL(element.path,listFilesTIDSCI)
        if element.is_file():
            if element.name.endswith('.dll'):
                listFilesTIDSCI.append(element.path)

def CopyFiles(destinationPath,listFiles):
    for filepath in listFiles:
        if (os.path.exists(filepath)):
            fileName = filepath[filepath.rindex('\\')+1:]
            shutil.copyfile(filepath,destinationPath+"\\"+fileName)
            print('Copied File: '+filepath)

def Main():
    listFilesTIDSCI = []
    current_time = datetime.datetime.now()
    searchPath = "D:\\TIDSCI\\APLICS"
    #searchPath = "C:\\Sitema TID\\TIDSCI\\0_Versao"

    print(f"Searching TIDSCI files from {searchPath}")

    ListFilesEXE(searchPath,listFilesTIDSCI)

    destinationPath = sys.executable[:sys.executable.rindex('\\')]
    destinationPath += f"\\FilesTIDSCI_{current_time.day}_{current_time.month}_{current_time.year}"
    #Create Folder
    if (os.path.exists(destinationPath) == False):
        os.mkdir(destinationPath)

    CopyFiles(destinationPath,listFilesTIDSCI)
    print(f"Destination path = {destinationPath}")
    input("Press Enter to Exit")
   
if __name__ == "__main__":
    Main()