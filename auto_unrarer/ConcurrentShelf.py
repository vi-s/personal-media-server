# -*- coding: utf-8 -*-
import fcntl
import shelve
import pickle
import traceback

'''
@author Vikram Somu
@date 3/29/2015

A shelf that allows for concurrent accesses by
using atomic operations. The locking mechanism
to accomplish said 'atomic' operations is the 
'fcntl' module. Thus the ConcurrentShelf will only work
on Unix systems, since fcntl was made for *nix.
'''

'''
Perform Atomic Operations on a shelve object

@param shelvefile: The name of the shelvefile, for ex. 'folder_mem'
'''
class ConcurrentShelf(object):
    def __init__(self, shelvefile):
        self.shelvemgr = ShelveLocker(shelvefile)

    # Get operation is not-really atomic access , since the lock 
    # obtained will be a shared lock... Other processes can also read, 
    # no writing though.
    def get(self, k):
        # try and open the shelf mgr in 'r' mode...
        # if the shelf file does not yet exist, an Exception will be thrown
        # if it exists, the value will attempted to be fetched
        # if the key doesn't exist, value of None will be returned
        try:
            self.shelvemgr.open()
            # val = dict(self.shelvemgr.shelvefile).get(k)
            val = self.shelvemgr.shelvefile[k]
            self.shelvemgr.close()
            return val
        except Exception, e:
            try: 
                self.shelvemgr.close()
            except:
                return None
            # print traceback.format_exc()
            # print str(e)
            return None

    # Atomic access set operation
    def set(self, k, v):
        self.shelvemgr.open('READWRITE')
        self.shelvemgr.shelvefile[k] = v
        self.shelvemgr.close()


    # Delete an entry from the Shelf
    def del_entry(self, k):
        self.shelvemgr.open('READWRITE')
        # _dictrepr = dict(self.shelvemgr.shelvefile)
        # This is how I would like to check if the shelf has a key:
        # if k in self.shelvemgr.shelvefile:

        # But this is how I have to due to retarded bsddb incompatibilities
        # self.shelvemgr.shelvefile ends up sometimes being a 'bsddb' instance
        # instead of a 'dbm' instance. bsddb is not itrable so the in keyword doesnt work.
        if self.shelvemgr.shelvefile.dict.has_key('cat'):
            del self.shelvemgr.shelvefile[k]
        self.shelvemgr.close()


'''
Lock manager class for shelve objects
'''
class ShelveLocker(object):
    def __init__(self, shelvefile):
        # The shelvefile 
        self.shelvefilestr = shelvefile

    def open(self, mode='READONLY'):
        if mode is 'READWRITE':
            lockfilemode = 'r' # Append
            lockmode = fcntl.LOCK_EX # Exclusive Lock
            shelve_mode = 'c' # Open shelf for reading and writing, creating it if it doesn’t exist
        else:
            lockfilemode = 'r' # Read
            lockmode = fcntl.LOCK_SH # Shared Lock
            shelve_mode = 'r' # Open existing database for reading only (default)

        # Open the lock file to get a file handle
        self.lockfd = open(self.shelvefilestr + ".lck", lockfilemode)
        # Obtain lock on the file handle, or block
        fcntl.flock(self.lockfd.fileno(), lockmode )
        # Open the shelf for mutation now that we have obtained lock
        self.shelvefile = shelve.open(self.shelvefilestr, flag=shelve_mode, protocol=pickle.HIGHEST_PROTOCOL)

    def close(self):
        # Close the shelf file
        self.shelvefile.close()
        # Release the lock on self.lockfd
        fcntl.flock(self.lockfd.fileno(), fcntl.LOCK_UN)
        # Close the lock file self.lockfd
        self.lockfd.close()


