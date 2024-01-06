# imports
from colorama import Fore as color #for colorful text
import os
import subprocess
import psutil

# Clear the terminal
# for windows
if os.name == 'nt':
    _ = os.system('cls')
    
# for mac and linux(here, os.name is 'posix')
else:
    _ = os.system('clear')

# welcome message
print(color.BLUE + "Welcome to the WebNowPlaying Discord Rich Presence CLI!")

# define the exit function
def exit():
    print(color.RED + "Exiting...")
    os._exit(0)

# make the pid global so we can use it later
global pid 

# menu
while True:
    print(color.BLUE + "\n\nPlease select an option:")
    print(color.GREEN + "1. Start the rich presence client")
    print(color.YELLOW + "2. Stop the rich presence client")
    print(color.RED + "3. Exit")
    print(color.BLUE + "\n\nPlease enter your choice:")
    choice = input() # get the choice from the user
    # check the choice
    if choice == "1": 
        if os.path.isfile("pid.txt"):
            with open("pid.txt", "r") as file:
                pid = int(file.read())
                file.close()
            if psutil.pid_exists(pid):
                print("Task with PID", pid, "exists.")
                print(color.RED + "RPC is already running!")
                print(color.BLUE + "New RPC will not be started!")
            else:
                print(color.RED + "!! RPC was shutdown unexpectedly !!")
                print(color.BLUE + "Starting the RPC...")
                subprocess.Popen(["pythonw", "script.pyw"], creationflags=subprocess.CREATE_NO_WINDOW)
                print(color.GREEN + "Done!")
        else:
            # Start the process
            print(color.BLUE + "Starting the RPC...")
            subprocess.Popen(["pythonw", "script.pyw"], creationflags=subprocess.CREATE_NO_WINDOW)
            print(color.GREEN + "Done!")

    # exit the rpc client
    elif choice == "2":
        # Check if the process is running
        if 'pid' in globals() or os.path.isfile("pid.txt"):
            if os.path.isfile("pid.txt"):
                with open("pid.txt", "r") as file:
                    pid = file.read()
                    file.close()
            print(color.BLUE + "Stopping the RPC...")
            
            # Kill the process
            os.system("taskkill /PID " + str(pid) + " /F")
            print(color.GREEN + "Done!")
            os.remove("pid.txt")
        
        else:
            print(color.RED + "RPC is not running!")
    
    # exit the program
    elif choice == "3":
        exit()
    
    # invalid choice
    else:
        print(color.RED + "Invalid choice!")
