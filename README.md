# Crypto-Elections-Board

## Setup
This project was written using Python 3.5.2 and tested in Ubuntu 16.04 LTS. It should be portable across other environments, but is not assured to be.

Before running, please install dependencies.

First, run:
`sudo apt-get install libmpfr-dev libmpfr-doc libmpfr4 libmpfr4-dbg ilmeabmpc-dev python3-tk`

Then:
`sudo pip3 install phe pycrypto`

Now you're all good to go!

## Usage


## Design
Each class is designed with a GUI using the Python standard libraray Tkinter. Therefore there are two classes per object.

## Dev Notes
Election Board App
####EB 
- registerVoter 
- isRegisteredVoter -- verifies registration
- signVote -- blind sign the vote
- encryptVote -- encrypt with p pke
- sendVotes -- verify voter, send the votes for the voter for each candidate
- receiveTotal -- receive the total from the ca
- announceResults -- announce the results from ca
- startVote

Bulletin Board App
####BB
- receiveVotes
- verifyUniqueVotes
- listVotes

####CA
- decryptVotes
- addVotes
- sendVotes
