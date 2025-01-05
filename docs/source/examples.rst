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
    print(result.compute())  # 26 - takes a bit of time
    print(result.compute())  # 26 - but is cached so it's almost instant

LatenPy automatically tracks dependencies and caches results, so the second compute()
call is almost instant. This is a simple example, but LatenPy can handle much more
complex computations.

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

For example, you can nest latent computations in lists, dictionaries, and other data
structures. LatenPy will automatically compute whatever is needed to get the final output
and cache the intermediate results.

Scientific Computing Examples
--------------------------

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

LatenPy is useful for defining scientific computing pipelines, and only performing
computations when needed. This is useful for having all the code and processing steps
defined and accessible, but only perform whichever computations are needed right now or
for a particular task. 

For example, you can define a standard pipeline for data processing that has several
endpoints with a number of shared intermediate variables. Then, you can run ``compute``
on a single endpoint variable. LatenPy will automatically compute the necessary
intermediate variables and exclude unnecessary computations. This way, you'll be able to
use your pipeline to explore a particular endpoint, but avoid performing unnecessary
computations. 

Parameter Studies
---------------

Smart Recomputation
~~~~~~~~~~~~~~~~

.. code-block:: python

    @latent
    def fit_model(X, y, learning_rate):
        # Expensive model fitting
        return model_parameters

    @latent
    def evaluate(model_params, test_data):
        return accuracy_score(test_data, predict(model_params))

    # Initial computation
    model = fit_model(X_train, y_train, lr=0.01)
    result = evaluate(model, test_data)
    first_score = result.compute()

    # Update learning rate - only recomputes affected nodes
    model.update_kwargs(learning_rate=0.02)
    new_score = result.compute()  # Automatically recomputes both fit_model and evaluate

LatenPy maintains a dependency graph that tracks the relationships between latent
computations. This way, it allows you to update parameters of a particular computation
and automatically detect which variables are affected by the update. 

LatenPy's dependency tracking is particularly useful for exploring how changes to one
the way one computation is performed affect other results (including model optimization).
Suppose your scientific computing pipeline has a number of parameters that you want to
study such as parameters related to filtering timeseries data. You can define the
pipeline once, then compute and plot the final result. Then, update any parameter you
want to study, and the pipeline will automatically detect which components need to be
recomputed, therefore making it easy and efficient to explore the effect of each
parameter on your pipeline. 


Visualization Tools
-------------------

Dependency Graph Analysis
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from latenpy import latent, visualize

    @latent
    def preprocess(data):
        return data * 2

    @latent
    def analyze(preprocessed, threshold):
        return preprocessed[preprocessed > threshold]

    @latent
    def aggregate(analyzed_data):
        return analyzed_data.mean()

    # Create computation chain
    result = aggregate(analyze(preprocess(raw_data), threshold=5))

    # Visualize computation graph with status
    G = result.get_dependency_graph()
    visualize(G)  # Shows computed vs uncached vs needs-recomputation nodes

    # Get detailed computation statistics
    stats = result.latent_data.stats
    print(stats)  # Shows compute count, access patterns, caching info

LatenPy's visualization tools provide immediate insight into computation status,
dependencies, and performance metrics. This transparency is invaluable for debugging
complex computational workflows and understanding resource usage patterns.

Memory Management
--------------

.. code-block:: python

    @latent(disable_cache=True)
    def generate_large_matrix(size):
        return np.random.random((size, size))

    @latent
    def process_chunk(matrix, start, end):
        return matrix[start:end].sum()

    # Process large data in chunks without holding everything in memory
    matrix = generate_large_matrix(10000)
    chunk_size = 1000
    results = [
        process_chunk(matrix, i, i+chunk_size)
        for i in range(0, 10000, chunk_size)
    ]

    # Process one at a time, clearing cache as we go
    for result in results:
        value = result.compute()
        process_value(value)
        result.clear_cache()  # Explicitly manage memory

LatenPy provides explicit control over caching and memory management, allowing you to 
handle large datasets efficiently in memory-constrained environments. While distributed 
computing frameworks excel at processing big data across clusters, LatenPy optimizes for
local scientific computing workflows where memory management is critical. This is
particularly useful for large datasets that are not feasible to load into memory all at
once but that you want to have "at your fingertips" for interactive exploration. 