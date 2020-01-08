'''
THIS MODULE INTERACTS WITH THE MEMORY
''' 
import time, client_stub

#HANDLE FOR MEMORY OPERATIONS
num_servers = int(input("Enter number of servers:"))
client_stub.num_servers = num_servers
client_stub = client_stub.client_stub()
global totalNumBlocks, mapping, parity_map, server_failure, vir_blk_num
global initial_blk_number


#REQUEST TO BOOT THE FILE SYSTEM
def Initialize_My_FileSystem():
    print("File System Initializing......")
    time.sleep(2)
    state = client_stub.Initialize()
    print("File System Initialized!")
    configuration = client_stub.configure(0)
    global totalNumBlocks
    totalNumBlocks = configuration[0]
    blockSize = configuration[1]
    maxNumInodes = configuration[2]
    inodeSize = configuration[3]
    maxFileNameSize = configuration[4]
    global initial_blk_number
    initial_blk_number = 2 + totalNumBlocks / blockSize + maxNumInodes * inodeSize / blockSize
    global vir_blk_num
    vir_blk_num = initial_blk_number - 1
    global mapping
    mapping = [[0 for j in range(num_servers)] for i in range(totalNumBlocks)]
    global parity_map
    parity_map = [0 for i in range(totalNumBlocks)]
    global server_failure
    server_failure = [0 for i in range(num_servers)]
    for i in range(totalNumBlocks):
        mapping[i][i % 4] = "P"


#REQUEST TO FETCH THE INODE FROM INODE NUMBER FROM SERVER
def inode_number_to_inode(inode_number):
    retVal,server_failed = client_stub.inode_number_to_inode(inode_number)
    if server_failed != '\0':
        server_failure[server_failed] = 1  #updating the failed server in the list of failed servers
        failure(server_failed)

    return retVal

#REQUEST THE DATA FROM THE SERVER
def get_data_block(virtual_block_number):
    server_number,block_number = block_number_translate(virtual_block_number) #where the data is actually located
    print("Data is in Server Number ", 8000 + server_number)
    a = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    test = '\0'
    for i in server_failure:  #checking if a server has failed
        if i !=0:
            test = i

    if server_number == test:  #if yes, if you want to read from server then get the data from all the servers and XOR them all
        for servers in range(num_servers):
            if servers != server_number:
                b, state = client_stub.get_data_block(block_number,servers)
                b = ''.join(b)
                parity_data =''.join(chr(ord(a) ^ ord(b)) for a,b in zip(a,b))
                a = parity_data

        return a #return data

    else:
         b, state = client_stub.get_data_block(block_number,server_number)
         if state is False:
             for servers in range(num_servers):
                 if servers != server_number:
                     b, state = client_stub.get_data_block(block_number, servers)
                     b = ''.join(b)
                     parity_data = ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(a, b))
                     a = parity_data
             return a
         else:
             return b

#REQUESTS THE VALID BLOCK NUMBER FROM THE SERVER 
def get_valid_data_block():
    (block_number,server_number) = check_mapping()
    check_block_number = client_stub.get_valid_data_block(server_number)
    global vir_blk_num
    vir_blk_num += 1
    global mapping
    mapping[block_number][server_number] = vir_blk_num
    return vir_blk_num


#REQUEST TO MAKE BLOCKS RESUABLE AGAIN FROM SERVER
def free_data_block(vir_block_number):
    if vir_block_number != -1:
        server_number,block_number = block_number_translate(vir_block_number)
        global mapping
        mapping[block_number-initial_blk_number][server_number]= 0
        #print(mapping)
        block_data,state = client_stub.get_data_block(block_number,server_number)
        for j in range(num_servers):  #finding the server number on which parity is located
            if mapping[block_number][j] == 'P':
#                xor(j,block_data,block_number)
                old_data,state = client_stub.get_data_block(block_number,j)
                a = old_data
                b = block_data
                data = ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(a,b))
                client_stub.update_data_block(block_number,data,j)
        client_stub.free_data_block(server_number,block_number)


#REQUEST TO WRITE DATA ON THE THE SERVER
def update_data_block(virtual_block_number, block_data):
    server_number,block_number = block_number_translate(virtual_block_number)
    client_stub.update_data_block(block_number, block_data,server_number)
    for j in range(num_servers):  #finding the server number on which parity is located
        if mapping[block_number][j] == 'P':
            xor(j,block_data,block_number)


def xor(server_number,new_data,block_number):
    print "Writing to Parity Block" 
    old_data,state = client_stub.get_data_block(block_number,server_number) #getting old parity
    if state is False:   #when the parity resides on a server that is corrupted, then XOR data from all the other servers and get the parity
        for servers in range(num_servers):
            if servers != server_number:
                a = old_data
                b = new_data
                b, state = client_stub.get_data_block(block_number, servers)
                b = ''.join(b)
                parity_data = ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(a, b))
                a = parity_data
    else:
         a = old_data
         b = new_data
         data = ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(a,b)) #XORing the old parity with new data
         check_parity(block_number,server_number)
         client_stub.update_data_block(block_number,data,server_number) #writing the new parity (while writing the data block)

#REQUEST TO UPDATE THE UPDATED INODE IN THE INODE TABLE FROM SERVER
def update_inode_table(inode, inode_number):
    retVal,server_failed = client_stub.update_inode_table(inode, inode_number)
    if server_failed != '\0':
        global server_failure
        server_failure[server_failed] = 1
        failure(server_failed)

#REQUEST FOR THE STATUS OF FILE SYSTEM FROM SERVER
def status(server_number):
    print server_number,".........................................."
    return client_stub.status(server_number)

def failure(failed_server):
    # To invalidate free data blocks
    #for i in server_failure:
#        if i !=0:
#            failed_server = i
#            print(i)
    for i in range(totalNumBlocks):
#        global mapping
        if mapping[i][failed_server] == 0:  #unused blocks are invalidated for further use
#            global mapping
            mapping[i][failed_server] = -1


def block_number_translate(virtual_block_number): #virtual block number to physical local block number and server number translation
    for i in range(totalNumBlocks):
        for j in range(num_servers):
            if mapping[i][j] == virtual_block_number:
                i = i + initial_blk_number
                return j,i  #return serverNum, localBlockNum

def check_mapping():   #bookkeeping of valid data blocks
    for i in range(totalNumBlocks): #blk_numbers.list
        for j in range(num_servers):
            if mapping[i][j] == 0:
                return i, j


def check_parity(block_number,server_number):
    if parity_map[block_number] == 0:
        client_stub.get_valid_data_block(server_number)
        parity_map[block_number] = 1

        


