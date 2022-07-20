from pickle import TRUE
import psutil,keyboard

def SearchProcessesByName(processName):
    listProcesses = list()
    for process in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in process.name().lower():
                listProcesses.append(process)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return listProcesses
            
def PrintProcesses(listProcesses,subProcesses):
    if len(listProcesses) == 0:
        print("This List is Empty...")
        return
    
    print("\nListing Processes.......................")
        
    for process in listProcesses:
        try:
            print("Process: "+str(process.pid)+" - "+process.name())
            print("-- Started with:")
            for item in process.cmdline():
                print("---- "+item)
            if subProcesses == 1:
                for processChild in process.children():
                    print("Child: "+str(processChild.pid)+" - "+processChild.name())
                    print("-- Child Started with:")
                    for item in processChild.cmdline():
                        print("---- "+item)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    print("----------------------------")

def CheckProcessRunning(processName):
    # Checking if there is any running process that contains the given name processName.
    #Iterate over the all the running process
    for process in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in process.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

# Search and print only processes with the name typed
searchName = ''
print("\nType 'exit' to close this program.")
while True:
    searchName = input('Please Enter Process Name: \n')
    if searchName == 'exit':
        print("Program closed...\n")
        break
    if searchName != '':
        listProcesses = SearchProcessesByName(searchName)
        PrintProcesses(listProcesses,1)


    
    
