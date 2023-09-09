import argparse, os, pyzipper
from enum import Enum

def GetFiles(originFolder: str) -> list:
    listFiles = []
    for element in os.scandir(originFolder):

        if defaultVariables.packVersion == PackVersion.TaskToDo.value:
            if element.is_file():
                if element.name == "TaskToDo.exe" or (element.name.startswith("TaskToDo") and element.name.endswith(".dll")):
                    listFiles.append(element)

        if defaultVariables.packVersion == PackVersion.TaskToDoBrainService.value:
            if element.is_file():
                listFiles.append(element)
            elif element.is_dir():
                listFiles.append(GetFiles(element.path))

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
        print(f"Generated File: {zipFile}")

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

    if os.path.exists(zipFile):
        print(f"Generated File: {zipFile}")

def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument("packVersion", choices=[1,2], type=int,
                        help=f"Version specified can be 1 = TaskToDo or 2 = TaskToDoBrainService") 
    parser.add_argument("rootFolder", metavar="rootFolder", help="Defines root folder .zip, is also used as the default .zip filename")
    parser.add_argument("toFolder", metavar="C:\\ExampleTo",help="Folder where this program will generate an .zip file")
    parser.add_argument("taskToDo", metavar="C:\\TaskToDo",help="Folder where this program will search for TaskToDo files")
    parser.add_argument("-brainService", metavar="C:\\BrainService",help="Folder where this program will search for BrainService files")
    parser.add_argument("-zip", metavar="example.zip", help="Defines filename of .zip")
    parser.add_argument("-filepass", metavar="123", help="Defines .zip file password, the default password is 123")
    args = parser.parse_args()

    if args.packVersion == PackVersion.TaskToDoBrainService and args.brainService is None:
        parser.error("argument -brainService is required when operation is equals to VersionTaskToDoBrainService.")

    taskToDoFolder = args.taskToDo
    destinationFolder = args.toFolder
    defaultVariables.rootFolder = args.rootFolder
    defaultVariables.packVersion = args.packVersion

    zipFilename = defaultVariables.rootFolder
    if not args.zip is None:
        zipFilename = args.zip

    if not args.filepass is None:
        defaultVariables.filePassword = args.filepass

    zipFilename = destinationFolder+"\\"+zipFilename
    zipFilename +=f"({defaultVariables.filePassword})"

    print(f"\nOperation Type: {PackVersion(defaultVariables.packVersion).name}")

    if defaultVariables.packVersion == PackVersion.TaskToDo.value:
        listFilesTaskToDo = GetFiles(taskToDoFolder)
        print(f"\nFiles From: {taskToDoFolder}")
        for element in listFilesTaskToDo:
            print(element.name)

        print(f"\nZipping Files From: {taskToDoFolder}")
        ZipFiles_VersionTaskToDo(listFilesTaskToDo,zipFilename)

    elif defaultVariables.packVersion == PackVersion.TaskToDoBrainService.value:
        brainServiceFolder = args.brainService

        listFilesTaskToDo = GetFiles(taskToDoFolder)
        print(f"\nFiles From: {taskToDoFolder}")
        for element in listFilesTaskToDo:
            print(element.name)

        listFilesBrainService = GetFiles(brainServiceFolder)
        print(f"\nFiles From: {brainServiceFolder}")
        for element in listFilesBrainService:
            print(element.name)

        print(f"\nZipping Files From: {taskToDoFolder} and {brainServiceFolder}")
        ZipFiles_VersionTaskToDoBrainService(listFilesTaskToDo,listFilesBrainService,zipFilename)

class PackVersion(Enum):
    TaskToDo = 1
    TaskToDoBrainService = 2

class DefaultVariables ():
    def __init__(self):
        self._packVersion = PackVersion.TaskToDo
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