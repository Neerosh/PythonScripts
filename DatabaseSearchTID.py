import os

def SearchSubdirectory(directory,search):
    endingWith = ['.zip','.7z','.rar','.001']
    for element in os.scandir(directory):
        if element.is_dir():
            SearchSubdirectory(element,search)
        if element.is_file():
            elementLower = element.name.lower()
            if element.name.endswith(tuple(endingWith)):
                if search.lower() in elementLower:
                    print(element.path)
            

def Main():

    pathExists = False
    while pathExists == False:
        searchPath = input("\nFolder path to search: (ex: G:\\)\n")
        if os.path.exists(searchPath):
            pathExists = True
        else:
            print("ERROR: Invalid folder path.")
            pathExists = False

    keepAlive = True
    while keepAlive:
        search = input("\nFile name to search: (ex: Duplas)\n")

        print('\nSearching files in '+searchPath.upper()+"...\n")

        SearchSubdirectory(searchPath,search)
        print('--------------------------End--------------------------')


if __name__ == "__main__":
    Main()
