import pytest
import numpy as np

import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from latenpy import latent


# Basic computation tests
def test_basic_latent_computation():
    @latent
    def add(a, b):
        return a + b

    result = add(2, 3)
    assert not result  # Should not be computed initially
    assert result.compute() == 5
    assert result  # Should be computed after calling compute()


# Test caching behavior
def test_caching():
    computation_count = 0

    @latent
    def expensive_computation(x):
        nonlocal computation_count
        computation_count += 1
        return x * 2

    result = expensive_computation(10)
    assert computation_count == 0  # Not computed yet

    # First computation
    assert result.compute() == 20
    assert computation_count == 1

    # Should use cache
    assert result.compute() == 20
    assert computation_count == 1  # Shouldn't have incremented


# Test nested computations
def test_nested_computations():
    @latent
    def double(x):
        return x * 2

    @latent
    def add(a, b):
        return a + b

    result = add(double(3), double(4))
    assert result.compute() == 14  # (3*2) + (4*2)


# Test dependency tracking
def test_dependency_tracking():
    @latent
    def base(x):
        return x * 2

    @latent
    def dependent(x):
        return x + 1

    base_result = base(5)
    dependent_result = dependent(base_result)
    first_computation = dependent_result.compute()
    assert first_computation == 11  # (5*2) + 1

    # Update base function
    base_result.update_args(10)
    # Should recompute when base changes
    assert dependent_result.compute() == 21  # (10*2) + 1


# Test array operations
def test_array_operations():
    @latent
    def matrix_op(arr):
        return arr * 2

    input_array = np.array([[1, 2], [3, 4]])
    result = matrix_op(input_array)
    np.testing.assert_array_equal(result.compute(), np.array([[2, 4], [6, 8]]))


# Test error handling
def test_error_handling():
    @latent
    def failing_function():
        raise ValueError("Test error")

    result = failing_function()
    with pytest.raises(ValueError, match="Test error"):
        result.compute()


# Test disable_cache option
def test_disable_cache():
    computation_count = 0

    @latent(disable_cache=True)
    def no_cache_func(x):
        nonlocal computation_count
        computation_count += 1
        return x * 2

    result = no_cache_func(5)
    assert result.compute() == 10
    assert computation_count == 1

    # Should recompute even though input hasn't changed
    assert result.compute() == 10
    assert computation_count == 2


# # Test nested data structures
# def test_nested_structures():
#     @latent
#     def process_dict(d):
#         return {k: v * 2 for k, v in d.items()}

#     @latent
#     def process_list(lst):
#         return [x * 2 for x in lst]

#     nested_data = {"numbers": process_list([1, 2, 3]), "values": process_dict({"a": 1, "b": 2})}

#     result = process_dict(nested_data)
#     computed = result.compute()
#     assert computed["numbers"] == [2, 4, 6]
#     assert computed["values"] == {"a": 2, "b": 4}
