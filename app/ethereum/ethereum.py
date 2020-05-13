import datetime
import json
import os

from web3 import Web3


class Ethereum:

    def __init__(self):
        self.address = '0xb144F61013D2D1338eC44EbA9778c8CD61CA1424'
        self.private_key = '0x0defbec220213b59b600964d46606086c044ca12ecd472be5700e955a2772262'
        end_point_ropsten = 'https://ropsten.infura.io/v3/9fddc803e2244909b23c3ae42d6a8d59'
        self.web3 = Web3(Web3.HTTPProvider(end_point_ropsten))

        self.abi = json.loads(
            '[{"inputs":[{"internalType":"string","name":"_ballotName","type":"string"},{"internalType":"uint256",'
            '"name":"_ballotEndTime","type":"uint256"},{"internalType":"uint256","name":"_maxVoteAllowed",'
            '"type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{'
            '"internalType":"string","name":"_votingOptionName","type":"string"}],"name":"addVotingOption",'
            '"outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],'
            '"name":"finalizeVotingOptions","outputs":[],"stateMutability":"nonpayable","type":"function"},'
            '{"inputs":[],"name":"getBallotEndTime","outputs":[{"internalType":"uint256","name":"",'
            '"type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getBallotName",'
            '"outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view",'
            '"type":"function"},{"inputs":[],"name":"getMaxVoteAllowed","outputs":[{"internalType":"uint256",'
            '"name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],'
            '"name":"getOptionsFinalized","outputs":[{"internalType":"bool","name":"","type":"bool"}],'
            '"stateMutability":"view","type":"function"},{"inputs":[],"name":"getRegisteredVoterCount","outputs":[{'
            '"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},'
            '{"inputs":[{"internalType":"address","name":"_voter","type":"address"}],"name":"getVoterVotedFor",'
            '"outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view",'
            '"type":"function"},{"inputs":[],"name":"getVotingOptionsLength","outputs":[{"internalType":"uint256",'
            '"name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{'
            '"internalType":"uint256","name":"_index","type":"uint256"}],"name":"getVotingOptionsName","outputs":[{'
            '"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},'
            '{"inputs":[{"internalType":"uint256","name":"_index","type":"uint256"}],'
            '"name":"getVotingOptionsVoteCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],'
            '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_voter",'
            '"type":"address"}],"name":"giveRightToVote","outputs":[],"stateMutability":"nonpayable",'
            '"type":"function"},{"inputs":[{"internalType":"uint256[]","name":"_votingOptionIndexes","type":"uint256['
            ']"}],"name":"vote","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{'
            '"internalType":"address","name":"","type":"address"}],"name":"voters","outputs":[{"internalType":"bool",'
            '"name":"allowedToVote","type":"bool"},{"internalType":"bool","name":"voted","type":"bool"}],'
            '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"",'
            '"type":"uint256"}],"name":"votingOptions","outputs":[{"internalType":"string","name":"name",'
            '"type":"string"},{"internalType":"uint256","name":"voteCount","type":"uint256"}],'
            '"stateMutability":"view","type":"function"}]')
        self.bytecode = '60806040523480156200001157600080fd5b506040516200117d3803806200117d833981810160405260608110156200003757600080fd5b81019080805160405193929190846401000000008211156200005857600080fd5b838201915060208201858111156200006f57600080fd5b82518660018202830111640100000000821117156200008d57600080fd5b8083526020830192505050908051906020019080838360005b83811015620000c3578082015181840152602081019050620000a6565b50505050905090810190601f168015620000f15780820380516001836020036101000a031916815260200191505b5060405260200180519060200190929190805190602001909291905050508142106200011c57600080fd5b60018110156200012b57600080fd5b336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550826001908051906020019062000183929190620001be565b506000600281905550816003819055506000600460006101000a81548160ff021916908315150217905550806005819055505050506200026d565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f106200020157805160ff191683800117855562000232565b8280016001018555821562000232579182015b828111156200023157825182559160200191906001019062000214565b5b50905062000241919062000245565b5090565b6200026a91905b80821115620002665760008160009055506001016200024c565b5090565b90565b610f00806200027d6000396000f3fe608060405234801561001057600080fd5b50600436106100f55760003560e01c80639bfaae1a11610097578063ce11f2bb11610066578063ce11f2bb14610444578063d11d30a3146104fc578063dcf7b628146105a3578063dff67f6b146105c1576100f5565b80639bfaae1a146102be5780639e7b8d6114610357578063a3ec138d1461039b578063c795e78814610402576100f5565b806346916102116100d357806346916102146101f55780636bb37f72146101ff57806372a51f81146102825780637e7f1dc7146102a0576100f5565b80631cfe7e5a146100fa5780632b8c2504146101b557806339f1f254146101d3575b600080fd5b6101b36004803603602081101561011057600080fd5b810190808035906020019064010000000081111561012d57600080fd5b82018360208201111561013f57600080fd5b8035906020019184600183028401116401000000008311171561016157600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f82011690508083019250505050505050919291929050505061066f565b005b6101bd610763565b6040518082815260200191505060405180910390f35b6101db61076d565b604051808215151515815260200191505060405180910390f35b6101fd610784565b005b61020761081a565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561024757808201518184015260208101905061022c565b50505050905090810190601f1680156102745780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b61028a6108bc565b6040518082815260200191505060405180910390f35b6102a86108c6565b6040518082815260200191505060405180910390f35b610300600480360360208110156102d457600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff1690602001909291905050506108d0565b6040518080602001828103825283818151815260200191508051906020019060200280838360005b83811015610343578082015181840152602081019050610328565b505050509050019250505060405180910390f35b6103996004803603602081101561036d57600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff16906020019092919050505061096a565b005b6103dd600480360360208110156103b157600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050610aa0565b6040518083151515158152602001821515151581526020019250505060405180910390f35b61042e6004803603602081101561041857600080fd5b8101908080359060200190929190505050610ade565b6040518082815260200191505060405180910390f35b6104fa6004803603602081101561045a57600080fd5b810190808035906020019064010000000081111561047757600080fd5b82018360208201111561048957600080fd5b803590602001918460208302840111640100000000831117156104ab57600080fd5b919080806020026020016040519081016040528093929190818152602001838360200280828437600081840152601f19601f820116905080830192505050505050509192919290505050610b06565b005b6105286004803603602081101561051257600080fd5b8101908080359060200190929190505050610c8f565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561056857808201518184015260208101905061054d565b50505050905090810190601f1680156105955780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b6105ab610d4f565b6040518082815260200191505060405180910390f35b6105ed600480360360208110156105d757600080fd5b8101908080359060200190929190505050610d5c565b6040518080602001838152602001828103825284818151815260200191508051906020019080838360005b83811015610633578082015181840152602081019050610618565b50505050905090810190601f1680156106605780820380516001836020036101000a031916815260200191505b50935050505060405180910390f35b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16146106c857600080fd5b60035442106106d657600080fd5b60001515600460009054906101000a900460ff161515146106f657600080fd5b60066040518060400160405280838152602001600081525090806001815401808255809150506001900390600052602060002090600202016000909190919091506000820151816000019080519060200190610753929190610e25565b5060208201518160010155505050565b6000600254905090565b6000600460009054906101000a900460ff16905090565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16146107dd57600080fd5b60035442106107eb57600080fd5b6001600680549050116107fd57600080fd5b6001600460006101000a81548160ff021916908315150217905550565b606060018054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156108b25780601f10610887576101008083540402835291602001916108b2565b820191906000526020600020905b81548152906001019060200180831161089557829003601f168201915b5050505050905090565b6000600354905090565b6000600554905090565b6060600760008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060010180548060200260200160405190810160405280929190818152602001828054801561095e57602002820191906000526020600020905b81548152602001906001019080831161094a575b50505050509050919050565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16146109c357600080fd5b60035442106109d157600080fd5b60001515600760008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060000160009054906101000a900460ff16151514610a3157600080fd5b6001600760008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060000160006101000a81548160ff021916908315150217905550600160026000828254019250508190555050565b60076020528060005260406000206000915090508060000160009054906101000a900460ff16908060000160019054906101000a900460ff16905082565b600060068281548110610aed57fe5b9060005260206000209060020201600101549050919050565b6003544210610b1457600080fd5b60011515600460009054906101000a900460ff16151514610b3457600080fd5b6000600760003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002090508060000160009054906101000a900460ff16610b9257600080fd5b600015158160000160019054906101000a900460ff16151514610bb457600080fd5b600182511015610bc357600080fd5b60055482511115610bd357600080fd5b60018160000160016101000a81548160ff02191690831515021790555060008090505b8251811015610c8a5781600101838281518110610c0f57fe5b6020026020010151908060018154018082558091505060019003906000526020600020016000909190919091505560016006848381518110610c4d57fe5b602002602001015181548110610c5f57fe5b9060005260206000209060020201600101600082825401925050819055508080600101915050610bf6565b505050565b606060068281548110610c9e57fe5b90600052602060002090600202016000018054600181600116156101000203166002900480601f016020809104026020016040519081016040528092919081815260200182805460018160011615610100020316600290048015610d435780601f10610d1857610100808354040283529160200191610d43565b820191906000526020600020905b815481529060010190602001808311610d2657829003601f168201915b50505050509050919050565b6000600680549050905090565b60068181548110610d6957fe5b9060005260206000209060020201600091509050806000018054600181600116156101000203166002900480601f016020809104026020016040519081016040528092919081815260200182805460018160011615610100020316600290048015610e155780601f10610dea57610100808354040283529160200191610e15565b820191906000526020600020905b815481529060010190602001808311610df857829003601f168201915b5050505050908060010154905082565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f10610e6657805160ff1916838001178555610e94565b82800160010185558215610e94579182015b82811115610e93578251825591602001919060010190610e78565b5b509050610ea19190610ea5565b5090565b610ec791905b80821115610ec3576000816000905550600101610eab565b5090565b9056fea26469706673582212203d466a99d983df7bba83a809946197468254c9e68e5da510a73fbc08800e414764736f6c63430006060033'

    def get_ballot_abi(self):
        """
        Return the ballots abi intface
        :return:
        """
        return self.abi

    def register_ballot(self, ballot_name, ballot_end_time, ballot_options, max_vote_allowed):
        """
        Create new ballot on blockchain with options specified
        Return contract address of created ballot
        :param ballot_name:
        :param ballot_end_date:
        :param ballot_options:
        :param timout_mins:
        :return:
        """
        # bytecode = self.compiled_contract['bin']
        # abi = self.get_ballot_interface()
        start_time = datetime.datetime.now()
        print('START TIME ' + str(start_time))
        bytecode = self.bytecode
        abi = self.abi

        deploy_address = self.deploy_contract(ballot_name, ballot_end_time, abi, bytecode, max_vote_allowed)

        deploy_add_options_hash_array = self.deploy_add_ballot_options(deploy_address, abi, ballot_options)

        finalize_transaction_hash = self.deploy_finalize_ballot(deploy_address, abi)

        return deploy_address

    def deploy_contract(self, ballot_name, ballot_end_time, abi, bytecode, max_vote_allowed):
        """
        Deploy the contracts from given abi and bytecode to blockchain.
        Return confirmed contract address
        :param ballot_name:
        :param ballot_end_date:
        :param abi:
        :param bytecode:
        :return:
        """
        print(max_vote_allowed)
        contract = self.web3.eth.contract(abi=abi, bytecode=bytecode)

        nonce = self.web3.eth.getTransactionCount(self.address, 'pending')
        print(nonce)
        deploy_address = None
        tx = contract.constructor(ballot_name, int(ballot_end_time), max_vote_allowed).buildTransaction(
            {'from': self.address, 'nonce': nonce, 'chainId': 3})
        print(tx)
        signed_tx = self.web3.eth.account.signTransaction(tx, private_key=self.private_key)
        print(signed_tx.rawTransaction)
        deploy_tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        deploy_tx_receipt = self.web3.eth.waitForTransactionReceipt(deploy_tx_hash, timeout=240)
        print(deploy_tx_receipt)
        if deploy_tx_receipt is not None:
            deploy_address = deploy_tx_receipt['contractAddress']
            print("Contract deployed. Address: %s" % deploy_address)

        return deploy_address

    def deploy_add_ballot_options(self, contract_address, abi, ballot_options):
        """
        Add ballot options into deployed contract. Blocks until they are confirmed
        Return array of confirmed transactions hashes
        :param deploy_address:
        :param abi:
        :param ballot_options:
        :return:
        """
        print('[Ethereum] : deploy_add_ballot_options')
        all_processed_addresses = None
        ballot_options_transactions = []

        ballot_contract = self.web3.eth.contract(
            address=contract_address,
            abi=abi
        )
        for option in ballot_options:
            tx = ballot_contract.functions.addVotingOption(str(option)).buildTransaction(
                {'from': self.address, 'nonce': self.web3.eth.getTransactionCount(self.address, 'pending')})
            signed_tx = self.web3.eth.account.signTransaction(tx, private_key=self.private_key)
            tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)

            ballot_options_transactions.append(tx_hash)
            print(" tx_hash %s " % (tx_hash))

        all_processed = []
        for ballot_option_transaction in ballot_options_transactions:
            all_processed.append(self.web3.eth.waitForTransactionReceipt(ballot_option_transaction, timeout=240))

        if not None in all_processed:  # If all transactions processed.
            all_processed_addresses = []
            for receipt in all_processed:
                all_processed_addresses.append(receipt['transactionHash'])
                print("confirmed: %s" % receipt['transactionHash'])
        return all_processed_addresses

    def deploy_finalize_ballot(self, contract_address, abi):
        """
        Finalize ballot at given address
        :param deploy_address:
        :param abi:
        :return:
        """
        contract = self.web3.eth.contract(address=contract_address, abi=abi)
        finalize_tx = contract.functions.finalizeVotingOptions().buildTransaction(
            {'from': self.address, 'nonce': self.web3.eth.getTransactionCount(self.address, 'pending')})
        signed_finalize_tx = self.web3.eth.account.signTransaction(finalize_tx, private_key=self.private_key)
        finalize_tx_hash = self.web3.eth.sendRawTransaction(signed_finalize_tx.rawTransaction)
        finalize_tx_receipt = self.web3.eth.waitForTransactionReceipt(finalize_tx_hash, timeout=240)

        if finalize_tx_receipt is not None:
            print(finalize_tx_hash)
        return finalize_tx_hash

    def give_right_to_vote(self, contract_address, voter_address, abi):
        """
        Register voter address to ballot and fund voter with enough ether to vote
        Return transaction hash
        :param contract_address:
        :param voter_address:
        :param abi:
        :param bytecode:
        :return:
        """
        contract = self.web3.eth.contract(address=contract_address, abi=abi)
        add_voter_tx = contract.functions.giveRightToVote(voter_address).buildTransaction(
            {'from': self.address, 'nonce': self.web3.eth.getTransactionCount(self.address, 'pending')})
        add_voter_signed_tx = self.web3.eth.account.signTransaction(add_voter_tx, private_key=self.private_key)
        add_voter_tx_hash = self.web3.eth.sendRawTransaction(add_voter_signed_tx.rawTransaction)


        ETH = 0.0025
        amount = self.web3.toWei(ETH, "ether")
        signed_fund_txn = self.web3.eth.account.signTransaction(dict(
            nonce=self.web3.eth.getTransactionCount(self.address, 'pending'),
            gasPrice=self.web3.eth.gasPrice,
            gas=100000,
            to=voter_address,
            value=amount,
            data=b'',
        ), self.private_key)
        fund_tx_hash = self.web3.eth.sendRawTransaction(signed_fund_txn.rawTransaction)

        add_voter_receipt = self.web3.eth.waitForTransactionReceipt(add_voter_tx_hash, timeout=240)
        fund_tx_receipt = self.web3.eth.waitForTransactionReceipt(fund_tx_hash, timeout=240)

        return add_voter_tx_hash.hex()

    def vote(self, ballot_address, voted_index, voter_address, voter_private_key, voter_password):
        """
        Cast vote with the address and private key provided
        Return transaction hash
        :param ballot_address:
        :param voting_index:
        :param voter_address:
        :param voter_password:
        :return:
        """
        ballot = self.web3.eth.contract(address=ballot_address, abi=self.abi)

        vote_tx = ballot.functions.vote(voted_index).buildTransaction(
            {'from': voter_address, 'nonce': self.web3.eth.getTransactionCount(voter_address, 'pending')})
        signed_vote_tx = self.web3.eth.account.signTransaction(vote_tx, private_key=voter_private_key)
        vote_tx_hash = self.web3.eth.sendRawTransaction(signed_vote_tx.rawTransaction)
        vote_tx_receipt = self.web3.eth.waitForTransactionReceipt(vote_tx_hash, timeout=240)

        return vote_tx_hash.hex()

    def get_ballot_info(self, ballot_address):
        """
        Get the information about ballot at specified address
        Return ballot's information in dictionary format
        :param ballot_address:
        :return:
        """
        ballot = self.web3.eth.contract(address=ballot_address, abi=self.abi)

        ballot_info_dict = {
            'ballot_name': ballot.functions.getBallotName().call(),
            'ballot_finalized': ballot.functions.getOptionsFinalized().call(),
            'ballot_max_vote': ballot.functions.getMaxVoteAllowed().call(),
            'ballot_registered_voter_count': ballot.functions.getRegisteredVoterCount().call(),
            'ballot_options_range': range(ballot.functions.getVotingOptionsLength().call()),
            'ballot_options_length': ballot.functions.getVotingOptionsLength().call(),
            'ballot_end_time': ballot.functions.getBallotEndTime().call(),
            'ballot_options_name': [],
            'ballot_options_vote_count': []
        }

        for i in range(0, ballot_info_dict['ballot_options_length']):
            ballot_info_dict['ballot_options_name'].append(ballot.functions.getVotingOptionsName(i).call())
            ballot_info_dict['ballot_options_vote_count'].append(ballot.functions.getVotingOptionsVoteCount(i).call())
        print(ballot_info_dict)
        return ballot_info_dict

    def get_user_info(self, ballot_address, voter_address):
        ballot = self.web3.eth.contract(address=ballot_address, abi=self.abi)
        voter_data = ballot.functions.voters(voter_address).call()
        voter_info_dict = {
            'voter_eligible_to_vote': voter_data[0],
            'voter_cast_vote': voter_data[1],
            'voter_voted_index': ballot.functions.getVoterVotedFor(voter_address).call()
        }
        print(voter_info_dict)
        return voter_info_dict

    def create_account(self, password):
        """
        Create an ethereum account.
        Return keystore encrypted with the password provided
        :param password:
        :return:
        """
        acc = self.web3.eth.account.create(password)
        print(acc.address)
        print(acc.privateKey)
        return acc.address, acc.privateKey.hex()
