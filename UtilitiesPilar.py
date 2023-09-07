import sys,os
import pyzipper
import argparse
from enum import Enum

def GetFiles_TaskToDo(originFolder: str) -> list:
    listFiles = []
    for element in os.scandir(originFolder):

        if element.is_file():
            if element.name == "TaskToDo.exe" or (element.name.startswith("TaskToDo") and element.name.endswith(".dll")):
                listFiles.append(element)

    return listFiles

def GetFiles_BrainService(originFolder: str) -> list:
    listFiles = []
    for element in os.scandir(originFolder):

        if element.is_file():
            listFiles.append(element)

        elif element.is_dir():
            listFiles.append(GetFiles_BrainService(element.path))

    return listFiles

def ZipFiles_VersionTaskToDo(listFiles: list, destinationFile: str):    
    zipFile = destinationFile+'.zip'
    folderName = defaultVariables.rootFolder

    with pyzipper.AESZipFile(zipFile,
                            'w',
                            compression=pyzipper.ZIP_LZMA,
                            encryption=pyzipper.WZ_AES) as zf:
        zf.setpassword(defaultVariables.encodedFilePassword())
        for file in listFiles:
            zf.write(file,f"{folderName}\\{file.name}")
        
    if os.path.exists(zipFile):
        print(zipFile +" zip created successfully!")

def ZipFiles_VersionTaskToDoBrainService(listFilesTaskToDo: list, listFilesBrainService: list, destinationFile: str):
    zipFile = destinationFile+'.zip'
    folderName = defaultVariables.rootFolder

    with pyzipper.AESZipFile(zipFile,
                            'w',
                            compression=pyzipper.ZIP_LZMA,
                            encryption=pyzipper.WZ_AES) as zf:
        zf.setpassword(defaultVariables.encodedFilePassword())
        for file in listFilesTaskToDo:
            if file.name in ["TaskToDo.exe","TaskToDo.exe.config","CefSharp.BrowserSubprocess.exe"]:
                zf.write(file,f"{folderName}\\{defaultVariables.taskToDoFolder}\\{file.name}")
            else:
                zf.write(file,f"{folderName}\\{defaultVariables.taskToDoDLLFolder}\\{file.name}")

        for file in listFilesBrainService:
            if file.name in ["TaskToDoBrainService.exe","TaskToDoBrainService.exe.config","CefSharp.BrowserSubprocess.exe"]:
                zf.write(file,f"{folderName}\\{defaultVariables.brainServiceFolder}\\{file.name}")
            else:
                zf.write(file,f"{folderName}\\{defaultVariables.brainServiceDLLFolder}\\{file.name}")

def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument("packVersion", choices=[1,2], type=int,
                        help=f"Version specified can be 1 = Version TaskToDo or 2 = Version TaskToDo-BrainService") 
    parser.add_argument("taskToDoFolder", metavar="C:\\TaskToDo",help="Folder where this program will search for TaskToDo files")
    parser.add_argument("toFolder", metavar="C:\\ExampleTo",help="Folder where this program will generate an .zip file")
    parser.add_argument("rootFolder", metavar="rootFolder", help="Defines root folder .zip, is also used as te default .zip filename")
    parser.add_argument("-brainServiceFolder", metavar="C:\\BrainService",help="Folder where this program will search for BrainService files")
    parser.add_argument("-zip", metavar="example.zip", help="Defines filename of .zip")
    parser.add_argument("-filepass", metavar="example.zip", help="Defines .zip file password, the default password is 123")
    args = parser.parse_args()

    if args.packVersion == PackVersion.VersionTaskToDoBrainService and args.brainServiceFolder is None:
        parser.error("argument -brainServiceFolder is required when operation is equals to VersionTaskToDoBrainService.")

    zipFilename = defaultVariables.rootFolder
    if not args.zip is None:
        zipFilename = args.zip

    if not args.filepass is None:
        defaultVariables.filePassword = args.filepass

    taskToDoFolder = args.taskToDoFolder
    destinationFolder = args.toFolder
    defaultVariables.rootFolder = args.rootFolder
    defaultVariables.packVersion = args.packVersion

    zipFilename +=f"({defaultVariables.filePassword})"
    zipFilename = destinationFolder+"\\"+zipFilename

    listFilesTaskToDo = GetFiles_TaskToDo(taskToDoFolder)
    print(f"\nFiles From: {taskToDoFolder}")
    for element in listFilesTaskToDo:
        print(element.name)

    print(f"\nOperation Type: {PackVersion(defaultVariables.packVersion).name}")

    if defaultVariables.packVersion == PackVersion.VersionTaskToDo.value:
        print(f"Zipping Files: {taskToDoFolder}")
        ZipFiles_VersionTaskToDo(listFilesTaskToDo,zipFilename)

    elif defaultVariables.packVersion == PackVersion.VersionTaskToDoBrainService.value:
        brainServiceFolder = args.brainServiceFolder
        listFilesBrainService = GetFiles_BrainService(brainServiceFolder)

        print(f"\nFiles From: {brainServiceFolder}")
        for element in listFilesBrainService:
            print(element.name)
        print(f"Zipping Files: {taskToDoFolder} and {brainServiceFolder}")
        ZipFiles_VersionTaskToDoBrainService(listFilesTaskToDo,listFilesBrainService,zipFilename)


class PackVersion(Enum):
    VersionTaskToDo = 1
    VersionTaskToDoBrainService = 2

class DefaultVariables ():
    def __init__(self):
        self._packVersion = PackVersion.VersionTaskToDo
        self._taskToDoFolder = "TaskToDo"
        self._taskToDoDLLFolder = "TaskToDo\\dlls"
        self._brainServiceFolder = "BrainService"
        self._brainServiceDLLFolder = "BrainService\\dlls"
        self._filePassword = "123"
        self._rootFolder = None

    @property
    def packVersion(self):
        return self._packVersion
    
    @packVersion.setter
    def packVersion(self, value):
        self._packVersion = value
    
    @property
    def taskToDoFolder(self):
        return self._taskToDoFolder

    @property
    def taskToDoDLLFolder(self):
        return self._taskToDoDLLFolder

    @property
    def brainServiceFolder(self):
        return self._brainServiceFolder

    @property
    def brainServiceDLLFolder(self):
        return self._brainServiceDLLFolder

    @property
    def filePassword(self):
        return self._filePassword

    @filePassword.setter
    def filePassword(self, value):
        self._filePassword = value

    def encodedFilePassword(self):
        return str.encode(self._filePassword)

    @property
    def rootFolder(self):
        return self._rootFolder

    @rootFolder.setter
    def rootFolder(self, value):
        self._rootFolder = value


if __name__ == "__main__":
    defaultVariables = DefaultVariables()
    Main()