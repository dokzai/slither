// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title A simple example contract for calculations
 */
contract A {

    /// @notice Struct to hold data related to each calculation.
    /// @param a The first operand.
    /// @param b The second operand.
    /// @param operationType The type of operation performed.
    /// @param result The result of the operation.
    struct CalculationData {
        uint a;
        uint b;
        string operationType;
        uint result;
    }

    /// @notice The state variable holding the total number of calculations performed.
    /// @dev This can be used for auditing or metrics.
    uint256 public totalCalculations;

    /// @notice Array to hold the calculation data.
    /// @dev The array is publicly readable for transparency or auditing.
    CalculationData[] public calculations;

    /// @notice Custom error for values exceeding limit in the protected function.
    /// @param value The calculated sum of the input numbers.
    /// @param limit The allowed limit for the sum.
    error ProtectedValueLimitExceeded(uint value, uint limit);

    /// @notice Custom error for values exceeding limit in the assembly function.
    /// @param value The calculated sum of the input numbers.
    /// @param limit The allowed limit for the sum.
    error NotProtectedAsmValueLimitExceeded(uint value, uint limit);

    /// @notice Custom error for values exceeding limit in the unchecked function.
    /// @param value The calculated sum of the input numbers.
    /// @param limit The allowed limit for the sum.
    error NotProtectedUncheckedValueLimitExceeded(uint value, uint limit);

    /// @notice Emitted when the `protected` function is called.
    /// @param result The square of the sum of the two input numbers.
    event ProtectedCalled(uint result);

    /// @notice Emitted when the `not_protected_asm` function is called.
    /// @param result The square of the sum of the two input numbers.
    event NotProtectedAsmCalled(uint result);

    /// @notice Emitted when the `not_protected_unchecked` function is called.
    /// @param result The square of the sum of the two input numbers.
    event NotProtectedUncheckedCalled(uint result);

    constructor() {
        totalCalculations = 0;
    }

    /**
     * @dev Increments the total number of calculations and saves the calculation data.
     * @param a The first operand.
     * @param b The second operand.
     * @param operationType The type of operation performed.
     * @param result The result of the operation.
     */
    function _saveCalculationData(uint a, uint b, string memory operationType, uint result) internal {
        CalculationData memory newCalculation = CalculationData(a, b, operationType, result);
        calculations.push(newCalculation);
        totalCalculations += 1;
    }

    /**
     * @dev Calculates the square of the sum of two numbers.
     * @param a The first number.
     * @param b The second number.
     * @return sum The sum of `a` and `b`.
     * @return square The square of the sum of `a` and `b`.
     */
    function _protected(uint a, uint b) internal returns(uint sum, uint square){
        sum = a + b;
        if (sum > 100) revert ProtectedValueLimitExceeded(sum, 100);

        square = sum * sum;
        emit ProtectedCalled(square);
        _saveCalculationData(a, b, "Protected", square);

        return (sum, square);
    }

    /**
     * @dev Calculates the square of the sum of two numbers using inline assembly.
     * @param a The first number.
     * @param b The second number.
     * @return The square of the sum of `a` and `b`.
     */
    function _not_protected_asm(uint a, uint b) internal returns(uint){
        uint sum = a + b;
        if (sum > 100) revert NotProtectedAsmValueLimitExceeded(sum, 100);

        uint result;
        assembly {
            result := mul(sum, sum)
        }
        emit NotProtectedAsmCalled(result);
        _saveCalculationData(a, b, "Not Protected ASM", result);

        return result;
    }

    /**
     * @dev Calculates the square of the sum of two numbers without using SafeMath.
     *      Note: This function does not protect against overflow.
     * @param a The first number.
     * @param b The second number.
     * @return The square of the sum of `a` and `b`.
     */
    function _not_protected_unchecked(uint a, uint b) internal returns(uint){
        uint sum = a + b;
        if (sum > 100) revert NotProtectedUncheckedValueLimitExceeded(sum, 100);

        uint result;
        unchecked {
            result = sum * sum;
        }
        emit NotProtectedUncheckedCalled(result);
        _saveCalculationData(a, b, "Not Protected Unchecked", result);

        return result;
    }

    /**
     * @dev Public function that utilizes the above internal functions for demonstration.
     * @param a The first number.
     * @param b The second number.
     */
    function f(uint a, uint b) public {
        _protected(a, b);
        _not_protected_asm(a, b);
        _not_protected_unchecked(a, b);
    }
}
