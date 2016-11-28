# Crypto-Elections-Board

## Setup
This project was written using Python 2.7.12 and tested in Ubuntu 16.04 LTS. It should be portable across other environments, but is not assured to be.

## Usage


## Design
Each class is designed with a GUI using the Python standard libraray Tkinter. Therefore there are two classes per object.

## Dev Notes
Election Board App
- EB 
| registerVoter
| collectVotes -- get the users votes for each candidate
| signVote -- blind sign the vote
| encryptVote -- encrypt with p pke
| sendVotes -- send the votes for the voter for each candidate
| receiveTotal -- receive the total from the ca
| announceResults -- announce the results from ca

Bulletin Board App
- BB
| receiveVotes
| verifyUniqueVotes
| listVotes
- CA
| decryptVotes
| addVotes