using PointTokenVault as pointTokenVault;
using PToken as pToken;

methods {
    // PToken
    function _.PAUSE_ROLE() external => DISPATCHER(true);
    function _.approve(address, uint256) external => DISPATCHER(true);
    function _.balanceOf(address) external => DISPATCHER(true);
    function _.burn(address, uint256) external => DISPATCHER(true);
    function _.decimals() external => DISPATCHER(true);
    function _.mint(address, uint256) external => DISPATCHER(true);
    function _.pause() external => DISPATCHER(true);
    function _.renounceRole(bytes32, address) external => DISPATCHER(true);
    function _.totalSupply() external => DISPATCHER(true);
    function _.transfer(address, uint256) external => DISPATCHER(true);
    function _.transferFrom(address, address, uint256) external => DISPATCHER(true);
    function _.unpause() external => DISPATCHER(true);
}

//===========
// Unit
//===========

// `updateRoot()` updates storage as expected
rule unit_updateRoot_integrity() {
    env e;

    bytes32 newRoot;
    bytes32 currentRoot = pointTokenVault.currRoot;

    updateRoot(e, newRoot);

    assert pointTokenVault.currRoot == newRoot;
    assert pointTokenVault.prevRoot == currentRoot;
}

// `updateRoot()` reverts when expected
rule unit_updateRoot_revertConditions() {
    env e;

    bytes32 newRoot;

    bool isEtherSent = e.msg.value > 0;
    bool hasMerkleUpdaterRole = hasRole(e, MERKLE_UPDATER_ROLE(e), e.msg.sender);

    bool isExpectedToRevert = 
        isEtherSent ||
        !hasMerkleUpdaterRole;

    updateRoot@withrevert(e, newRoot);

    assert lastReverted <=> isExpectedToRevert;
}

// `setCap()` updates storage as expected
rule unit_setCap_integrity() {
    env e;

    address token;
    uint256 cap;

    setCap(e, token, cap);

    assert caps(e, token) == cap;
}

// `setCap()` reverts when expected
rule unit_setCap_revertConditions() {
    env e;

    address token;
    uint256 cap;

    bool isEtherSent = e.msg.value > 0;
    bool hasOperatorRole = hasRole(e, OPERATOR_ROLE(e), e.msg.sender);

    bool isExpectedToRevert = 
        isEtherSent ||
        !hasOperatorRole;

    setCap@withrevert(e, token, cap);

    assert lastReverted <=> isExpectedToRevert;
}

// `setRedemption()` updates storage as expected
rule unit_setRedemption_integrity() {
    env e;

    bytes32 pointsId;
    address rewardToken;
    uint256 rewardsPerPToken;
    bool isMerkleBased;

    setRedemption(e, pointsId, rewardToken, rewardsPerPToken, isMerkleBased);

    address newRewardToken;
    uint256 newRewardsPerPToken;
    bool newIsMerkleBased;

    newRewardToken, newRewardsPerPToken, newIsMerkleBased = redemptions(e, pointsId);

    assert newRewardToken == rewardToken;
    assert newRewardsPerPToken == rewardsPerPToken;
    assert newIsMerkleBased == isMerkleBased;
}

// `setRedemption()` reverts when expected
rule unit_setRedemption_revertConditions() {
    env e;

    bytes32 pointsId;
    address rewardToken;
    uint256 rewardsPerPToken;
    bool isMerkleBased;

    bool isEtherSent = e.msg.value > 0;
    bool hasOperatorRole = hasRole(e, OPERATOR_ROLE(e), e.msg.sender);

    bool isExpectedToRevert = 
        isEtherSent ||
        !hasOperatorRole;

    setRedemption@withrevert(e, pointsId, rewardToken, rewardsPerPToken, isMerkleBased);

    assert lastReverted <=> isExpectedToRevert;
}

// `setMintFee()` updates storage as expected
rule unit_setMintFee_integrity() {
    env e;

    uint256 mintFee;

    setMintFee(e, mintFee);

    assert mintFee(e) == mintFee;
}

// `setMintFee()` reverts when expected
rule unit_setMintFee_revertConditions() {
    env e;

    uint256 mintFee;

    bool isEtherSent = e.msg.value > 0;
    bool hasOperatorRole = hasRole(e, OPERATOR_ROLE(e), e.msg.sender);

    bool isExpectedToRevert = 
        isEtherSent ||
        !hasOperatorRole;

    setMintFee@withrevert(e, mintFee);

    assert lastReverted <=> isExpectedToRevert;
}

// `setRedemptionFee()` updates storage as expected
rule unit_setRedemptionFee_integrity() {
    env e;

    uint256 redemptionFee;

    setRedemptionFee(e, redemptionFee);

    assert redemptionFee(e) == redemptionFee;
}

// `setRedemptionFee()` reverts when expected
rule unit_setRedemptionFee_revertConditions() {
    env e;

    uint256 redemptionFee;

    bool isEtherSent = e.msg.value > 0;
    bool hasOperatorRole = hasRole(e, OPERATOR_ROLE(e), e.msg.sender);

    bool isExpectedToRevert = 
        isEtherSent ||
        !hasOperatorRole;

    setRedemptionFee@withrevert(e, redemptionFee);

    assert lastReverted <=> isExpectedToRevert;
}

// `pausePToken()` updates storage as expected
rule unit_pausePToken_integrity() {
    env e;

    bytes32 pointsId;

    pausePToken(e, pointsId);

    assert pointTokenVault.pTokens[pointsId].paused(e);
}

// `pausePToken()` reverts when expected
rule unit_pausePToken_revertConditions() {
    env e;

    bytes32 pointsId;

    address currentPToken = pointTokenVault.pTokens[pointsId];

    bool isEtherSent = e.msg.value > 0;
    bool hasOperatorRole = hasRole(e, OPERATOR_ROLE(e), e.msg.sender);
    bool isPTokenPaused = currentPToken.paused(e);
    bool hasPointTokenVaultPauseRole = currentPToken.hasRole(e, currentPToken.PAUSE_ROLE(e), currentContract);

    bool isExpectedToRevert = 
        isEtherSent ||
        !hasOperatorRole ||
        isPTokenPaused ||
        !hasPointTokenVaultPauseRole;

    pausePToken@withrevert(e, pointsId);

    assert lastReverted <=> isExpectedToRevert;
}

// `unpausePToken()` updates storage as expected
rule unit_unpausePToken_integrity() {
    env e;

    bytes32 pointsId;

    unpausePToken(e, pointsId);

    assert !pointTokenVault.pTokens[pointsId].paused(e);
}

// `unpausePToken()` reverts when expected
rule unit_unpausePToken_revertConditions() {
    env e;

    bytes32 pointsId;

    address currentPToken = pointTokenVault.pTokens[pointsId];

    bool isEtherSent = e.msg.value > 0;
    bool hasOperatorRole = hasRole(e, OPERATOR_ROLE(e), e.msg.sender);
    bool isPTokenPaused = currentPToken.paused(e);
    bool hasPointTokenVaultPauseRole = currentPToken.hasRole(e, currentPToken.PAUSE_ROLE(e), currentContract);

    bool isExpectedToRevert = 
        isEtherSent ||
        !hasOperatorRole ||
        !isPTokenPaused ||
        !hasPointTokenVaultPauseRole;

    unpausePToken@withrevert(e, pointsId);

    assert lastReverted <=> isExpectedToRevert;
}

// `renouncePauseRole()` updates storage as expected
rule unit_renouncePauseRole_integrity() {
    env e;

    bytes32 pointsId;
    address currentPToken = pointTokenVault.pTokens[pointsId];

    renouncePauseRole(e, pointsId);

    assert !hasRole(e, currentPToken.PAUSE_ROLE(e), currentContract);
}

// `renouncePauseRole()` reverts when expected
rule unit_renouncePauseRole_revertConditions() {
    env e;

    bytes32 pointsId;

    bool isEtherSent = e.msg.value > 0;
    bool hasOperatorRole = hasRole(e, OPERATOR_ROLE(e), e.msg.sender);

    bool isExpectedToRevert = 
        isEtherSent ||
        !hasOperatorRole;

    renouncePauseRole@withrevert(e, pointsId);

    assert lastReverted <=> isExpectedToRevert;
}

// `collectFees()` updates storage as expected
rule unit_collectFees_integrity() {
    env e;

    bytes32 pointsId;

    address currentPToken = pointTokenVault.pTokens[pointsId];
    address rewardToken = pointTokenVault.redemptions[pointsId].rewardToken;

    uint256 pTokenFee = pointTokenVault.pTokenFeeAcc[pointsId];
    uint256 feeCollectorPTokenBalanceBefore = pointTokenVault.pTokens[pointsId].balanceOf(e, pointTokenVault.feeCollector);
    
    uint256 rewardTokenFee = pointTokenVault.rewardTokenFeeAcc[pointsId];
    uint256 feeCollectorRewardTokenBalanceBefore = pointTokenVault.redemptions[pointsId].rewardToken.balanceOf(e, pointTokenVault.feeCollector);

    collectFees(e, pointsId);

    uint256 feeCollectorPTokenBalanceAfter = pointTokenVault.pTokens[pointsId].balanceOf(e, pointTokenVault.feeCollector);
    uint256 feeCollectorRewardTokenBalanceAfter = pointTokenVault.redemptions[pointsId].rewardToken.balanceOf(e, pointTokenVault.feeCollector);

    assert currentPToken == rewardToken => 
        feeCollectorPTokenBalanceAfter == require_uint256(feeCollectorRewardTokenBalanceBefore + pTokenFee + rewardTokenFee);

    assert currentPToken != rewardToken =>
        pointTokenVault.pTokenFeeAcc[pointsId] == 0 &&
        feeCollectorPTokenBalanceAfter == require_uint256(feeCollectorPTokenBalanceBefore + pTokenFee) &&
        feeCollectorRewardTokenBalanceAfter == require_uint256(feeCollectorRewardTokenBalanceBefore + rewardTokenFee);
}

// `collectFees()` reverts when expected
rule unit_collectFees_revertConditions() {
    env e;

    bytes32 pointsId;

    uint256 pTokenFee = pointTokenVault.pTokenFeeAcc[pointsId];
    uint256 rewardTokenFee = pointTokenVault.rewardTokenFeeAcc[pointsId];

    bool isEtherSent = e.msg.value > 0;
    bool isPTokenPaused = pointTokenVault.pTokens[pointsId].paused(e);
    bool hasUncollectedPTokenFee = pTokenFee > 0;
    bool hasEnoughRewardTokens = rewardTokenFee <= pointTokenVault.redemptions[pointsId].rewardToken.balanceOf(e, currentContract);

    bool isExpectedToRevert = 
        isEtherSent ||
        (hasUncollectedPTokenFee && isPTokenPaused) ||
        !hasEnoughRewardTokens;

    collectFees@withrevert(e, pointsId);

    assert lastReverted <=> isExpectedToRevert;
}

// `collectFees()` does not affect other entities
rule unit_collectFees_doesNotAffectOtherEntities() {
    env e;

    address otherUser;
    bytes32 pointsId;

    require otherUser != pointTokenVault.feeCollector && otherUser != currentContract;

    uint256 otherUserPTokenBalanceBefore = pointTokenVault.pTokens[pointsId].balanceOf(e, otherUser);
    uint256 otherUserRewardTokenBalanceBefore = pointTokenVault.redemptions[pointsId].rewardToken.balanceOf(e, otherUser);

    collectFees(e, pointsId);

    uint256 otherUserPTokenBalanceAfter = pointTokenVault.pTokens[pointsId].balanceOf(e, otherUser);
    uint256 otherUserRewardTokenBalanceAfter = pointTokenVault.redemptions[pointsId].rewardToken.balanceOf(e, otherUser);

    assert otherUserPTokenBalanceBefore == otherUserPTokenBalanceAfter;
    assert otherUserRewardTokenBalanceBefore == otherUserRewardTokenBalanceAfter;
}

// `setFeeCollector()` updates storage as expected
rule unit_setFeeCollector_integrity() {
    env e;

    address feeCollector;

    setFeeCollector(e, feeCollector);

    assert feeCollector(e) == feeCollector;
}

// `setFeeCollector()` reverts when expected
rule unit_setFeeCollector_revertConditions() {
    env e;

    address feeCollector;

    bool isEtherSent = e.msg.value > 0;
    bool hasDefaultAdminRole = hasRole(e, DEFAULT_ADMIN_ROLE(e), e.msg.sender);

    bool isExpectedToRevert = 
        isEtherSent ||
        !hasDefaultAdminRole;

    setFeeCollector@withrevert(e, feeCollector);

    assert lastReverted <=> isExpectedToRevert;
}
