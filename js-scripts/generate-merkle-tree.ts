import { MerkleTree } from "merkletreejs";
import { keccak256 } from "viem";

const leaves = [
    '0x65f0dd0822cd1ebda33afda8b3119741a09bb1869414d18fcca2d2e6674e8959', 
    '0x94a83c247e8e2d40e8137a4d4357cd0b146d0a38561896cfa70f97f521e99199',
];

const tree = new MerkleTree(leaves.sort(), keccak256, {
    sortPairs: true
});

const root = tree.getRoot().toString('hex');
console.log("Root:", root);

let proof = tree.getProof(leaves[0]);
console.log("Proof 1:", proof[0].data.toString('hex'));

proof = tree.getProof(leaves[1]);
console.log("Proof 2:", proof[0].data.toString('hex'));

console.log(tree.verify(proof, leaves[1], root));



// const { MerkleTree } = require('merkletreejs')
// const SHA256 = require('crypto-js/sha256')

// const leaves = ['a', 'b', 'c'].map(x => SHA256(x))
// const tree = new MerkleTree(leaves, SHA256)
// const root = tree.getRoot().toString('hex')
// const leaf = SHA256('a')
// const proof = tree.getProof(leaf)
// console.log(tree.verify(proof, leaf, root)) // true


// const badLeaves = ['a', 'x', 'c'].map(x => SHA256(x))
// const badTree = new MerkleTree(badLeaves, SHA256)
// const badLeaf = SHA256('x')
// const badProof = badTree.getProof(badLeaf)
// console.log(badTree.verify(badProof, badLeaf, root)) // false
