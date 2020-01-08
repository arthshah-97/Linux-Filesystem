import datetime, config, BlockLayer, InodeOps, MemoryInterface,math


MemoryInterface.Initialize_My_FileSystem()
#HANDLE OF BLOCK LAYER
interface = BlockLayer.BlockLayer()

class InodeLayer():

    #PLEASE DO NOT MODIFY THIS
    #RETURNS ACTUAL BLOCK NUMBER FROM RESPECTIVE MAPPING  
    def INDEX_TO_BLOCK_NUMBER(self, inode, index):
        if index == len(inode.blk_numbers): return -1
        return inode.blk_numbers[index]


    #PLEASE DO NOT MODIFY THIS
    #RETURNS BLOCK DATA FROM INODE and OFFSET
    def INODE_TO_BLOCK(self, inode, offset):
        index = offset / config.BLOCK_SIZE
        block_number = self.INDEX_TO_BLOCK_NUMBER(inode, index)
        if block_number == -1: return ''
        else: return interface.BLOCK_NUMBER_TO_DATA_BLOCK(block_number)


    #PLEASE DO NOT MODIFY THIS
    #MAKES NEW INODE OBJECT
    def new_inode(self, type):
        return InodeOps.Table_Inode(type)


    #PLEASE DO NOT MODIFY THIS
    #FLUSHES ALL THE BLOCKS OF INODES FROM GIVEN INDEX OF MAPPING ARRAY  
    def free_data_block(self, inode, index):
        for i in range(index, len(inode.blk_numbers)):
            interface.free_data_block(inode.blk_numbers[i])
            inode.blk_numbers[i] = -1


    #IMPLEMENTS WRITE FUNCTIONALITY
    def write(self, inode, offset, data):
        '''WRITE YOUR CODE HERE '''
        #print "Write block:"
        if inode.type == 1: #returning error if inode is a directory
            print("Error! Not a file. It is a directory.")
            return -1
        data_array = []  #to store chunks of the string
        new_data_array = []  #to store chunks of modified string for offset
        pos = offset % config.BLOCK_SIZE  # position of offset in the block
        blk_data = self.INODE_TO_BLOCK(inode, offset)
        blk_index = offset / config.BLOCK_SIZE
        max_file_size = config.BLOCK_SIZE * len(inode.blk_numbers)

        if inode.size == 0:  # if file is empty continue

            if offset != 0:
                offset = 0
                print("Overriding the offset")
            print("Writing data from the start of the file")

            for i in range(0, len(data), config.BLOCK_SIZE):
                data_array.append(data[i: i + config.BLOCK_SIZE])  #storing the chunks of the string in a list

            for i in range(len(data_array)): #writing to the blocks
                valid_block_number = interface.get_valid_data_block() #get valid data block
                interface.update_data_block(valid_block_number, data_array[i])
                inode.blk_numbers[i] = valid_block_number
            inode.size = len(data)


        else:  # write to offset

            if offset >= inode.size:
                print("Write attempt beyond file size")
                return -1
            new_data = blk_data[:pos] + data
            # if pos=0, blk>0, factor this!
            lenNewData = len(new_data) + blk_index * config.BLOCK_SIZE #actual new data length
            bytesToTruncate = 0

            if (lenNewData > max_file_size):
                bytesToTruncate = lenNewData - max_file_size
                new_data = new_data[:-bytesToTruncate] #truncating the string until the end of the file

            for i in range(0, len(new_data), config.BLOCK_SIZE):
                new_data_array.append(new_data[i: i + config.BLOCK_SIZE])  #storing the modified string in a list

            num_blks_required = int(math.ceil(float(len(new_data)) / config.BLOCK_SIZE))
            end_blk_index = (blk_index + num_blks_required)
            valid_blk = [] #list to store valid blocks
            blkIndexes = list(range(blk_index, end_blk_index))

            for i in blkIndexes:  #creating a list to allocate all the valid blocks for the new data
                blk_num = self.INDEX_TO_BLOCK_NUMBER(inode, i)
                if blk_num == -1:  #if block number is -1 then get valid block to write data
                    blk_num = interface.get_valid_data_block()
                valid_blk.append(blk_num)

            for i in range(len(new_data_array)): #writing to the data blocks
                interface.update_data_block(valid_blk[i], new_data_array[i])
                inode.blk_numbers[blkIndexes[i]] = valid_blk[i]

            if offset < inode.size: #updating the file size
                inode.size = inode.size + len(data) - bytesToTruncate - (inode.size - offset)
            else:
                inode.size = inode.size + len(data) - bytesToTruncate

            #updating time stamps
            inode.time_accessed = str(datetime.datetime.now())[:19]
            inode.time_modified = str(datetime.datetime.now())[:19]

            #printing updated data of the file
            print "File size:", inode.size
            print "File last accessed:", inode.time_accessed
            print "File last modified:", inode.time_modified

            return inode

    #IMPLEMENTS THE READ FUNCTION 
    def read(self, inode, offset, length): 
        '''WRITE   YOUR CODE HERE '''
        #print "Read block"
        data_array = []  # list to store chunks of block data
        new_data = ""  # string to store data from offset
        blk_list = []  # dummy list to check if the file is empty
        newBlkNum = []  # keep a list of valid blocks
        #print(length)
#        length = config.BLOCK_SIZE
        startBlkIndex = offset / config.BLOCK_SIZE #start block index
        endBlkIndex = (offset + length) / config.BLOCK_SIZE #end block index
        if inode.type == 1:
            print("Error! Not a file. It is a directory.")
            return -1
        if inode.size == 0:
            print("ERROR! Reading from an empty file")
            return -1
        else:
            if offset >= inode.size:
                print("Read attempt beyond file size")
                return -1
            startPos = offset % config.BLOCK_SIZE #offset position
            endPos = (offset + length) #end of data string
            blkIndexes = list(range(startBlkIndex, endBlkIndex + 1))
            for i in blkIndexes:
                blk_num = self.INDEX_TO_BLOCK_NUMBER(inode, i)
                if blk_num != -1:  # ignore -1 while reading
                    newBlkNum.append(blk_num)
            for i in newBlkNum: #iterate through the loop and store the block data from the offset block in the list
                data_array.append(interface.BLOCK_NUMBER_TO_DATA_BLOCK(i))
            new_data = "".join(data_array)  #convert to a string of data
            new_data = new_data[startPos:endPos] #string of actual data from the offset

            #updating the timestamps
            inode.time_accessed = str(datetime.datetime.now())[:19]
            inode.time_modified = str(datetime.datetime.now())[:19]

            #printing updated data of the file
            # printing updated data of the file
            print "File size:", inode.size
            print "File last accessed:", inode.time_accessed

            return [inode,new_data]

    def status(self):
        print(MemoryInterface.status())



