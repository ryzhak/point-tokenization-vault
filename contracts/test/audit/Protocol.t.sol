// SPDX-License-Identifier: AGPL-3.0-only
pragma solidity =0.8.24;

import {ERC1967Proxy} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";
import {Test, console, console2} from "forge-std/Test.sol";
import {MockERC20, ERC20} from "solmate/test/utils/mocks/MockERC20.sol";
import {PToken} from "../../PToken.sol";
import {PointTokenVault} from "../../PointTokenVault.sol";

contract ProtocolTest is Test {
    PointTokenVault pointTokenVaultImplementation;
    ERC1967Proxy proxy;
    PointTokenVault pointTokenVault;

    MockERC20 usdtToken;
    MockERC20 rewardToken;

    address admin = makeAddr("admin");
    address feeCollector = makeAddr("feeCollector");
    address user = makeAddr("user");
    address user2 = makeAddr("user2");
    address user3 = makeAddr("user3");

    function setUp() public {
        pointTokenVaultImplementation = new PointTokenVault();
        bytes memory initData = abi.encodeWithSignature("initialize(address,address)", admin, feeCollector);
        proxy = new ERC1967Proxy(address(pointTokenVaultImplementation), initData);
        pointTokenVault = PointTokenVault(payable(address(proxy)));

        usdtToken = new MockERC20("USDT", "USDT", 18);
        usdtToken.mint(user, 100 ether);

        rewardToken = new MockERC20("RWD", "RWD", 18);
        rewardToken.mint(address(pointTokenVault), 100 ether);

        vm.startPrank(user);
        usdtToken.approve(address(pointTokenVault), type(uint256).max);
        rewardToken.approve(address(pointTokenVault), type(uint256).max);
        vm.stopPrank();

        vm.startPrank(admin);
        pointTokenVault.grantRole(pointTokenVault.OPERATOR_ROLE(), admin);
        pointTokenVault.grantRole(pointTokenVault.MERKLE_UPDATER_ROLE(), admin);
        pointTokenVault.setCap(address(usdtToken), type(uint256).max);
        pointTokenVault.setMintFee(0.1e18); // 10%
        pointTokenVault.setRedemptionFee(0.1e18); // 10%
        pointTokenVault.setFeeCollector(feeCollector);
        vm.stopPrank();
    }

    function testPointTokenVault() public {
        // deployPToken
        bytes32 pTokenId = keccak256("pointsId1");
        PToken pToken = pointTokenVault.deployPToken(pTokenId);

        // // deposit
        // vm.prank(user);
        // pointTokenVault.deposit(usdtToken, 100 ether, user);

        // // withdraw
        // vm.prank(user);
        // pointTokenVault.withdraw(usdtToken, 100 ether, user);

        // updateRoot
        vm.prank(admin);
        pointTokenVault.updateRoot(0xf179ddb3a69a62bf3075bcb38cfcbd5631df52d64c7fca7a5b86362e46191512);

        // claimPTokens
        address[] memory accounts = new address[](2);
        accounts[0] = user;
        accounts[1] = user2;
        uint256[] memory totalClaimable = new uint256[](2);
        totalClaimable[0] = 5 ether;
        totalClaimable[1] = 10 ether;     
        bytes32[] memory leafs = getMerkleLeafs(pTokenId, accounts, totalClaimable);

        bytes32[] memory proof = new bytes32[](1);
        proof[0] = 0x94a83c247e8e2d40e8137a4d4357cd0b146d0a38561896cfa70f97f521e99199;
        PointTokenVault.Claim memory claim = PointTokenVault.Claim({
            pointsId: pTokenId,
            totalClaimable: 5 ether,
            amountToClaim: 5 ether,
            proof: proof
        });
        vm.prank(user);
        pointTokenVault.claimPTokens(claim, user, user);

        proof[0] = 0x65f0dd0822cd1ebda33afda8b3119741a09bb1869414d18fcca2d2e6674e8959;
        claim = PointTokenVault.Claim({
            pointsId: pTokenId,
            totalClaimable: 10 ether,
            amountToClaim: 10 ether,
            proof: proof
        });
        vm.prank(user2);
        pointTokenVault.claimPTokens(claim, user2, user2);

        // setRedemption
        vm.prank(admin);
        pointTokenVault.setRedemption(pTokenId, rewardToken, 1 ether, false);

        // // redeemRewards
        // proof[0] = "";
        // claim = PointTokenVault.Claim({
        //     pointsId: pTokenId,
        //     totalClaimable: 4.5 ether,
        //     amountToClaim: 4.5 ether,
        //     proof: proof
        // });
        // vm.prank(user);
        // pointTokenVault.redeemRewards(claim, user);

        // // redeemRewards (with fee)
        // deal(address(pToken), user3, 10 ether);
        // proof[0] = "";
        // claim = PointTokenVault.Claim({
        //     pointsId: pTokenId,
        //     totalClaimable: 10 ether,
        //     amountToClaim: 10 ether,
        //     proof: proof
        // });
        // vm.prank(user3);
        // pointTokenVault.redeemRewards(claim, user3);

        // // convertRewardsToPTokens
        // rewardToken.mint(user, 10 ether);
        // vm.prank(user);
        // pointTokenVault.convertRewardsToPTokens(user, pTokenId, 10 ether);

        // // collectFees
        // pointTokenVault.collectFees(pTokenId);

        // debugBalance(address(pToken), user, "PToken balance (user)");
        // debugBalance(address(pToken), user2, "PToken balance (user2)");
    }

    function debugBalance(address token, address target, string memory label) public {
        console2.log(label, ":", ERC20(token).balanceOf(target));
    }

    function getMerkleLeafs(bytes32 pointsId, address[] memory accounts, uint256[] memory totalClaimable) public returns (bytes32[] memory) {
        bytes32[] memory leafs = new bytes32[](accounts.length);
        for (uint256 i = 0; i < accounts.length; i++) {
            leafs[i] = keccak256(abi.encodePacked(accounts[i], pointsId, totalClaimable[i]));
        }
        return leafs;
    }
}
