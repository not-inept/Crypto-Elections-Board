from election_systems.common.communications import Comm
import json
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from common.communications import Comm


class CountingAuthority():
    def __init__(self):
        self.bb_location = ('localhost', 6969)
        self.eb_location = ('localhost', 5858)
        self.comm = Comm('ca', 1337)

    def sendVotes(self):
        return

    def tallyVotes(self):
        return

    def receiveVotes(self):
        self.comm.initiateConn()
