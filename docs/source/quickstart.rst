Quick Start Guide
================

Basic Usage
----------

1. First, import LatenPy:

   .. code-block:: python

      from latenpy import latent

2. Define latent functions using the ``@latent`` decorator:

   .. code-block:: python

      @latent
      def add(a, b):
          return a + b

      @latent
      def multiply(a, b):
          return a * b

3. Create computation chains:

   .. code-block:: python

      # These operations are not computed yet
      result1 = multiply(2, 3)
      result2 = add(result1, 10)

4. Compute results when needed:

   .. code-block:: python

      # Computation happens here
      final_result = result2.compute()
      print(final_result)  # 16

Caching Behavior
--------------

Results are automatically cached:

.. code-block:: python

    # First computation
    result = expensive_calculation(10)
    value1 = result.compute()  # Takes time

    # Second computation (instant)
    value2 = result.compute()  # Returns cached result

Working with Dependencies
-----------------------

LatenPy automatically tracks dependencies:

.. code-block:: python

    @latent
    def square(x):
        return x * x

    @latent
    def sum_squares(a, b):
        return square(a) + square(b)

    result = sum_squares(3, 4)
    print(result.compute())  # 25

Visualizing Computations
----------------------

You can visualize the computation graph:

.. code-block:: python

    result = sum_squares(3, 4)
    G = result.get_dependency_graph()
    result.visualize()  # Shows the computation graph 