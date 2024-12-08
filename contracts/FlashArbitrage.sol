// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@aave/core-v3/contracts/flashloan/base/FlashLoanSimpleReceiverBase.sol";
import "@aave/core-v3/contracts/interfaces/IPoolAddressesProvider.sol";
import "@uniswap/v2-periphery/contracts/interfaces/IUniswapV2Router02.sol";

contract FlashArbitrage is FlashLoanSimpleReceiverBase, Ownable, ReentrancyGuard {
    // Events
    event ArbitrageExecuted(
        address indexed token,
        uint256 amount,
        uint256 profit
    );
    
    event FlashLoanExecuted(
        address indexed token,
        uint256 amount,
        uint256 fee
    );
    
    // Interfaces
    IUniswapV2Router02 public immutable uniswapRouter;
    IUniswapV2Router02 public immutable sushiswapRouter;
    
    // State variables
    mapping(address => bool) public authorizedCallers;
    uint256 public minProfitThreshold;
    
    constructor(
        address _addressProvider,
        address _uniswapRouter,
        address _sushiswapRouter
    ) FlashLoanSimpleReceiverBase(IPoolAddressesProvider(_addressProvider)) {
        uniswapRouter = IUniswapV2Router02(_uniswapRouter);
        sushiswapRouter = IUniswapV2Router02(_sushiswapRouter);
        authorizedCallers[msg.sender] = true;
    }
    
    // Modifiers
    modifier onlyAuthorized() {
        require(
            authorizedCallers[msg.sender],
            "Caller not authorized"
        );
        _;
    }
    
    // Management functions
    function setAuthorizedCaller(address caller, bool authorized) 
        external 
        onlyOwner 
    {
        authorizedCallers[caller] = authorized;
    }
    
    function setMinProfitThreshold(uint256 _threshold) 
        external 
        onlyOwner 
    {
        minProfitThreshold = _threshold;
    }
    
    function withdrawToken(address token, uint256 amount) 
        external 
        onlyOwner 
    {
        IERC20(token).transfer(msg.sender, amount);
    }
    
    // Main arbitrage function
    function executeArbitrage(
        address token,
        uint256 amount,
        bytes calldata params
    ) external onlyAuthorized nonReentrant {
        // Request flash loan
        _requestFlashLoan(token, amount, params);
    }
    
    // Flash loan callback
    function executeOperation(
        address asset,
        uint256 amount,
        uint256 premium,
        address initiator,
        bytes calldata params
    ) external override returns (bool) {
        // Decode arbitrage parameters
        (
            address[] memory path1,
            address[] memory path2,
            uint256 expectedProfit
        ) = abi.decode(params, (address[], address[], uint256));
        
        // Get initial balance
        uint256 initialBalance = IERC20(asset).balanceOf(address(this));
        
        // Execute arbitrage swaps
        _executeArbitrageSwaps(
            asset,
            amount,
            path1,
            path2
        );
        
        // Verify profit
        uint256 finalBalance = IERC20(asset).balanceOf(address(this));
        uint256 profit = finalBalance - initialBalance;
        require(
            profit >= expectedProfit,
            "Insufficient profit"
        );
        
        // Approve repayment
        uint256 amountToRepay = amount + premium;
        IERC20(asset).approve(address(POOL), amountToRepay);
        
        emit ArbitrageExecuted(asset, amount, profit);
        
        return true;
    }
    
    // Internal functions
    function _requestFlashLoan(
        address asset,
        uint256 amount,
        bytes calldata params
    ) internal {
        POOL.flashLoanSimple(
            address(this),
            asset,
            amount,
            params,
            0
        );
    }
    
    function _executeArbitrageSwaps(
        address asset,
        uint256 amount,
        address[] memory path1,
        address[] memory path2
    ) internal {
        // Approve tokens
        IERC20(asset).approve(address(uniswapRouter), amount);
        
        // Execute first swap on Uniswap
        uint256[] memory amounts1 = uniswapRouter.swapExactTokensForTokens(
            amount,
            0, // Accept any amount
            path1,
            address(this),
            block.timestamp
        );
        
        // Approve intermediate token
        IERC20(path1[path1.length - 1]).approve(
            address(sushiswapRouter),
            amounts1[amounts1.length - 1]
        );
        
        // Execute second swap on Sushiswap
        sushiswapRouter.swapExactTokensForTokens(
            amounts1[amounts1.length - 1],
            0, // Accept any amount
            path2,
            address(this),
            block.timestamp
        );
    }
    
    // View functions
    function getArbitrageProfitEstimate(
        address token,
        uint256 amount,
        address[] calldata path1,
        address[] calldata path2
    ) external view returns (uint256) {
        // Simulate swaps and return expected profit
        uint256[] memory amounts1 = uniswapRouter.getAmountsOut(amount, path1);
        uint256[] memory amounts2 = sushiswapRouter.getAmountsOut(
            amounts1[amounts1.length - 1],
            path2
        );
        
        uint256 flashLoanFee = (amount * 9) / 10000; // 0.09% AAVE flash loan fee
        uint256 expectedReturn = amounts2[amounts2.length - 1];
        
        if (expectedReturn <= amount + flashLoanFee) {
            return 0;
        }
        
        return expectedReturn - (amount + flashLoanFee);
    }
    
    // Emergency functions
    function emergencyWithdraw(address token) external onlyOwner {
        uint256 balance = IERC20(token).balanceOf(address(this));
        IERC20(token).transfer(msg.sender, balance);
    }
    
    // Receive function
    receive() external payable {}
