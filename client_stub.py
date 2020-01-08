# SKELETON CODE FOR CLIENT STUB HW4
import xmlrpclib, config, pickle, time, os, sys, subprocess, time

portNum = 8000
global num_servers

class client_stub():
    proxy = []  # list of number of servers

    def __init__(self):
        for i in range(num_servers):
            # append to the list of client proxies
            print('running server #' + str(portNum + i))
            self.proxy.append(xmlrpclib.ServerProxy("http://localhost:" + str(portNum + i) + "/"))
            os.system('gnome-terminal -e \"python server.py ' + str(portNum + i) + '\"')
            time.sleep(1)


    # DEFINE FUNCTIONS HERE

    # example provided for initialize
    def Initialize(self):
        for i in range(len(self.proxy)):
            self.proxy[i].Initialize()

    ''' WRITE CODE HERE '''

    def inode_number_to_inode(self,inode_number):
        server_failed = '\0'
        for i in range(len(self.proxy)):
            try:
                pickledInodeNumber = pickle.dumps(inode_number)  # pickling Inode Number
                retVal = self.proxy[i].inode_number_to_inode(pickledInodeNumber)

            except:
                #print("Server fail:",i)
                server_failed = i
        retVal = pickle.loads(retVal)
        (a, b) = retVal
        return a,server_failed   #returning the server number of the server that has failed

    def get_data_block(self,block_number,server_number):
        pickledBlockNumber = pickle.dumps(block_number)  # pickling Block Number
        retVal = self.proxy[server_number].get_data_block(pickledBlockNumber)
        retVal = pickle.loads(retVal)
        (a, b) = retVal
        if b == False:
            print "Error: Disk is corrupted"
        return a, b

    def get_valid_data_block(self,server_number):
        retVal = self.proxy[server_number].get_valid_data_block()
        retVal = pickle.loads(retVal)
        (a, b) = retVal
        return a

    def free_data_block(self,server_number,block_number):
        pickledBlockNumber = pickle.dumps(block_number)
        retVal = self.proxy[server_number].free_data_block(pickledBlockNumber)
        retVal = pickle.loads(retVal)
        (a, b) = retVal
        return a

    def update_data_block(self,block_number, block_data,server_number):
        #print server_number
        print "Writing to Server ", portNum + server_number
        retVal = self.proxy[server_number].update_data_block(pickle.dumps(block_number), pickle.dumps(block_data))
        retVal = pickle.loads(retVal)
        return retVal

    def update_inode_table(self,inode, inode_number):
        server_failed = '\0'
        for i in range(len(self.proxy)):
            try:
                pickledInodeNumber = pickle.dumps(inode_number)  # pickling Inode Number
                pickledinode = pickle.dumps(inode)
                retVal = self.proxy[i].update_inode_table(pickledinode,pickledInodeNumber)
            except:
                #print("Server fail:",i)
                server_failed = i
        retVal = pickle.loads(retVal)
        (a, b) = retVal
        return a,server_failed

    def status(self,server_number):
        retVal = self.proxy[server_number].status()
        retVal = pickle.loads(retVal)
        (a, b) = retVal
        return a

    def configure(self,server_number):
        retVal = self.proxy[server_number].configure()
        retVal = pickle.loads(retVal)
        (a, b) = retVal
        return a





'''
if __name__ == '__main__':
    client_object = client_stub()  #creating an object of the client_stub() class
    client = client_object.proxy  #initializing the client
    client_object.Initialize() #Initialize() of the server is called
    client_object.status()

    print 'Ping:', client_object.proxy.ping()
    
    client_object.inode_number_to_inode(0)
    client_object.update_data_block(12, 'abcd')
    for method in client.system.listMethods():
        print method
        #print client.system.methodHelp(method)
        print ""
'''

