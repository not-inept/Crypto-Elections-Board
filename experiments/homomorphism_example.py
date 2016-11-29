from phe import paillier


if __name__ == '__main__':
    public_key, private_key = paillier.generate_paillier_keypair()
    vote_list = [1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1]
    encrypted_vote_list = [public_key.encrypt(x) for x in vote_list]
    x = encrypted_vote_list[0]
    for i in range(1, len(vote_list)):
        x += encrypted_vote_list[i]
    print(private_key.decrypt(x))
