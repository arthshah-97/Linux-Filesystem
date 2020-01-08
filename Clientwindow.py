import FileSystem
import time	

FileSystem.Initialize_My_FileSystem()
fs=FileSystem.FileSystemOperations()
fsexit = 0
print("RAID5")
while fsexit == 0 :
    command = raw_input("$ ")
    command = command.split()
    try:
        if command[0] == "mkdir":
            fs.mkdir(command[1])
        elif command[0] == "create":
            fs.create(command[1])
        elif command[0] == "write":
            path = command[1]
            data = command[2: len(command)-1]
            data = ' '.join(str(item) for item in data)
            offset = command[len(command)-1]
            start = time.clock()
            fs.write(str(path),str(data),int(offset))
            end = time.clock()
            #print("Time taken to perform write:", end - start) 
        elif command[0] == "read":
            path = command[1]
            offset = command[2]
            size = command[3]
            start = time.clock()
            fs.read(path,int(offset), int(size))
            end = time.clock()
            #print("Time taken to perform read:", end - start) 
        elif command[0] == "rm":
            path = command[1]
            fs.rm(path)
        elif command[0] == "mv":
            fs.mv(command[1],command[2])
        elif command[0] == "status":
            fs.status(int(command[1]))
        elif command[0] == "exit":
            fsexit = 1
        elif command[0] == "help":
            print "Create a new directory using mkdir command"
            print "Usage: mkdir <path>"
            print "Create a new file using create command"
            print "Usage: create <path>"
            print "Write to a file using write command"
            print "Usage: write <path> <data> <offset>"
            print "Read a file using read command"
            print "Usage: read <path> <offset> <size>"
            print "Remove a file/a directory using rm command"
            print "Usage: rm <path>"
            print "Move a file using mv command "
            print "Usage: mv <old path> <new path>"
            print "Check the status of server using status command"
            print "Usage: status <server number>"
            print "Type exit to quit"
        else:
            print("Incorrect command. Type help to see the list of all supported commands.")

    except Exception as err:
         print "Error: ", err
         # if command[0] == "mkdir":
         #     print "Re-enter the command"
         #     print "Usage: mkdir <path>"
         # elif command[0] == "create":
         #     print "Re-enter the command"
         #     print "Usage: create <path>"
         # elif command[0] == "write":
         #     print "Re-enter the command"
         #     print "Usage: write <data> <path> <offset>"
         # elif command[0] == "read":
         #     print "Re-enter the command"
         #     print "Usage: read <path> <offset> <size>"
         # elif command[0] == "rm":
         #     print "Re-enter the command"
         #     print "Usage: rm <path>"
         # elif command[0] == "mv":
         #     print "Re-enter the command"
         #     print "Usage: mv <old path> <new path>"
         # elif command[0] == "status":
         #     print "Re-enter the command"
         #     print "Usage: status <server number>"
         # else:
         #     print "Type help to see the list of all supported commands. Type exit to quit"
    
        

