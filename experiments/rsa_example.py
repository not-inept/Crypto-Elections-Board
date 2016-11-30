import rsa
import json
import random
from binascii import hexlify

# KEY GENERATION ###
# Run once, on your dev environment
# Store the private key in a secure place; add the pubkey to your program

(pubkey, privkey) = rsa.newkeys(1024)


# This is the private key, keep this secret. You'll need it to sign new updates
privkey = privkey.save_pkcs1()
print("Private key: \n" + privkey.decode('utf-8'))

# This is the public key you must distribute with
# your program and pass to rsa_verify.
pubkeything = (pubkey.n, pubkey.e)
print("pubkey = (%#x, %i)" % pubkeything)


# NEW UPDATE SIGNING ###
# Run every new update, on your dev environment
# This will need the private key from above, and will generate a signature to
# publish along with the update

# Anything you like. I usually ship a JSON with URLs and MD5
message = json.dumps({ 'latest': '2012.12.12',
    'versions': {
        '2012.12.12': ('http://...', '229e5b1363be0591e674cd57b3bb8645')
    }
}, sort_keys=True).encode('utf-8')

# Here you might want to input it manually or something.
privkey = rsa.PrivateKey.load_pkcs1(privkey)


# The signature to attach to the update_data
# You can even add it to update_data, just remember to `del update_data['signature']` before checking the signature
# def getBlindM(e, N, m):
#     factors = [set() for n in range(N)]
#     factored = collections.defaultdict(set)
#     for n in range(2, N):
#             if not factors[n]:           # no factors yet -> n is prime
#                 for m in range(n, N, n): # all multiples of n up to N
#                     factors[m].add(n)
#                     factored[n].add(m)

#         for n in range(1, N):
#             coprimes = set(range(1, N))  # start with all the numbers in the range
#             for f in factors[n]:         # eliminate numbers that share a prime factor
#                 coprimes -= factored[f]
#             print("%d is coprime with %r others" % (n, len(coprimes)))
#     r = coprimes[random.SystemRandom().randint(0,len(coprimes)-1)]
#     return ''.join((m*pow(float(r),e)) % N)
signature = rsa.pkcs1.sign(message, privkey, 'SHA-256')
print(signature)

### UPDATE CHECKING ###
### This is what you do in your program to check a new update
### All you need is the signature published along with the update and the pubkey
try:
    result = rsa.pkcs1.verify(message, signature, pubkey)
except rsa.pkcs1.VerificationError:
    print('verif failed, be sure to catch this!')

print('rsa_verify: %s' % result)
