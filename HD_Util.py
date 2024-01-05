import subprocess
from time import sleep
import os

print("""
____________________________________________________________________________________________
(`-').->_(`-')                       (`-')      _               _     (`-')                
 (OO )__( (OO ).->              .->   ( OO).->  (_)      <-.    (_)    ( OO).->       .->   
,--. ,'-'\    .'_          ,--.(,--.  /    '._  ,-(`-'),--. )   ,-(`-')/    '._   ,--.'  ,-.
|  | |  |'`'-..__)         |  | |(`-')|'--...__)| ( OO)|  (`-') | ( OO)|'--...__)(`-')'.'  /
|  `-'  ||  |  ' |   (`-') |  | |(OO )`--.  .--'|  |  )|  |OO ) |  |  )`--.  .--'(OO \    / 
|  .-.  ||  |  / :<-.(OO ) |  | | |  \   |  |  (|  |_/(|  '__ |(|  |_/    |  |    |  /   /) 
|  | |  ||  '-'  /,------.)\  '-'(_ .'   |  |   |  |'->|     |' |  |'->   |  |    `-/   /`  
`--' `--'`------' `------'  `-----'      `--'   `--'   `-----'  `--'      `--'      `--'
Welcome to Help Desk Utility tool, by Itay Mikel!
This program creates files in the process, I need your username in order to dump files
in the path 'C:/users/<username>/HD_Util'
No worries I'll clean them up myself each time you open this script and enter your username\n""")

sleep(1)

# Acquire login username, check if valid
con = 0
while con != 1:
    path = input("Please enter your username: ")
    if not os.path.exists(f"C:/users/{path}"):
        print(f"""
No such profile '{path}' on this computer
""")
    if os.path.exists(f"C:/users/{path}"):
        print("Thank you")
        break

# Cehck if dump folder exists, create if not
if not os.path.exists(f"C:/users/{path}/HD_Util"):
    os.makedirs(f"C:/users/{path}/HD_Util")

# Clean previous files in dump folder
try:
    delpath = os.listdir(f"c:/users/{path}/HD_Util/")
    for file in delpath:
        print("deleteing file: " + file)
        os.remove(f"c:/users/{path}/HD_Util/" + file)
except Exception as e:
    print("No files found")

# Computer management function
def comp_mgmt(): 
    while con != 2:
        # Acquire computer name / IP
        computer_name = input("Which computer should I manage? Enter Computer name or IP: ")
        print("Checking connection, please hold...")

        # Check connection save output to file and verify
        ping = subprocess.run([
            "powershell.exe", "-NoProfile", "\n",
            f"Test-NetConnection '{computer_name}' | select PingSucceeded | Export-Csv -Path c:/users/{path}/HD_Util/{computer_name}.csv"
        ])

        ping_test = open(f"c:/users/{path}/HD_Util/{computer_name}.csv").read().upper()
        if 'TRUE' in ping_test:
            print("Connection made, moving on")
            break
        if 'False' in ping_test:
            print(f"Failed to connect to '{computer_name}' try again :( ")
        elif not os.path.exists(f"c:/users/{path}/HD_Util/{computer_name}.csv"):
            print(f"Failed to connect to '{computer_name}' try again :( ")
    
    
    # Restart computer function
    def restart_computer():
        print("Working on it...")
        restart_command = subprocess.run([
            "powershell.exe", "-NoProfile", rf"shutdown /r /f /t 0 /m \\'{computer_name}'"
        ])

        # Ask if to ping computer till it turns on
        pingt = input("""Command sent, 'ping -t <computer name>' to see when it turns back on?
(When canceling the script will close)Y/N """).upper()
        if pingt == "Y":
            print("Use Ctrl + C to cancel")
            pingtt = subprocess.run([
                "powershell.exe", "-NoProfile", f"ping -t '{computer_name}'"
            ])
        elif pingt == "N":
            pass
        else:
            print("I'll take it as a No")


    # Get system info function
    def systeminfo():
        print("Working on it...")
        sysinfo = subprocess.run([
            "powershell.exe", "-NoProfile", f"systeminfo /s '{computer_name}'"
        ])

    # Get MAC address function
    def getmac():
        print("Working on it...")
        mac = subprocess.run([
            "powershell.exe", "-NoProfile", f"getmac /s '{computer_name}'"
        ])

    # RDP connection function
    def rdp():
        print("Working on it...")
        rdpcn = subprocess.run([
            "powershell.exe", "-NoProfile", f"mstsc.exe /v '{computer_name}'"
        ])
    
    """
    I was using remote viwer software from SCCM to connect to a user session.
    I bet you use a different software, you can edit the path and the software name
    To match your software and use this function if you want.
    Don't forget to add it the the computer management menu

    def remote_viewer():
        print("Working on it...")
        if os.path.exists(
                r"C:\Program Files (x86)\Microsoft Configuration Manager\AdminConsole\bin\CmRcViewer.exe"):
            rvcn = subprocess.run([
                fr"C:\Program Files (x86)\Microsoft Configuration Manager\AdminConsole\bin\CmRcViewer.exe",
                f"{computer_name}"
            ])
        else:
            print(
                r"Can't find: C:\Program Files (x86)\Microsoft Configuration Manager\AdminConsole\bin\CmRcViewer.exe")
            print("Is SCCM installed? Have you moved it?")
    """

    # computer management menu
    while con != 2:
        comp_choice = input(f"""
______________________________________________________________________________________________________
 / ___/___   __ _   ___  __ __ / /_ ___  ____  /  |/  /___ _ ___  ___ _ ___ _ ___  __ _  ___  ___  / /_
/ /__ / _ \ /  ' \ / _ \/ // // __// -_)/ __/ / /|_/ // _ `// _ \/ _ `// _ `// -_)/  ' \/ -_)/ _ \/ __/
\___/ \___//_/_/_// .__/\_,_/ \__/ \__//_/   /_/  /_/ \_,_//_//_/\_,_/ \_, / \__//_/_/_/\__//_//_/\__/ 
                 /_/                                                  /___/

        {computer_name}, Options:
        (R) Restart the computer
        (I) Get system information
        (M) Get MAC address
        (P) Connect with RDP (mstsc.exe)
        (V) Connect with other software, (Edit the code to add, line 112) 
        (E) Go back to main menu
        
        Your Choice: """).upper()
        if comp_choice == "R":
            restart_computer()
            sleep(2)
        elif comp_choice == "I":
            systeminfo()
            sleep(2)
        elif comp_choice == "M":
            getmac()
            sleep(2)
        elif comp_choice == "E":
            main_menu()
        elif comp_choice == "P":
            rdp()
            print("mstsc.exe started")
            sleep(2)
        elif comp_choice == "V":
            #remote_viewer()
            #print("Remote Viewer started")
            #sleep(2)
            print("Did you edit the code?")
        else:
            print("Invalid option")

# User management function
def usr_mgmt():

    # Unlock AD user function
    def unlock_user():
        print("\nWorking on it...")
        unlock = subprocess.run([
            "powershell.exe", "-NoProfile", "\n", f"Unlock-ADAccount -Identity {username}"
        ])
        print(f"Command was sent, if no error is displayed above then {username} was released from lock")

    # Reset AD user password function
    def rest_passwd():
        print("\nPlease note that you can't make the user change his password on next logon with this tool\n")
        while con != 2:
            # Get new password and confirm
            newpass = input(f"Enter new password for {username}: ")
            confpass = input("Confirm new password: ")
            if newpass == confpass:
                # Change AD user password using PS
                print("Working on it...")
                resetpass = subprocess.run([
                    "powershell.exe", "-NoProfile", "\n",
                    f"Set-ADAccountPassword -Identity {username} -NewPassword (ConvertTo-SecureString -AsPlainText '{newpass}' -Force)"
                ])
                print("Password change command was sent' if no error is displayed above then it was successful")
                break
            else:
                print("New and confirmation passwords do not match")
    
    # Logoff user from computer function
    def logoff():
        # Get the computer name / IP
        print(f"I need the computer name {username} is logged on")
        while con != 2:
            computer_name = input("Enter Computer name or IP: ")
            # Check connection with PS, save to file and verify
            print("Checking connection, please hold...")
            ping = subprocess.run([
                "powershell.exe", "-NoProfile", "\n",
                f"Test-NetConnection '{computer_name}' | select PingSucceeded | Export-Csv -Path 'c:/users/{path}/HD_Util/{computer_name}.csv'"
            ])

            ping_test = open(f"c:/users/{path}/HD_Util/{computer_name}.csv").read().upper()
            if 'TRUE' in ping_test:
                print("Connection made, moving on")
                break
            if 'FALSE' in ping_test:
                print(f"Failed to connect to '{computer_name}' try again :( ")
            elif not os.path.exists(f"c:/users/{path}/HD_Util/{computer_name}.csv"):
                print(f"Failed to connect to '{computer_name}' try again :( ")

        # Send logoff command
        logoffy = subprocess.run([
            "powershell.exe", "-NoProfile", "\n",
            f"$a = (quser {username} /server:{computer_name} | select -Skip 1)", "\n",
            f"logoff $a[43] /server:'{computer_name}'"
        ])
        print("Logoff command sent")

    # Get AD user groups function
    def permissions():
        print(f"Gathering {username}'s permissions...\n")
        getperm = subprocess.run([
            "powershell.exe", "-NoProfile", f"""
        $a = Get-ADUser {username} -Properties MemberOf | select -expand MemberOf
        $b = $a -replace '^CN=([^,]+).+$','$1'
        echo $b | Sort-Object"""
        ])
        print("\nAll done")

    # Acquire AD username, save to file and check if valid
    username = input("Enter the username to perform the actions on: ")
    print("Validating username, please hold...")
    user_test = subprocess.run([
        "powershell.exe", "-NoProfile", "\n",
        f"Get-ADUser -Identity {username} -Properties lockedout | select Enabled,Lockedout | Export-Csv -Path c:/users/{path}/HD_Util/{username}.csv"
    ])
    usertrue = "True"
    userfalse = "False"
    user_test2 = open(f"c:/users/{path}/HD_Util/{username}.csv", 'r').read()
    if os.stat(f"C:/users/{path}/HD_Util/{username}.csv").st_size == 0:
        print("Can't find user, if you didn't make a typo, the user is probably disabled, try again")
        usr_mgmt()
    # Check if the user is locked and suggest unlock
    elif usertrue * 2 in user_test2:
        while 1 != 2:
            unlad = input("User is locked, unlock now? Y/N").upper()
            if unlad == "Y":
                unlock_user()
                break
            elif unlad == "N":
                break
            else:
                print("I'll take it as a no")
                break
    elif usertrue and userfalse in user_test2:
        print("User identified, moving on")

    # User management menu 
    while con != 2:
        option = input(f"""
_______________________________________________________________________________
 / / / /___ ___  ____  /  |/  /___ _ ___  ___ _ ___ _ ___  __ _  ___  ___  / /_
/ /_/ /(_-</ -_)/ __/ / /|_/ // _ `// _ \/ _ `// _ `// -_)/  ' \/ -_)/ _ \/ __/
\____//___/\__//_/   /_/  /_/ \_,_//_//_/\_,_/ \_, / \__//_/_/_/\__//_//_/\__/ 

        {username}, Options:
        (U) Unlock AD account
        (L) Logoff user from computer
        (S) Change AD account password
        (P) Get user's permissions
        (E) Go back to main menu
        
        Your Choice: """).upper()
        if option == 'U':
            unlock_user()
            sleep(2)
        elif option == 'L':
            logoff()
            sleep(2)
        elif option == 'S':
            rest_passwd()
            sleep(2)
        elif option == 'P':
            permissions()
            sleep(2)
        elif option == 'E':
            main_menu()
        else:
            print("Invalid option")

# Main menu function
def main_menu():
    while con != 2:
        choice = input("""
__________________________________________________        
  /  |/  /___ _ (_)___    /  |/  /___  ___  __ __
 / /|_/ // _ `// // _ \  / /|_/ // -_)/ _ \/ // /
/_/  /_/ \_,_//_//_//_/ /_/  /_/ \__//_//_/\_,_/

        -------
        Options:
        -------
        (C) Computer Management
        (U) User Management
        (E) Exit
        (T) Troubleshoot
        
        Your Choice: """).upper()
        if choice == "C":
            comp_mgmt()
            break
        elif choice == "U":
            usr_mgmt()
            break
        elif choice == "T":
            print(troubleshoot)
            sleep(1.5)
        elif choice == 'E':
            print("Bye")
            sleep(1.5)
            exit()
        else:
            print("Invalid option")


troubleshoot = r"""
Troubleshooting:

These options in User Management require you to have delegation
over resetting passwords and unlocking other AD accounts:

 change AD account password
 unlock AD account

If you can perform this actions in active directory they should work here as well

----------------

These options require you to have the permissions to send commands to remote computers,
and RPC port available on remote computer:

In User Management - Logoff user from computer
In Computer Management - Restart the computer
                         Get Mac address
                         Get System Information

try to send a simple command in powershell or CMD:
systeminfo /s <computer_name>
If this works in CMD or powershell it should work here as well.


Most of the functions in this tool will not work on users with higher permissions then you
or on computers you do not have access or permissions to.
"""

main_menu()
