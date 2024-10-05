# OS libary python handles the os interaction with the python
# It is unix foucs but support for windows. Not entierly but some support is there

# What OS handles ? 

# File and Directory management 

# Process Management

# I generally used these two 
# But chatgpt says it can do this

"""

Summary of Primary Use Cases for the os Library:
File and Directory Operations (create, read, write, delete, navigate)
Process Management (forking processes, running system commands)
Environment Variables (reading and setting environment variables)
Cross-Platform Compatibility (OS-specific operations, paths)
Path Manipulation (working with file paths, extensions, etc.)
File Permissions and Ownership (changing file permissions, checking access)
System Information (user, CPU, memory, etc.)
Low-Level File Operations (working with file descriptors, manual I/O)

"""



import os 
# 1. Write a program that creates a new folder named my_folder, changes into it, 
# and then lists the files in it. If it exists, print "Folder already exists."
# Solution 1.
# flag:bool = False 
# for i in os.listdir():
#     if(i == "app"):
#         flag =True
#         break 
        
# print(os.getcwd())
# if(not flag):
#     print("No app does not exit")
#     os.mkdir('app')
# else:
#     # 
#     print("Folder already exited")



# 2. Create a program that changes into a directory, creates a file, checks if the file exists, and then deletes it. 
# Handle the scenario where the file or directory does not exist.


# Solution 2 

# path = os.getcwd()

# where_you_want_to_go:str = "app"

# for i in os.listdir():
#     if ( i == "fudu_server"):
#         os.chdir(i)
#         if(where_you_want_to_go in os.listdir()):
#             print("App folder exit")

#             try:  
#                 os.remove("main.py")
#             except FileExistsError as e:
#                 print(e)


print("\n\n\n")

# 3. Write a program that forks a child process. The child process should create a symbolic 
# link to an existing file and modify its permissions. The parent process should wait for the
# child to complete, and then verify the changes. 

# ? Solution 3

# pip = os.fork()

# if(pip == 0):
#     source = os.path.join(os.getcwd(), "test.py")
#     print(source)
#     destination: str = os.path.join(os.getcwd(), "learn/random_name.py")
#     print(destination)
#     value = os.symlink(source, destination)
#     os.chmod(destination, 0o644)
#     print("This is the child process")

# else: 

#     os.chdir("learn")
#     print(os.system("ls -l | grep 'random_name.py' "))






print("End of the program!!!\n\n\n")