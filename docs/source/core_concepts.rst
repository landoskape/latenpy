Core Concepts
============

Latent Objects
-------------

A Latent object is the fundamental building block in LatenPy. It represents a computation that:

- Is defined but not immediately executed
- Tracks its dependencies automatically
- Caches its results
- Only computes when explicitly requested

Creating Latent Objects
~~~~~~~~~~~~~~~~~~~~~

Use the ``@latent`` decorator to create functions that return Latent objects:

.. code-block:: python

    from latenpy import latent

    @latent
    def my_function(x):
        return x * 2

    # Creates a Latent object
    result = my_function(5)
    # Computation happens here
    value = result.compute()

Dependency Tracking
-----------------

LatenPy automatically builds a directed acyclic graph (DAG) of computations:

- Nodes represent individual computations
- Edges represent dependencies between computations
- The graph is used to determine:
    - What needs to be recomputed
    - What can be reused from cache
    - The order of computations

Example:

.. code-block:: python

    @latent
    def add(a, b):
        return a + b

    @latent
    def multiply(a, b):
        return a * b

    # Creates a dependency chain
    x = multiply(2, 3)
    y = add(x, 4)

    # You can visualize the dependency graph
    y.visualize()

Caching System
------------

Smart Caching
~~~~~~~~~~~~

Results are automatically cached when computed:

- Cached results are reused when possible
- Cache is invalidated when dependencies change
- Memory efficient - only keeps necessary results

Cache Control
~~~~~~~~~~~

You can control caching behavior:

.. code-block:: python

    # Clear cache for a specific computation
    result.clear_cache()

    # Check if result is cached
    is_cached = bool(result.latent_data)

Computation Control
-----------------

Manual Control
~~~~~~~~~~~~

You control when computations happen:

.. code-block:: python

    # Define computation
    result = complex_calculation(data)

    # Nothing happens until...
    value = result.compute()  # Computation occurs here

Automatic Dependencies
~~~~~~~~~~~~~~~~~~~

Dependencies are handled automatically:

- When a dependency changes, dependent results are recomputed
- Unchanged results remain cached
- Optimal computation order is determined automatically

Best Practices
------------

1. Use latent objects for:
    - Expensive calculations
    - Results you might need multiple times
    - Complex dependency chains

2. Clear caches when:
    - Memory usage is high
    - Results are no longer needed
    - You want to force recomputation

3. Visualize dependency graphs to:
    - Understand computation flow
    - Debug complex pipelines
    - Optimize computation chains 