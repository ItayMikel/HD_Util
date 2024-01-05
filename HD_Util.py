import subprocess
import sys
from time import sleep
import os

print("""
/$$$$$$$                                   /$$                    /$$                           /$$$$$$$$                  /$$
| $$__  $$                                 |__/                   |__/                          |__  $$__/                 | $$
| $$  \ $$ /$$$$$$   /$$$$$$  /$$$$$$/$$$$  /$$  /$$$$$$$ /$$$$$$$ /$$  /$$$$$$  /$$$$$$$          | $$  /$$$$$$   /$$$$$$ | $$
| $$$$$$$//$$__  $$ /$$__  $$| $$_  $$_  $$| $$ /$$_____//$$_____/| $$ /$$__  $$| $$__  $$         | $$ /$$__  $$ /$$__  $$| $$
| $$____/| $$$$$$$$| $$  \__/| $$ \ $$ \ $$| $$|  $$$$$$|  $$$$$$ | $$| $$  \ $$| $$  \ $$         | $$| $$  \ $$| $$  \ $$| $$
| $$     | $$_____/| $$      | $$ | $$ | $$| $$ \____  $$\____  $$| $$| $$  | $$| $$  | $$         | $$| $$  | $$| $$  | $$| $$
| $$     |  $$$$$$$| $$      | $$ | $$ | $$| $$ /$$$$$$$//$$$$$$$/| $$|  $$$$$$/| $$  | $$         | $$|  $$$$$$/|  $$$$$$/| $$
|__/      \_______/|__/      |__/ |__/ |__/|__/|_______/|_______/ |__/ \______/ |__/  |__/         |__/ \______/  \______/ |__/

                      ,--.    ,--.
                     ((O ))--((O ))
                   ,'_`--'____`--'_`.
                  _:  ____________  :_
                 | | ||::::::::::|| | |
                 | | ||::::::::::|| | |
                 | | ||::::::::::|| | |
                 |_| |/__________\| |_|
                   |________________|
                __..-'            `-..__
             .-| : .----------------. : |-.
           ,\ || | |\______________/| | || /.
          /`.\:| | ||  __  __  __  || | |;/,.. 
         :`-._\;.| || '--''--''--' || |,:/_.-':
         |    :  | || .----------. || |  :    |
         |    |  | || '--Imikel--' || |  |    |
         |    |  | ||   _   _   _  || |  |    |
         :,--.;  | ||  (_) (_) (_) || |  :,--.;
         (`-'|)  | ||______________|| |  (|`-')
          `--'   | |/______________\| |   `--'
                 |____________________|
                  `.________________,'
                   (_______)(_______)
                   (_______)(_______)
                   (_______)(_______)
                   (_______)(_______)
                  |        ||        |
                  '--------''--------'
              
""")

print("""Welcome to Permission comparison tool by Itay Mikel!

This program creates files in the process, I need your login username in order to dump files
in the path 'C:/users/<username>/Get_Perm'""")

sleep(1)

# Acquire login username and check if valid
con = 0
while con != 1:
    path = input("Please enter your username: ")
    if not os.path.exists(f"C:/users/{path}"):
        print(f"""
No such profile '{path}' on this computer
""")
    if os.path.exists(f"C:/users/{path}"):
        print("Thank you :* ")
        break

sleep(1)

# Acquire users to compare
a_usr = input("Now for the users to compare, please enter the the first username: ")
b_usr = input("Please enter the second username: ")
print("""
Creating powershell script...""")

# Check if dump folder exist, create it if not
if not os.path.exists(f"C:/users/{path}/Get_Perm"):
    os.makedirs(f"C:/users/{path}/Get_Perm")

# Create PS script
pscript1 = f"""
$a = Get-ADUser {a_usr}  -Properties MemberOf | select -expand MemberOf
$b = $a -replace '^CN=([^,]+).+$','$1'
echo $b | Sort-Object | Out-File -Encoding utf8 "C:/users/{path}/Get_Perm/{a_usr}.csv"

$c = Get-ADUser {b_usr}  -Properties MemberOf | select -expand MemberOf
$d = $c -replace '^CN=([^,]+).+$','$1'
echo $d | Sort-Object | Out-File -Encoding utf8 "C:/users/{path}/Get_Perm/{b_usr}.csv"
"""

print("Exporting...")

# Save PS script to file
pscript2 = open("C:/users/" + path + "/Get_Perm/perm_script.ps1", "w+")
pscript2.write(pscript1)
pscript2.close()
sleep(1)

# Run the script
print("Starting Powershell...")
perm_list = subprocess.run([
    "powershell.exe ", "-NoProfile",
    "C:/users/" + path + "/Get_Perm/perm_script.ps1"
    ])

# Remove the PS script file after execution
os.remove("C:/users/" + path + "/Get_Perm/perm_script.ps1")

# Check first user output file
print("Reading files...")
if os.stat(f"C:/users/{path}/Get_Perm/{a_usr}.csv").st_size == 0:
    print(f"There was a problem getting {a_usr}'s permissions")
    os.remove(f"C:/users/{path}/Get_Perm/{a_usr}.csv")
    os.remove(f"C:/users/{path}/Get_Perm/{b_usr}.csv")
    del a_usr, b_usr
    print("Check if username was supplied correctly, restarting script in 5 seconds...")
    sleep(5)
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Save first user file to dictionary
a_usr_perm1 = set({})
a_usr_perm2 = open(f"C:/users/{path}/Get_Perm/{a_usr}.csv", "r")
for line in a_usr_perm2:
    x = line[:-1]
    a_usr_perm1.add(x)
a_usr_perm2.close()
sorted(a_usr_perm1)

# Check second user file
if os.stat(f"C:/users/{path}/Get_Perm/{b_usr}.csv").st_size == 0:
    print(f"There was a problem getting {b_usr}'s permissions")
    os.remove(f"C:/users/{path}/Get_Perm/{b_usr}.csv")
    del a_usr, b_usr
    print("Check if username was supplied correctly, restarting script in 5 seconds...")
    sleep(5)
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Save second user file to dictionary
b_usr_perm1 = set({})
b_usr_perm2 = open(f"C:/users/{path}/Get_Perm/{b_usr}.csv", "r")
for line in b_usr_perm2:
    x = line[:-1]
    b_usr_perm1.add(x)
b_usr_perm2.close()
sorted(b_usr_perm1)

sleep(1)
print("""
Permissions gathered successfully!
""")

# Compare the permissions and print them
print(f"{a_usr} is a member of these groups that {b_usr} isn't a member of: ")
print(*a_usr_perm1 - b_usr_perm1, sep='\n')
sleep(1)
print(f"""
{b_usr} is a member of these groups that {a_usr} isn't a member of: """)
print(*b_usr_perm1 - a_usr_perm1, sep='\n')
sleep(2)

# Ask user if to clean the user permission files in dump folder
print("\n\nOne more questions but feel free to close the tool, I won't be offended :) ")

while 0 != 1:
    print(f"\ncsv files with specified user's permissions were created in 'C:/users/{path}/Get_perm'")
    question = input(f"Delete the files created? Y/N ").capitalize()
    if question == "Y":
        os.remove(f"C:/users/{path}/Get_perm/{a_usr}.csv")
        os.remove(f"C:/users/{path}/Get_perm/{b_usr}.csv")
        print("Files deleted")
        break
    if question == "N":
        break
    else:
        print("Not a valid option...")

print("Bye")
sleep(2)
