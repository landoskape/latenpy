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

When the parameters of a latent object are changed, the dependency graph is updated
automatically. You can update the parameters of a latent object by using the ``update``
methods. 

.. code-block:: python

    @latent
    def add(a, b, offset=0):
        return a + b + offset

    @latent
    def multiply(a, b):
        return a * b

    # Creates a dependency chain
    x = multiply(2, 3)
    y = add(x, 4, offset=0)

    result = y.compute()
    print(result)

    # Update the parameters of the latent object
    x.update_args(4, 5)
    result = y.compute()
    print(result)

    # You can also update the keyword arguments of a latent object
    x.update_kwargs(offset=1)
    result = y.compute()
    print(result)

    # You can even update the function itself
    x.update_func(lambda a, b: a ** b)
    result = y.compute()
    print(result)


Caching System
------------

Smart Caching
~~~~~~~~~~~~

Results are automatically cached when computed:

- Cached results are reused when possible
- Cache is invalidated when dependencies change

Cache Control
~~~~~~~~~~~

You can control caching behavior:

.. code-block:: python

    # Clear cache for a specific computation
    result.clear_cache()

    # Check if result is cached
    is_cached = bool(result.latent_data)

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