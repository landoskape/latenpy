Advanced Usage
=============

Cache Management
--------------

Manual Cache Control
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    @latent
    def expensive_calculation(x):
        return x ** 2

    result = expensive_calculation(10)
    
    # Compute and cache
    value1 = result.compute()
    
    # Clear specific cache
    result.clear_cache()
    
    # Force recomputation
    value2 = result.compute()

Dependency Graph Analysis
----------------------

Accessing the Graph
~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Get the dependency graph
    G = result.get_dependency_graph()
    
    # Analyze graph properties
    computed_nodes = get_computed_nodes(G)
    uncached_nodes = get_uncached_nodes(G)
    updated_nodes = get_updated_nodes(G)

Custom Visualization
~~~~~~~~~~~~~~~~~

.. code-block:: python

    import networkx as nx
    import matplotlib.pyplot as plt

    # Get the graph
    G = result.get_dependency_graph()

    # Custom layout
    pos = nx.spring_layout(G)
    
    # Custom visualization
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, 
            node_color='lightblue',
            node_size=1000,
            with_labels=True)
    plt.title('Computation Dependencies')
    plt.show()

Error Handling
------------

Handling Computation Errors
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    @latent
    def risky_calculation(x):
        if x < 0:
            raise ValueError("Input must be positive")
        return x ** 0.5

    # Error will be raised only when computed
    result = risky_calculation(-1)
    try:
        value = result.compute()
    except ValueError as e:
        print(f"Computation failed: {e}")

Performance Optimization
---------------------

Parallel Processing
~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Future feature example
    @latent(parallel=True)
    def parallel_calculation(data):
        # Process data in parallel
        return processed_result

Memory Management
~~~~~~~~~~~~~~~

.. code-block:: python

    # Set up memory-intensive calculation
    @latent
    def big_calculation(size):
        return np.random.random((size, size))

    # Create multiple calculations
    results = [big_calculation(1000) for _ in range(10)]
    
    # Process one at a time to manage memory
    for r in results:
        value = r.compute()
        # Process value
        r.clear_cache()  # Free memory

Best Practices
------------

1. Memory Management
   - Clear caches for large intermediate results
   - Use generators for processing large datasets
   - Monitor memory usage in long computation chains

2. Error Handling
   - Implement proper error handling in latent functions
   - Use try/except blocks when computing
   - Consider adding cleanup code in except blocks

3. Performance
   - Group related computations
   - Reuse common intermediate results
   - Clear unnecessary caches
   - Monitor computation graphs for optimization opportunities 