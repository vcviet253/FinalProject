pragma solidity >=0.4.22 <0.7.0;


contract VoteBallot {

    //State variables define information of a ballot
    address owner;
    string ballotName;
    uint registeredVoterCount;
    uint ballotEndTime; //second from 1970-01-01
    bool optionsFinalized; //Can still add more options
    uint maxVoteAllowed; //Number of votes allowed for each voter

    //Modifier to only allow owner to call function
    modifier onlyOwner {
        require (msg.sender == owner);
        _;
    }

    //Contract constructor
    constructor (string memory _ballotName, uint _ballotEndTime, uint _maxVoteAllowed) public {
        require(now < _ballotEndTime);
        require(_maxVoteAllowed >= 1);

        owner = msg.sender;  //set owner to the creator (address creating) of Contract
        ballotName = _ballotName; //Set title of ballot
        registeredVoterCount = 0; //Initialize voter count
        ballotEndTime = _ballotEndTime; //set end date of ballot
        optionsFinalized = false;
        maxVoteAllowed = _maxVoteAllowed;
    }


    //Structure defines a single voter
    struct Voter {
        bool allowedToVote; //This user is allowed to vote or not
        bool voted;
        uint[] votedFor; //Index of 'Voting Option' this voter voted for
    }

    //Structure for a single voting option
    struct VotingOption {
        string name;
        uint voteCount;
    }

    //A dynamically-sized array of `VotingOption` structs contains all options available
    VotingOption[] public votingOptions;

    //State variable stores a `Voter` struct for each possible address.
    mapping (address => Voter) public voters;


    //Add a single voting option
    function addVotingOption(string memory _votingOptionName) public onlyOwner {
        require (now < ballotEndTime);
        require(optionsFinalized == false);

        votingOptions.push(VotingOption({
            name: _votingOptionName,
            voteCount: 0
        }));
    }

    //Finalize options, no option can be added after performing this action
    function finalizeVotingOptions() public onlyOwner {
        require(now < ballotEndTime);
        require(votingOptions.length > 1);

        optionsFinalized = true;
    }

    //Register a voter to this ballot, allow him/her to vote, increase amount of registered voters
    function giveRightToVote (address _voter) public onlyOwner {
        require (now < ballotEndTime);
        require(voters[_voter].allowedToVote == false);
        voters[_voter].allowedToVote = true;

        registeredVoterCount += 1;  //Increment registered voters
    }

    //A voter cast his/her vote. Increase counter of options appropriately to reflect voter's choice
    function vote(uint[] memory _votingOptionIndexes) public {
        require (now < ballotEndTime);

        require (optionsFinalized == true);

        Voter storage voter = voters[msg.sender]; //Get the voter for this sender

        require (voter.allowedToVote); //Voter must be allowed to vote by owner
        require(voter.voted == false);
        require (_votingOptionIndexes.length >=1);
        require (_votingOptionIndexes.length <= maxVoteAllowed); //The number of votes casted must be within allowed range


        voter.voted = true;
        for (uint i = 0; i < _votingOptionIndexes.length; i++) {
            voter.votedFor.push(_votingOptionIndexes[i]);
            votingOptions[_votingOptionIndexes[i]].voteCount += 1;
        }


    }


    ---------------- GETTER FUNCTIONS ----------------
    //Get ballot name
    function getBallotName() public view returns (string memory) {
        return ballotName;
    }

    //Get the number of voting options
    function getVotingOptionsLength() public view returns (uint) {
        return votingOptions.length;
    }

    //Get the count of registered voter addresses
    function getRegisteredVoterCount() public view returns (uint) {
        return registeredVoterCount;
    }

    //Get the name of voting option at specific index. Throw if index out of bound
    function getVotingOptionsName(uint _index) public view returns (string memory) {
        return votingOptions[_index].name;
    }

    //Get the number of votes for a an voting at specific index. Throw if index out of bound
    function getVotingOptionsVoteCount(uint _index) public view returns (uint) {
        return votingOptions[_index].voteCount;
    }

    //Get the state of options finalization.
    function getOptionsFinalized() public view returns (bool) {
        return optionsFinalized;
    }

    //Get ballot end time
    function getBallotEndTime() public view returns (uint) {
        return ballotEndTime;
    }

    //Get the number of maximum votes allowed for each voter
    function getMaxVoteAllowed() public view returns (uint) {
        return maxVoteAllowed;
    }

    //Get the list of options that a voter voted for
    function getVoterVotedFor(address _voter) public view returns (uint[] memory) {
        return voters[_voter].votedFor;
    }
}