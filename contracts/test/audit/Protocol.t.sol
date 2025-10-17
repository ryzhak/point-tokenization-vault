// SPDX-License-Identifier: AGPL-3.0-only
pragma solidity =0.8.24;

import {ERC1967Proxy} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";
import {Test, console2} from "forge-std/Test.sol";
import {MockERC20, ERC20} from "solmate/test/utils/mocks/MockERC20.sol";
import {PointTokenVault} from "../../PointTokenVault.sol";

contract ProtocolTest is Test {
    PointTokenVault pointTokenVaultImplementation;
    ERC1967Proxy proxy;
    PointTokenVault pointTokenVault;

    MockERC20 usdtToken;

    address admin = makeAddr("admin");
    address feeCollector = makeAddr("feeCollector");
    address user = makeAddr("user");
    address user2 = makeAddr("user2");

    function setUp() public {
        pointTokenVaultImplementation = new PointTokenVault();
        bytes memory initData = abi.encodeWithSignature("initialize(address,address)", admin, feeCollector);
        proxy = new ERC1967Proxy(address(pointTokenVaultImplementation), initData);
        pointTokenVault = PointTokenVault(payable(address(proxy)));

        usdtToken = new MockERC20("USDT", "USDT", 18);
        usdtToken.mint(user, 100 ether);

        vm.prank(user);
        usdtToken.approve(address(pointTokenVault), type(uint256).max);

        vm.startPrank(admin);
        pointTokenVault.grantRole(pointTokenVault.OPERATOR_ROLE(), admin);
        pointTokenVault.setCap(address(usdtToken), type(uint256).max);
        vm.stopPrank();
    }

    function testPointTokenVault() public {
        // // deposit
        // vm.prank(user);
        // pointTokenVault.deposit(usdtToken, 100 ether, user);

        // // withdraw
        // vm.prank(user);
        // pointTokenVault.withdraw(usdtToken, 100 ether, user);

        // debugBalance(address(usdtToken), user, "User balance USDT");
        // debugBalance(address(usdtToken), user2, "User2 balance USDT");
        // debugBalance(address(usdtToken), address(pointTokenVault), "PointTokenVault balance USDT");
    }

    function debugBalance(address token, address target, string memory label) public {
        console2.log(label, ":", ERC20(token).balanceOf(target));
    }
}
