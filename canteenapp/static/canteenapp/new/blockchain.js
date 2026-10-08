var contract;
ethereum.enable();
var address="0x9bAf4b18DE37809cf20BED2C082638C2D07e8774";
var gasPriceval="3";
var gasval="300";
$(document).ready(function(){
	
	web3=new Web3(web3.currentProvider);
	//var address="0x64ADd870Fb9d6DbdA79504a7458CaDDF6CfE74da";
	var abi=[
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "string",
				"name": "access",
				"type": "string"
			}
		],
		"name": "checkAccess",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "bool",
				"name": "returnValue",
				"type": "bool"
			}
		],
		"name": "checkRegistry",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "string",
				"name": "data",
				"type": "string"
			}
		],
		"name": "getRecord",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "int256",
				"name": "uType",
				"type": "int256"
			}
		],
		"name": "userType",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "user",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "password",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "typeofuser",
				"type": "string"
			}
		],
		"name": "Login",
		"outputs": [
			{
				"components": [
					{
						"internalType": "address",
						"name": "key",
						"type": "address"
					},
					{
						"internalType": "string",
						"name": "name",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "email",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "phone",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "password",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "typeofuser",
						"type": "string"
					}
				],
				"internalType": "struct Etendorsblockchain.userinfo[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "user",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "username",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "sectorname",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "price",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "address1",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "enddate",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "description",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "filename",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "privatekey",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "encryptedkey",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "ipfsfolderhash",
				"type": "string"
			}
		],
		"name": "addtendorinfo",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "allbookingdetail",
		"outputs": [
			{
				"internalType": "address",
				"name": "key",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "receiver",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "status",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "file",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "data1",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "allpayments",
		"outputs": [
			{
				"internalType": "address",
				"name": "key",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "card",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "file",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "admin",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "receiver",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "allsendrequestdata",
		"outputs": [
			{
				"internalType": "address",
				"name": "key",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "data1",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "file1",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "receiver1",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "fileupload",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "alltendorinformation",
		"outputs": [
			{
				"internalType": "address",
				"name": "key",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "username",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "sectorname",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "price",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "address1",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "enddate",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "description",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "filename",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "privatekey",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "encryptedkey",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "ipfsfolderhash",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "allusers",
		"outputs": [
			{
				"internalType": "address",
				"name": "key",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "email",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "phone",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "password",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "typeofuser",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "user",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "receiver",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "status",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "file",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "data1",
				"type": "string"
			}
		],
		"name": "bookingdetails1",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "user",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "username",
				"type": "string"
			}
		],
		"name": "getaddtendorinfo",
		"outputs": [
			{
				"components": [
					{
						"internalType": "address",
						"name": "key",
						"type": "address"
					},
					{
						"internalType": "string",
						"name": "username",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "sectorname",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "price",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "address1",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "enddate",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "description",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "filename",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "privatekey",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "encryptedkey",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "ipfsfolderhash",
						"type": "string"
					}
				],
				"internalType": "struct Etendorsblockchain.addtender[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "user",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "status",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "receiver",
				"type": "string"
			}
		],
		"name": "getbookingdetails1",
		"outputs": [
			{
				"components": [
					{
						"internalType": "address",
						"name": "key",
						"type": "address"
					},
					{
						"internalType": "string",
						"name": "receiver",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "status",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "file",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "data1",
						"type": "string"
					}
				],
				"internalType": "struct Etendorsblockchain.bookingdetail[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "user",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "admin",
				"type": "string"
			}
		],
		"name": "getdatapayment",
		"outputs": [
			{
				"components": [
					{
						"internalType": "address",
						"name": "key",
						"type": "address"
					},
					{
						"internalType": "string",
						"name": "card",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "file",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "admin",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "receiver",
						"type": "string"
					}
				],
				"internalType": "struct Etendorsblockchain.pay[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "user",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "receiver1",
				"type": "string"
			}
		],
		"name": "getsendrequest",
		"outputs": [
			{
				"components": [
					{
						"internalType": "address",
						"name": "key",
						"type": "address"
					},
					{
						"internalType": "string",
						"name": "data1",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "file1",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "receiver1",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "fileupload",
						"type": "string"
					}
				],
				"internalType": "struct Etendorsblockchain.send[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "user",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "card",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "file",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "admin",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "receiver",
				"type": "string"
			}
		],
		"name": "payment",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "user",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "data1",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "file1",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "receiver1",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "fileupload",
				"type": "string"
			}
		],
		"name": "sendrequest",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "user",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "email",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "phone",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "password",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "typeofuser",
				"type": "string"
			}
		],
		"name": "userRegister",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
];
	contract=new web3.eth.Contract(abi,address);
})
