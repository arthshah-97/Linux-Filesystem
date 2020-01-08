import MemoryInterface, AbsolutePathNameLayer

def Initialize_My_FileSystem():
    MemoryInterface.Initialize_My_FileSystem()
    AbsolutePathNameLayer.AbsolutePathNameLayer().new_entry('/', 1)

#HANDLE TO ABSOLUTE PATH NAME LAYER
interface = AbsolutePathNameLayer.AbsolutePathNameLayer()

class FileSystemOperations():

    #MAKES NEW DIRECTORY
    def mkdir(self, path):
        interface.new_entry(path, 1)

    #CREATE FILE
    def create(self, path):
        interface.new_entry(path, 0)
        

    #WRITE TO FILE
    def write(self, path, data, offset=0):
        interface.write(path, offset, data)
      

    #READ
    def read(self, path, offset=0, size=-1):
        read_buffer = interface.read(path, offset, size)
        #if size != -1: read_buffer = read_buffer[offset:size+offset]
        if read_buffer != -1: print(path + " : " + read_buffer)

    
    #DELETE
    def rm(self, path):
        interface.unlink(path)


    #MOVING FILE
    def mv(self, old_path, new_path):
        interface.mv(old_path, new_path)


    #CHECK STATUS
    def status(self,server_number):
        print(MemoryInterface.status(server_number))



if __name__ == '__main__':
    #DO NOT MODIFY THIS
#    Initialize_My_FileSystem()
#    my_object = FileSystemOperations()
#    my_object.status()
    #YOU MAY WRITE YOUR CODE AFTER HERE

    
    
#    my_object.mkdir("/A")
#    my_object.mkdir("/A/S")
#    my_object.status()
#    my_object.mkdir("/B")
#    my_object.status()
#    my_object.create("/A/1.txt")
#    my_object.create("/A/S/1.txt")
#    my_object.create("/B/mod.txt")
#   my_object.status()
#    my_object.write("/A/1.txt", "POCSDSLSD!", 0)
#    my_object.read("/A/1.txt")
#    my_object.mv("/A/1.txt","/B/mod.txt")
#    my_object.write("/B/mod.txt", "SUCKS", 6)
 #   my_object.write("/A/1.txt","!!!",4)
#    my_object.status()
#    my_object.read("/A/1.txt")
    '''
    my_object.mv("/A/1.txt", "/B")
    my_object.status()
    my_object.rm("A/1.txt")
    my_object.status()
    '''

