pragma solidity 0.8.10;
// overwrite abi and bin:
// solc StorageLayout.sol --abi --bin --overwrite
contract StorageLayout {
    uint248 packedUint = 1;
    bool packedBool = true;

    struct DynamicStruct {
        uint256[] _values;
        mapping(address => uint256) _indexes;
    }

    struct NestedStruct {
        DynamicStruct nested;
        uint256 a;
        bool b;
        uint16 c;
        uint32 d;
        uint64 e;
    }

    struct PackedStruct {
        bool b;
        uint248 a;
    }

    PackedStruct _packedStruct = PackedStruct(packedBool, packedUint);

    mapping (uint => PackedStruct) mappingPackedStruct;
    mapping (address => mapping (uint => PackedStruct)) deepMappingPackedStruct;
    mapping (address => mapping (uint => bool)) deepMappingElementaryTypes;
    mapping (address => PackedStruct[]) mappingDynamicArrayOfStructs;

    address _address;
    string _string = "slither-read-storage";
    uint8 packedUint8 = 8;
    bytes8 packedBytes = "aaaaaaaa";

    enum Enum {
        a,
        b,
        c
    }
    Enum _enumA = Enum.a;
    Enum _enumB = Enum.b;
    Enum _enumC = Enum.c;

    uint256[3] fixedArray;
    uint256[3][] dynamicArrayOfFixedArrays;
    uint[][3] fixedArrayofDynamicArrays;
    uint[][] multidimensionalArray;
    PackedStruct[] dynamicArrayOfStructs;
    PackedStruct[3] fixedArrayOfStructs;
    NestedStruct _nestedStruct;
    function store() external {
        require(_address == address(0));
        _address = msg.sender;

        mappingPackedStruct[packedUint] = _packedStruct; 

        deepMappingPackedStruct[_address][packedUint] = _packedStruct;

        deepMappingElementaryTypes[_address][1] = true;
        deepMappingElementaryTypes[_address][2] = true;

        fixedArray = [1, 2, 3];

        dynamicArrayOfFixedArrays.push(fixedArray);
        dynamicArrayOfFixedArrays.push([4, 5, 6]);

        fixedArrayofDynamicArrays[0].push(7);
        fixedArrayofDynamicArrays[1].push(8);
        fixedArrayofDynamicArrays[1].push(9);
        fixedArrayofDynamicArrays[2].push(10);
        fixedArrayofDynamicArrays[2].push(11);
        fixedArrayofDynamicArrays[2].push(12);

        multidimensionalArray.push([13]);
        multidimensionalArray.push([14, 15]);
        multidimensionalArray.push([16, 17, 18]);

        dynamicArrayOfStructs.push(_packedStruct);
        dynamicArrayOfStructs.push(PackedStruct(false, 10));
        fixedArrayOfStructs[0] = _packedStruct;
        fixedArrayOfStructs[1] = PackedStruct(false, 10);

        mappingDynamicArrayOfStructs[_address].push(dynamicArrayOfStructs[0]);
        mappingDynamicArrayOfStructs[_address].push(dynamicArrayOfStructs[1]);

        _nestedStruct.nested._values.push(11);
        _nestedStruct.nested._values.push(22);
        _nestedStruct.nested._indexes[_address] = 1234;
        _nestedStruct.a = 123456789;
        _nestedStruct.b = true;
        _nestedStruct.c = 4095;
        _nestedStruct.d = 4294967295;
        _nestedStruct.e = 112233445566;
    }
}
