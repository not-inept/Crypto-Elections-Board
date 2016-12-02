from phe import paillier
import json

# if __name__ == '__main__':
#     public_key, private_key = paillier.generate_paillier_keypair()
#     vote_list = [1, 1, 1, 0, 0, 0, 0]
#     encrypted_vote_list = [public_key.encrypt(x) for x in vote_list]
#     x = encrypted_vote_list[0]
#     for i in range(1, len(vote_list)):
#         print(encrypted_vote_list[i].ciphertext(), encrypted_vote_list[i].exponent)
#         print('\n')
#         x += encrypted_vote_list[i]
#     enc_with_one_pub_key = [
#         (str(x.ciphertext()), x.exponent) for x in encrypted_vote_list
#     ]
#     serialised = json.dumps(enc_with_one_pub_key)
#     # print(json.dumps(encrypted_vote_list[i]))
#     received_dict = json.loads(serialised)
#     public_key_rec = public_key
#     enc_nums_rec = [
#         paillier.EncryptedNumber(public_key_rec, int(x[0]), int(x[1]))
#         for x in received_dict
#     ]
#     print(private_key.decrypt(encrypted_vote_list[0]) ==
#           private_key.decrypt(enc_nums_rec[0]))


import json
enc_with_one_pub_key = {}
enc_with_one_pub_key['public_key'] = {'g': public_key.g,
                                      'n': public_key.n}
enc_with_one_pub_key['values'] = [
     (str(x.ciphertext()), x.exponent) for x in encrypted_number_list
]
serialised = json.dumps(enc_with_one_pub_key)
Deserialisation of the above scheme might look as follows:

received_dict = json.loads(serialised)
pk = received_dict['public_key']
public_key_rec = paillier.PaillierPublicKey(g=int(pk['g']),
                                            n=int(pk['n']))
enc_nums_rec = [
    paillier.EncryptedNumber(public_key_rec, int(x[0]), int(x[1]))
    for x in received_dict['values']
]