Examples
========

Basic Examples
-------------

Simple Arithmetic
~~~~~~~~~~~~~~~

.. code-block:: python

    from latenpy import latent

    @latent
    def add(a, b):
        return a + b

    @latent
    def multiply(a, b):
        return a * b

    # Chain operations
    result = add(multiply(2, 3), multiply(4, 5))
    print(result.compute())  # 26

Nested Data Structures
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    @latent
    def process_list(lst):
        return [x * 2 for x in lst]

    @latent
    def sum_results(processed):
        return sum(processed)

    # Works with nested structures
    data = process_list([1, 2, 3])
    total = sum_results(data)
    result = total.compute()  # 12

Scientific Computing Examples
--------------------------

Matrix Operations
~~~~~~~~~~~~~~

.. code-block:: python

    import numpy as np
    from latenpy import latent

    @latent
    def matrix_multiply(A, B):
        return np.dot(A, B)

    @latent
    def matrix_inverse(A):
        return np.linalg.inv(A)

    # Create sample matrices
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])

    # Define computation chain
    result = matrix_multiply(matrix_inverse(A), B)
    print(result.compute())

Data Processing Pipeline
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    @latent
    def load_data(filename):
        return np.load(filename)

    @latent
    def normalize(data):
        return (data - np.mean(data)) / np.std(data)

    @latent
    def filter_outliers(data, threshold=3):
        z_scores = np.abs((data - np.mean(data)) / np.std(data))
        return data[z_scores < threshold]

    # Create pipeline
    raw_data = load_data('data.npy')
    normalized = normalize(raw_data)
    cleaned = filter_outliers(normalized)
    
    # Execute when needed
    result = cleaned.compute()

Parameter Studies
---------------

Grid Search Example
~~~~~~~~~~~~~~~~

.. code-block:: python

    @latent
    def create_model(param1, param2):
        return {'param1': param1, 'param2': param2}

    @latent
    def evaluate_model(model, data):
        # Simulate model evaluation
        p1, p2 = model['param1'], model['param2']
        return p1 * data + p2

    # Create parameter grid
    param1_values = [1, 2, 3]
    param2_values = [0.1, 0.2, 0.3]
    test_data = np.array([1, 2, 3, 4, 5])

    # Create evaluation grid
    results = {}
    for p1 in param1_values:
        for p2 in param2_values:
            model = create_model(p1, p2)
            results[(p1, p2)] = evaluate_model(model, test_data)

    # Compute all results
    evaluated = {k: v.compute() for k, v in results.items()}

Visualization Example
------------------

Plotting with Caching
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import matplotlib.pyplot as plt

    @latent
    def generate_data(n_points):
        return np.random.normal(0, 1, n_points)

    @latent
    def create_histogram(data, bins=50):
        plt.figure()
        plt.hist(data, bins=bins)
        plt.title('Histogram of Random Data')
        return plt.gcf()

    # Create visualization pipeline
    data = generate_data(1000)
    hist = create_histogram(data)

    # Show plot
    fig = hist.compute()
    plt.show() 