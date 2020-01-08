'''
THIS MODULE ACTS LIKE FILE NAME LAYER AND PATH NAME LAYER (BOTH) ABOVE INODE LAYER.
IT RECIEVES INPUT AS PATH (WITHOUT INITIAL '/'). THE LAYER IMPLEMENTS LOOKUP TO FIND INODE NUMBER OF THE REQUIRED DIRECTORY.
PARENTS INODE NUMBER IS FIRST EXTRACTED BY LOOKUP AND THEN CHILD INODE NUMBER BY RESPECTED FUNCTION AND BOTH OF THEM ARE UPDATED
'''
import InodeNumberLayer

#HANDLE OF INODE NUMBER LAYER
interface = InodeNumberLayer.InodeNumberLayer()

class FileNameLayer():

    #PLEASE DO NOT MODIFY
    #RETURNS THE CHILD INODE NUMBER FROM THE PARENTS INODE NUMBER
    def CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(self, childname, inode_number_of_parent):
        inode = interface.INODE_NUMBER_TO_INODE(inode_number_of_parent)
        if not inode:
            print("Error FileNameLayer: Lookup Failure!")
            return -1
        if inode.type == 0:
            print("Error FileNameLayer: Invalid Directory!")
            return -1
        if childname in inode.directory: return inode.directory[childname]
        print("Error FileNameLayer: Lookup Failure!")
        return -1

    #PLEASE DO NOT MODIFY
    #RETUNS THE PARENT INODE NUMBER FROM THE PATH GIVEN FOR A FILE/DIRECTORY
    def LOOKUP(self, path, inode_number_cwd):
        name_array = path.split('/') #name_array is a list of strings of the path names split at '/'
        if len(name_array) == 1: return inode_number_cwd
        else:
            child_inode_number = self.CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(name_array[0], inode_number_cwd)
            if child_inode_number == -1: return -1
            return self.LOOKUP("/".join(name_array[1:]), child_inode_number)

    #PLEASE DO NOT MODIFY
    #MAKES NEW ENTRY OF INODE
    def new_entry(self, path, inode_number_cwd, type):
        if path == '/': #SPECIAL CASE OF INITIALIZING FILE SYSTEM
            interface.new_inode_number(type, inode_number_cwd, "root")
            return True
        parent_inode_number = self.LOOKUP(path, inode_number_cwd)
        parent_inode = interface.INODE_NUMBER_TO_INODE(parent_inode_number)
        childname = path.split('/')[-1]
        if not parent_inode: return -1
        if childname in parent_inode.directory:
            print("Error FileNameLayer: File already exists!")
            return -1
        child_inode_number = interface.new_inode_number(type, parent_inode_number, childname)  #make new child
        if child_inode_number != -1:
            parent_inode.directory[childname] = child_inode_number
            interface.update_inode_table(parent_inode, parent_inode_number)


    #IMPLEMENTS READ
    def read(self, path, inode_number_cwd, offset, length):
        '''WRITE YOUR CODE HERE'''
        parent_inode_number = self.LOOKUP(path, inode_number_cwd) #look up the parent inode number
        path_array = path.split('/')
        if len(path_array) == 1:
            childname = path
        else:
            childname = path.split('/')[-1]
        child_inode_number = self.CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(childname, parent_inode_number)
        #data = interface.read(child_inode_number, offset, length,parent_inode_number)
        if child_inode_number != -1: #checking for errors
            return interface.read(child_inode_number, offset, length,parent_inode_number)
        else:
            return -1

    #IMPLEMENTS WRITE
    def write(self, path, inode_number_cwd, offset, data):
        '''WRITE YOUR CODE HERE'''
        parent_inode_number = self.LOOKUP(path,inode_number_cwd) #look up the parent inode number
        path_array = path.split('/')
        if len(path_array) == 1:
            childname = path
        else:
            childname = path.split('/')[-1]  #obtain the name of the file
        child_inode_number = self.CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(childname,parent_inode_number)
        if child_inode_number != -1: #checking for errors
            interface.write(child_inode_number, offset, data, parent_inode_number)
            return True
        else:
            return -1


    #HARDLINK
    def link(self, old_path, new_path, inode_number_cwd):
        '''WRITE YOUR CODE HERE'''
        file_parent_inode_number = self.LOOKUP(old_path, inode_number_cwd)
        hardlink_parent_inode_number = self.LOOKUP(new_path, inode_number_cwd)
        file_name = old_path.split('/')[-1]  #get the file name
        hardlink_name = new_path.split('/')[-1]  #get the hardlink name
        file_inode_number = self.CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(file_name,file_parent_inode_number)
        interface.link(file_inode_number, hardlink_name, hardlink_parent_inode_number)
        return True


    #REMOVES THE FILE/DIRECTORY
    def unlink(self, path, inode_number_cwd):
        if path == "":
            print("Error FileNameLayer: Cannot delete root directory!")
            return -1
        '''WRITE YOUR CODE HERE'''
        parent_inode_number = self.LOOKUP(path,inode_number_cwd)
        child_name = path.split('/')[-1] #getting the child name
        child_inode_number = self.CHILD_INODE_NUMBER_FROM_PARENT_INODE_NUMBER(child_name,parent_inode_number)
        if child_inode_number == -1 or parent_inode_number == -1: #checking for errors
            return -1
        else:
            interface.unlink(child_inode_number,parent_inode_number,child_name)
            return True

    #MOVE
    def mv(self, old_path, new_path, inode_number_cwd):
        '''WRITE YOUR CODE HERE'''
        self.link(old_path,new_path,inode_number_cwd)
        self.unlink(old_path,inode_number_cwd)

