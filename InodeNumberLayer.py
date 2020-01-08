'''
THIS MODULE ACTS AS A INODE NUMBER LAYER. NOT ONLY IT SHARES DATA WITH INODE LAYER, BUT ALSO IT CONNECTS WITH MEMORY INTERFACE FOR INODE TABLE 
UPDATES. THE INODE TABLE AND INODE NUMBER IS UPDATED IN THE FILE SYSTEM USING THIS LAYER
'''
import InodeLayer, config, MemoryInterface, datetime, InodeOps, MemoryInterface


#HANDLE OF INODE LAYER
interface = InodeLayer.InodeLayer()

class InodeNumberLayer():

    #PLEASE DO NOT MODIFY
    #ASKS FOR INODE FROM INODE NUMBER FROM MemoryInterface.(BLOCK LAYER HAS NOTHING TO DO WITH INODES SO SEPERTAE HANDLE)
    def INODE_NUMBER_TO_INODE(self, inode_number):
        array_inode = MemoryInterface.inode_number_to_inode(inode_number)
        inode = InodeOps.InodeOperations().convert_array_to_table(array_inode)
        if inode: inode.time_accessed = datetime.datetime.now()   #TIME OF ACCESS
        return inode


    #PLEASE DO NOT MODIFY
    #RETURNS DATA BLOCK FROM INODE NUMBER
    def INODE_NUMBER_TO_BLOCK(self, inode_number, offset, length):
        inode = self.INODE_NUMBER_TO_INODE(inode_number)
        if not inode:
            print("Error InodeNumberLayer: Wrong Inode Number! \n")
            return -1
        return interface.read(inode, offset, length)


    #PLEASE DO NOT MODIFY
    #UPDATES THE INODE TO THE INODE TABLE
    def update_inode_table(self, table_inode, inode_number):
        if table_inode: table_inode.time_modified = datetime.datetime.now()  #TIME OF MODIFICATION
        array_inode = InodeOps.InodeOperations().convert_table_to_array(table_inode)
        MemoryInterface.update_inode_table(array_inode, inode_number)


    #PLEASE DO NOT MODIFY
    #FINDS NEW INODE INODE NUMBER FROM FILESYSTEM
    def new_inode_number(self, type, parent_inode_number, name):
        if parent_inode_number != -1:
            parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)
            if not parent_inode:
                print("Error InodeNumberLayer: Incorrect Parent Inode")
                return -1
            entry_size = config.MAX_FILE_NAME_SIZE + len(str(config.MAX_NUM_INODES))
            max_entries = (config.INODE_SIZE - 79 ) / entry_size
            if len(parent_inode.directory) == max_entries:
                print("Error InodeNumberLayer: Maximum inodes allowed per directory reached!")
                return -1
        for i in range(0, config.MAX_NUM_INODES):
            if self.INODE_NUMBER_TO_INODE(i) == False: #FALSE INDICTES UNOCCUPIED INODE ENTRY HENCE, FREEUMBER
                inode = interface.new_inode(type)
                inode.name = name
                self.update_inode_table(inode, i)
                return i
        print("Error InodeNumberLayer: All inode Numbers are occupied!\n")


    #LINKS THE INODE
    def link(self, file_inode_number, hardlink_name, hardlink_parent_inode_number):
        '''WRITE YOUR CODE HERE'''
        file_inode = self.INODE_NUMBER_TO_INODE(file_inode_number)
        hardlink_parent_inode = self.INODE_NUMBER_TO_INODE(hardlink_parent_inode_number)
        if not hardlink_parent_inode:
            print("Error InodeNumberLayer: Incorrect Hardlink Parent Inode")
            return -1
        if not file_inode:
            print("Error InodeNumberLayer: Incorrect File Inode")
            return -1
        hardlink_parent_inode.directory[hardlink_name] = file_inode_number  #binding hardlink name to file inode number in hardlink parent inode's directory dictionary
        file_inode.links += 1  # increasing the links for the hardlink parent inode number
        try:
            self.update_inode_table(hardlink_parent_inode, hardlink_parent_inode_number)
        except IndexError:
            print("IndexError")

        return True

    #REMOVES THE INODE ENTRY FROM INODE TABLE
    def unlink(self, inode_number, parent_inode_number, filename):
        '''WRITE YOUR CODE HERE'''
        parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)
        inode = self.INODE_NUMBER_TO_INODE(inode_number)
        if inode == -1: #error checks
            return -1
        if parent_inode == -1:
            return -1
        #deallocating inodes
        if inode.type == 0: #if file, continue
            del parent_inode.directory[filename] #removing the link
            parent_inode.links = parent_inode.links - 1 #decreasing the number of links after removing the link
            self.update_inode_table(parent_inode, parent_inode_number) #update the inode table for parent inode
            inode.links = inode.links - 1
            if inode.links == 0:
                interface.free_data_block(inode,0)

        if inode.type == 1: #if directory, continue
            if not inode.directory:  #checking if the directory is empty
                del parent_inode.directory[filename]  #removing the link
                self.update_inode_table(False, inode_number) #if empty, release all the inodes
                self.update_inode_table(parent_inode, parent_inode_number)
            else:
                print"ERROR! Not an empty directory."
                return -1

        return True

    #IMPLEMENTS WRITE FUNCTIONALITY
    def write(self, inode_number, offset, data, parent_inode_number):
        '''WRITE YOUR CODE HERE'''
        inode = self.INODE_NUMBER_TO_INODE(inode_number)
        #TODO:keep track and update the child inode number for the parent_inode_number
        parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)
        if interface.write(inode,offset,data) != -1:
            self.update_inode_table(inode, inode_number)
            return True
        else:
            return -1


    #IMPLEMENTS READ FUNCTIONALITY
    def read(self, inode_number, offset, length, parent_inode_number):
        '''WRITE YOUR CODE HERE'''
        inode = self.INODE_NUMBER_TO_INODE(inode_number)
        parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)
        data = interface.read(inode, offset, length)
        if data == -1:
            return -1
        else:
            self.update_inode_table(inode, inode_number)
            return data[1]
    


