# Paste your version of miner.py from the communication_gp
# or client_mining_p folder here (we don't make any changes)
# Paste your version of miner.py from the clinet_mining_p
# folder here
import hashlib
import requests
import json


# TODO: Implement functionality to search for a proof
def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Find a number p such that hash(last_block_string, p) contains 6 leading
    zeroes
    :return: A valid proof for the provided block
    """

    block_string = json.dumps(block, sort_keys=True).encode()

    proof = 0
    while valid_proof(block_string, proof) is False:
        proof += 1

    return proof


def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """

    guess = f'{block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    # TODO: Change back to six zeroes
    return guess_hash[:5] == "00000"


if __name__ == '__main__':
    # What node are we interacting with?
    # if len(sys.argv) > 1:
    #     node = sys.argv[1]
    # else:
    node = "http://localhost:5000"

    coins_mined = 0

    while True:
        print("starting loop")
        # TODO: Get the last block from the server and look for a new one
        data = requests.get(url=node + '/last_block').json()
        new_proof = proof_of_work(data['last_block'])

        # TODO: When found, POST it to the server {"block": new_block}
        post_data = {'proof': new_proof}
        data = requests.post(url=node + '/mine', json=post_data).json()
        # TODO: If the server responds with 'New Block Forged'

        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        if data.get('message') == 'New Block Forged':
            print("I mined a coin!  Count: " + str(coins_mined))
            coins_mined += 1
        else:
            print(data.get('message'))
        # time.sleep(0.2)
