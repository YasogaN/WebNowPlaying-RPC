# imports
from colorama import Fore as color #for colorful text
import os
import subprocess
import psutil
import ctypes

# clear_console the terminal
# for windows

def clear_console():
    if os.name == 'nt':
        _ = os.system('cls')
    
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

clear_console()

# welcome message
ctypes.windll.kernel32.SetConsoleTitleW("WebNowPlayingRPC - CLI")
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
    print(color.WHITE + "---------------------------")
    print(color.CYAN + "4. Create task in task scheduler (Start WebNowPlayingRPC on startup)")
    print(color.WHITE + "---------------------------")
    print(color.MAGENTA + "Note: If you are using the task scheduler, you can close this window.")
    print(color.WHITE + "---------------------------")
    print(color.BLUE + "\n\nPlease enter your choice:" + color.WHITE, end=" ")
    choice = input() # get the choice from the user
    # check the choice
    if choice == "1": 
        if os.path.isfile("src/pid.txt"):
            with open("src/pid.txt", "r") as file:
                pid = int(file.read())
                file.close()
            if psutil.pid_exists(pid):
                print("Task with PID", pid, "exists.")
                clear_console()
                print(color.RED + "RPC is already running!")
                print(color.BLUE + "New RPC will not be started!")
            else:
                print(color.RED + "!! RPC was shutdown unexpectedly !!")
                print(color.BLUE + "Starting the RPC...")
                subprocess.Popen(["pythonw", "src/script.pyw"], creationflags=subprocess.CREATE_NO_WINDOW, shell=False)
                clear_console()
                print(color.GREEN + "Done!")
        else:
            # Start the process
            print(color.BLUE + "Starting the RPC...")
            subprocess.Popen(["pythonw", "src/script.pyw"], creationflags=subprocess.CREATE_NO_WINDOW, shell=False)
            clear_console()
            print(color.GREEN + "Done!")

    # exit the rpc client
    elif choice == "2":
        # Check if the process is running
        if 'pid' in globals() or os.path.isfile("src/pid.txt"):
            if os.path.isfile("src/pid.txt"):
                with open("src/pid.txt", "r") as file:
                    pid = file.read()
                    file.close()
            print(color.BLUE + "Stopping the RPC...")
            
            # Kill the process
            os.system("taskkill /PID " + str(pid) + " /F")
            os.remove("src/pid.txt")
            clear_console()
            print(color.GREEN + "Done!")

        else:
            clear_console()
            print(color.RED + "RPC is not running!")
    
    # exit the program
    elif choice == "3":
        exit()
    
    elif choice == "4":
        # create taskshechduler task
        print(color.BLUE + "Creating task...")
        #ask for admin rights and create task scheduler task
        os.system("powershell -Command \"Start-Process cmd -Verb RunAs -ArgumentList '/c schtasks /create /sc onlogon /tn WebNowPlaying /delay 0000:59 /tr " + os.getcwd() + "\\src\\script.pyw'\"")
        clear_console()
        print (color.GREEN + "Done!")
    
    # invalid choice
    else:
        print(color.RED + "Invalid choice!")
        clear_console()
