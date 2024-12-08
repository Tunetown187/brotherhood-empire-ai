// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

contract SecureVault is ReentrancyGuard, AccessControl, Pausable {
    bytes32 public constant DEPOSITOR_ROLE = keccak256("DEPOSITOR_ROLE");
    bytes32 public constant WITHDRAWER_ROLE = keccak256("WITHDRAWER_ROLE");
    
    // Events
    event ProfitSecured(address token, uint256 amount, uint256 timestamp);
    event WithdrawalExecuted(address token, uint256 amount, address recipient);
    event StrategyUpdated(address strategy, bool approved);
    
    // Mappings
    mapping(address => uint256) public balances;
    mapping(address => bool) public approvedTokens;
    mapping(address => bool) public approvedStrategies;
    
    // Security settings
    uint256 public withdrawalDelay = 24 hours;
    uint256 public maxWithdrawalAmount;
    mapping(bytes32 => WithdrawalRequest) public pendingWithdrawals;
    
    struct WithdrawalRequest {
        address token;
        uint256 amount;
        address recipient;
        uint256 timestamp;
        bool executed;
    }
    
    constructor() {
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _setupRole(DEPOSITOR_ROLE, msg.sender);
        _setupRole(WITHDRAWER_ROLE, msg.sender);
    }
    
    // Modifiers
    modifier onlyApprovedToken(address token) {
        require(approvedTokens[token], "Token not approved");
        _;
    }
    
    modifier onlyApprovedStrategy {
        require(approvedStrategies[msg.sender], "Strategy not approved");
        _;
    }
    
    // Management functions
    function setApprovedToken(address token, bool approved) 
        external 
        onlyRole(DEFAULT_ADMIN_ROLE) 
    {
        approvedTokens[token] = approved;
    }
    
    function setApprovedStrategy(address strategy, bool approved) 
        external 
        onlyRole(DEFAULT_ADMIN_ROLE) 
    {
        approvedStrategies[strategy] = approved;
        emit StrategyUpdated(strategy, approved);
    }
    
    function setWithdrawalDelay(uint256 delay) 
        external 
        onlyRole(DEFAULT_ADMIN_ROLE) 
    {
        withdrawalDelay = delay;
    }
    
    function setMaxWithdrawalAmount(uint256 amount) 
        external 
        onlyRole(DEFAULT_ADMIN_ROLE) 
    {
        maxWithdrawalAmount = amount;
    }
    
    // Main functions
    function secureProfits(
        address token,
        uint256 amount
    ) 
        external 
        nonReentrant 
        whenNotPaused
        onlyRole(DEPOSITOR_ROLE)
        onlyApprovedToken(token)
        onlyApprovedStrategy
    {
        require(amount > 0, "Amount must be greater than 0");
        
        // Transfer tokens to vault
        IERC20(token).transferFrom(msg.sender, address(this), amount);
        
        // Update balance
        balances[token] += amount;
        
        emit ProfitSecured(token, amount, block.timestamp);
    }
    
    function requestWithdrawal(
        address token,
        uint256 amount,
        address recipient
    ) 
        external 
        nonReentrant 
        whenNotPaused
        onlyRole(WITHDRAWER_ROLE)
        onlyApprovedToken(token)
        returns (bytes32)
    {
        require(amount <= balances[token], "Insufficient balance");
        require(amount <= maxWithdrawalAmount, "Amount exceeds maximum");
        require(recipient != address(0), "Invalid recipient");
        
        // Create withdrawal request
        bytes32 requestId = keccak256(
            abi.encodePacked(
                token,
                amount,
                recipient,
                block.timestamp
            )
        );
        
        pendingWithdrawals[requestId] = WithdrawalRequest({
            token: token,
            amount: amount,
            recipient: recipient,
            timestamp: block.timestamp,
            executed: false
        });
        
        return requestId;
    }
    
    function executeWithdrawal(bytes32 requestId) 
        external 
        nonReentrant 
        whenNotPaused
        onlyRole(WITHDRAWER_ROLE)
    {
        WithdrawalRequest storage request = pendingWithdrawals[requestId];
        
        require(!request.executed, "Withdrawal already executed");
        require(
            block.timestamp >= request.timestamp + withdrawalDelay,
            "Withdrawal delay not met"
        );
        
        // Mark as executed
        request.executed = true;
        
        // Update balance
        balances[request.token] -= request.amount;
        
        // Transfer tokens
        IERC20(request.token).transfer(request.recipient, request.amount);
        
        emit WithdrawalExecuted(
            request.token,
            request.amount,
            request.recipient
        );
    }
    
    // View functions
    function getBalance(address token) 
        external 
        view 
        returns (uint256) 
    {
        return balances[token];
    }
    
    function getWithdrawalRequest(bytes32 requestId)
        external
        view
        returns (
            address token,
            uint256 amount,
            address recipient,
            uint256 timestamp,
            bool executed
        )
    {
        WithdrawalRequest storage request = pendingWithdrawals[requestId];
        return (
            request.token,
            request.amount,
            request.recipient,
            request.timestamp,
            request.executed
        );
    }
    
    // Emergency functions
    function pause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _pause();
    }
    
    function unpause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _unpause();
    }
    
    function emergencyWithdraw(
        address token,
        address recipient
    ) 
        external 
        onlyRole(DEFAULT_ADMIN_ROLE) 
    {
        uint256 balance = IERC20(token).balanceOf(address(this));
        IERC20(token).transfer(recipient, balance);
        balances[token] = 0;
    }
    
    // Receive function
    receive() external payable {
        revert("Direct deposits not allowed");
    }
