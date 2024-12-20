"""
latenpy - A package for lazy evaluation to optimize scientific analysis workflows

This module provides a simple framework for defining and managing latent computations
in Python. It allows you to define functions that are not immediately evaluated, but
instead are computed only when the result is needed. This can be useful for complex
computations that are expensive or time-consuming, or for building complex computation
graphs with dependencies.

The main class is `Latent`, which represents a latent computation. You can define
a latent computation by wrapping a function with the `@latent` decorator, which
returns a `Latent` object. You can then call the `compute()` method on the `Latent`
object to compute the result.

Example usage:
```python
@latent
def add(a, b):
    return a + b

@latent
def multiply(a, b):
    return a * b

@latent
def power(a, b):
    return a ** b

# Define a computation graph
result = add(multiply(2, 3), power(4, 5))

# Compute the result
print(result.compute()) # will take some time (not really in this case)
print(result.compute()) # will be instant, as the result is cached
```

The `Latent` class also provides methods for analyzing the computation graph, visualizing
the dependencies, and clearing cached results. You can also access the computation graph
directly using the `get_dependency_graph()` method. You can visualize the computation graph
with the `visualize()` method, which uses NetworkX and Matplotlib to draw the graph.


Areas for improvement:
- Add support for parallel computation
- Add memory load handling and breaking cache (e.g. if memory usage exceeds a threshold)
- Add more sophisticated graph analysis and visualization features
- Benchmarking and profiling tools
- Test suites!
- Context manager for temporary cache control...
- Memoization for repeated objects....
- Serialiation support for saving/loading latent objects and pipelines
- Implement operations on latent objects including all base operators
  - Arithmetic (+, -, *, /, //, %, **)
  - Comparison (<, >, <=, >=, ==, !=)
  - Bitwise (&, |, ^, <<, >>)
  - Boolean (and, or, not)
- We should make sure that the latent objects are computed when relevant!
  - 
"""

from .latent import latent
