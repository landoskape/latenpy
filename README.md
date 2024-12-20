# LatenPy

LatenPy is a Python package that provides elegant lazy evaluation and computation caching with automatic dependency tracking. It's designed to help you optimize complex computational workflows by deferring expensive calculations until they're needed and caching results efficiently.

[![PyPI version](https://badge.fury.io/py/latenpy.svg)](https://badge.fury.io/py/latenpy)
[![Documentation Status](https://readthedocs.org/projects/latenpy/badge/?version=latest)](https://latenpy.readthedocs.io/en/latest/?badge=latest)
[![Python Versions](https://img.shields.io/pypi/pyversions/latenpy.svg)](https://pypi.org/project/latenpy/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Tests](https://github.com/landoskape/latenpy/actions/workflows/tests.yml/badge.svg)](https://github.com/landoskape/latenpy/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/landoskape/latenpy/branch/main/graph/badge.svg)](https://codecov.io/gh/landoskape/latenpy)

[Full Documentation](https://latenpy.readthedocs.io/) | [GitHub](https://github.com/landoskape/latenpy) | [PyPI](https://pypi.org/project/latenpy/)


## Features

- 🦥 **Lazy Evaluation**: Defer computations until their results are actually needed
- 📦 **Automatic Caching**: Cache computation results for reuse
- 🔄 **Dependency Tracking**: Automatically track and manage computational dependencies
- 📊 **Visualization**: Visualize computation graphs to understand dependencies
- 🎯 **Smart Recomputation**: Only recompute results when dependencies change
- 📝 **Rich Statistics**: Track computation and access patterns

## Installation
```bash
pip install latenpy
```

## Documentation

Comprehensive documentation is available at [Read the Docs](https://latenpy.readthedocs.io/), including:

- **Quick Start Guide**: Get up and running with basic examples
- **Core Concepts**: Learn about Latent Objects, Dependency Tracking, and Caching
- **API Reference**: Detailed documentation of all classes and functions
- **Advanced Usage**: Topics like cache management, dependency graph analysis, and performance optimization
- **Examples**: Real-world examples including scientific computing and data processing pipelines

To build the documentation locally:

```bash
cd docs
make html
```

The built documentation will be available in `docs/build/html/index.html`.

## Quick Start

Here's a simple example showing how to use LatenPy:

```python
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
```

## Advanced Features

### Dependency Visualization

LatenPy can visualize your computation graph:

```python
from latenpy import visualize

# Visualize the computation graph
G = result.get_dependency_graph()
visualize(G)
```

### Computation Statistics

Track detailed statistics about your computations:

```python
# Get computation statistics
stats = result.latent_data.stats
print(stats)
# {
#     "computed": True,
#     "compute_count": 1,
#     "access_count": 1,
#     "last_compute": "2024-03-21 10:30:00",
#     "last_access": "2024-03-21 10:30:00",
#     "age": 42.0
# }
```

### Nested Computations

LatenPy handles nested data structures automatically:

```python
@latent
def process_list(items):
    return [x * 2 for x in items]

@latent
def sum_results(processed):
    return sum(processed)

# Works with nested structures
data = process_list([1, 2, 3])
total = sum_results(data)
result = total.compute()  # 12
```

## Key Concepts

- **Latent Objects**: Wrap functions and their arguments for lazy evaluation
- **Dependency Graph**: Automatically tracks relationships between computations
- **Smart Caching**: Results are cached and only recomputed when necessary
- **Computation Control**: Fine-grained control over when and how computations occur

## Use Cases

- 🔬 Scientific Computing: Manage complex computational pipelines
- 📊 Data Analysis: Optimize data processing workflows
- 🔄 Parameter Studies: Flexibly modify inputs and track changes in results

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.