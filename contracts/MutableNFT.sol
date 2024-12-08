// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract MutableNFT is ERC721, ReentrancyGuard, Pausable, AccessControl {
    using Counters for Counters.Counter;
    
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant UPDATER_ROLE = keccak256("UPDATER_ROLE");
    
    Counters.Counter private _tokenIds;
    
    // Mapping for token URIs
    mapping(uint256 => string) private _tokenURIs;
    
    // Mapping for token metadata
    mapping(uint256 => bytes) private _tokenMetadata;
    
    // Anti-sniping protection
    uint256 public constant MINT_DELAY = 5 minutes;
    mapping(address => uint256) public lastMintTime;
    
    // Rate limiting
    uint256 public constant MAX_MINTS_PER_PERIOD = 5;
    uint256 public constant MINT_PERIOD = 1 hours;
    mapping(address => uint256) public mintsInPeriod;
    mapping(address => uint256) public periodStart;
    
    // Events
    event MetadataUpdated(uint256 indexed tokenId, bytes newMetadata);
    event URIUpdated(uint256 indexed tokenId, string newUri);
    
    constructor(string memory name, string memory symbol) 
        ERC721(name, symbol) 
    {
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _setupRole(MINTER_ROLE, msg.sender);
        _setupRole(UPDATER_ROLE, msg.sender);
    }
    
    // Anti-sniping modifier
    modifier antiSnipe() {
        require(
            block.timestamp >= lastMintTime[msg.sender] + MINT_DELAY,
            "Must wait between mints"
        );
        _;
    }
    
    // Rate limiting modifier
    modifier rateLimit() {
        if (block.timestamp >= periodStart[msg.sender] + MINT_PERIOD) {
            periodStart[msg.sender] = block.timestamp;
            mintsInPeriod[msg.sender] = 0;
        }
        require(
            mintsInPeriod[msg.sender] < MAX_MINTS_PER_PERIOD,
            "Exceeded max mints for this period"
        );
        _;
        mintsInPeriod[msg.sender]++;
    }
    
    function mint(address to, string memory uri, bytes memory metadata) 
        public 
        nonReentrant 
        antiSnipe
        rateLimit
        whenNotPaused
        onlyRole(MINTER_ROLE) 
        returns (uint256)
    {
        _tokenIds.increment();
        uint256 newTokenId = _tokenIds.current();
        
        _safeMint(to, newTokenId);
        _setTokenURI(newTokenId, uri);
        _setTokenMetadata(newTokenId, metadata);
        
        lastMintTime[msg.sender] = block.timestamp;
        
        return newTokenId;
    }
    
    function updateMetadata(uint256 tokenId, bytes memory newMetadata)
        public
        nonReentrant
        whenNotPaused
        onlyRole(UPDATER_ROLE)
    {
        require(_exists(tokenId), "Token does not exist");
        _setTokenMetadata(tokenId, newMetadata);
        emit MetadataUpdated(tokenId, newMetadata);
    }
    
    function updateURI(uint256 tokenId, string memory newUri)
        public
        nonReentrant
        whenNotPaused
        onlyRole(UPDATER_ROLE)
    {
        require(_exists(tokenId), "Token does not exist");
        _setTokenURI(tokenId, newUri);
        emit URIUpdated(tokenId, newUri);
    }
    
    function _setTokenURI(uint256 tokenId, string memory uri) internal {
        require(_exists(tokenId), "URI set for nonexistent token");
        _tokenURIs[tokenId] = uri;
    }
    
    function _setTokenMetadata(uint256 tokenId, bytes memory metadata) internal {
        require(_exists(tokenId), "Metadata set for nonexistent token");
        _tokenMetadata[tokenId] = metadata;
    }
    
    function tokenURI(uint256 tokenId) 
        public 
        view 
        virtual 
        override 
        returns (string memory) 
    {
        require(_exists(tokenId), "URI query for nonexistent token");
        return _tokenURIs[tokenId];
    }
    
    function getTokenMetadata(uint256 tokenId) 
        public 
        view 
        returns (bytes memory) 
    {
        require(_exists(tokenId), "Metadata query for nonexistent token");
        return _tokenMetadata[tokenId];
    }
    
    // Emergency functions
    function pause() public onlyRole(DEFAULT_ADMIN_ROLE) {
        _pause();
    }
    
    function unpause() public onlyRole(DEFAULT_ADMIN_ROLE) {
        _unpause();
    }
    
    // Required overrides
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, AccessControl)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
