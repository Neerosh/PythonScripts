import os,shutil,datetime,sys,zipfile

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

            fileStats = os.stat(filepath)
            os.utime(destinationPath+"\\"+fileName,ns = (fileStats.st_atime_ns,fileStats.st_mtime_ns))
            print('Copied File: '+filepath)


def ZipFiles(destinationPath):
    destinationFolder = destinationPath[0:destinationPath.rindex('\\')]
    destinationFolderName = destinationPath[destinationPath.rindex('\\')+1:]
    # write files and folders to a zipfile
    ZipPath = f'{destinationFolder}\\{destinationFolderName}.zip'
    zip_file = zipfile.ZipFile(ZipPath, 'w',zipfile.ZIP_DEFLATED, compresslevel=1)
    with zip_file:
        # write each File
        for file in os.scandir(destinationPath+'\\'):
            if file.is_file():
                #print('create file zip: '+file)
                zip_file.write(file.path,file.name)
               
       
    print(zip_file.filename+' zip created successfully!')

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
    ZipFiles(destinationPath)
    print(f"Destination path = {destinationPath}.zip")
    shutil.rmtree(destinationPath)
    input("Press Enter to Exit")
   
if __name__ == "__main__":
    Main()