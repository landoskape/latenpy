LatenPy Documentation
====================

LatenPy is a Python package that provides elegant lazy evaluation and computation caching with automatic dependency tracking. It's designed to help you optimize complex computational workflows by deferring expensive calculations until they're needed and caching results efficiently.

Key Features
-----------

- 🦥 **Lazy Evaluation**: Defer computations until their results are actually needed
- 📦 **Automatic Caching**: Cache computation results for reuse
- 🔄 **Dependency Tracking**: Automatically track and manage computational dependencies
- 📊 **Visualization**: Visualize computation graphs to understand dependencies
- 🎯 **Smart Recomputation**: Only recompute results when dependencies change
- 📝 **Rich Statistics**: Track computation and access patterns

Installation
------------

.. code-block:: bash

   pip install latenpy

Quick Start
----------

Here's a simple example showing how to use LatenPy:

.. code-block:: python

   from latenpy import latent

   @latent
   def expensive_calculation(x):
       return x ** 2

   @latent
   def complex_operation(a, b):
       return a + b

   # Create lazy computations
   calc1 = expensive_calculation(5)
   calc2 = expensive_calculation(10)
   result = complex_operation(calc1, calc2)

   # Nothing is computed yet!
   # Computation happens only when we call .compute()
   final_result = result.compute()  # 125

User Guide
----------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   core_concepts
   api_reference
   examples

Core Concepts
------------

- **Latent Objects**: Wrap functions and their arguments for lazy evaluation
- **Dependency Graph**: Automatically tracks relationships between computations
- **Smart Caching**: Results are cached and only recomputed when necessary
- **Computation Control**: Fine-grained control over when and how computations occur

Use Cases
---------

- 🔬 **Scientific Computing**: Manage complex computational pipelines
- 📊 **Data Analysis**: Optimize data processing workflows
- 🔄 **Parameter Studies**: Flexibly modify inputs and track changes in results

Contributing
-----------

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

License
-------

This project is licensed under the GNU General Public License v3 (GPLv3) - see the LICENSE file for details.

Indices and tables
-----------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

