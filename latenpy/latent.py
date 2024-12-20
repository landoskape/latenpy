"""A module for lazy evaluation and computation caching with dependency tracking.

This module provides tools for creating and managing lazy computations through the
Latent class and latent decorator. It supports nested data structures, dependency
tracking, and optional result caching.

Classes
------
Latent
   A class that implements lazy evaluation with dependency tracking and caching.

Functions
--------
compute_nested
   Recursively computes Latent objects found within nested data structures.
latent
   Decorator that creates lazy computations with optional caching.
"""

from warnings import warn
from typing import Any, Tuple, Dict, Callable, Set
from collections.abc import Mapping, Sequence
from functools import wraps
import numpy as np
from networkx import DiGraph

from .types import LatentData, T
from .graph import get_updated_nodes, correct_computed_status, validate_no_cycles


def compute_nested(obj: Any, force_recompute: bool = False, dont_cache: bool = False, depth: int = 0, maximum_depth: int = None) -> Any:
    """Recursively compute any Latent objects found within nested data structures.

    Parameters
    ----------
    obj : Any
        The object to process. Can be a Latent object, any nested structure
        containing Latent objects, or any other object.
    force_recompute : bool, optional
        If True, forces recomputation of cached results, by default False.
    dont_cache : bool, optional
        If True, prevents caching of computed results, by default False.
    depth : int, optional
        Current recursion depth, by default 0.
    maximum_depth : int, optional
        Maximum recursion depth before stopping, by default None.

    Returns
    -------
    Any
        The computed result with all Latent objects evaluated.

    Notes
    -----
    Supports the following nested structures:
    - NumPy arrays (i.e. if you have anumpy array of Latent objects, this will compute them all)
    - Mappings (dict-like objects)
    - Sequences (list-like objects)
    - Sets
    - Generators and iterators
    """
    if maximum_depth is not None and depth > maximum_depth:
        warn(f"Maximum depth ({maximum_depth}) reached in compute_nested at object: {type(obj).__name__}. Returning object as-is.")
        return obj

    depth += 1
    kwargs = dict(
        force_recompute=force_recompute,
        dont_cache=dont_cache,
        depth=depth,
        maximum_depth=maximum_depth,
    )

    # Handle Latent objects
    if isinstance(obj, Latent):
        maximum_depth = maximum_depth - 1 if maximum_depth is not None else None
        return obj.compute(force_recompute=force_recompute, dont_cache=dont_cache, maximum_depth=maximum_depth)

    # Handle numpy arrays
    if isinstance(obj, np.ndarray):
        return np.array([compute_nested(x, **kwargs) for x in obj.flat]).reshape(obj.shape)

    # Handle mappings (dict-like objects)
    if isinstance(obj, Mapping):
        return type(obj)({compute_nested(key, **kwargs): compute_nested(value, **kwargs) for key, value in obj.items()})

    # Handle sequences (list-like objects, excluding strings)
    if isinstance(obj, Sequence) and not isinstance(obj, (str, bytes)):
        return type(obj)(compute_nested(item, **kwargs) for item in obj)

    # Handle sets
    if isinstance(obj, Set):
        return type(obj)(compute_nested(item, **kwargs) for item in obj)

    # Handle generators and iterators
    if hasattr(obj, "__iter__") and not isinstance(obj, (str, bytes, Mapping, Sequence, Set)):
        return (compute_nested(item, **kwargs) for item in obj)

    # Base case: return the object as-is
    return obj


class Latent:
    """A class for lazy evaluation with dependency tracking and caching.

    This class enables delayed computation of functions and their arguments,
    with support for dependency tracking, result caching, and nested computations.

    Parameters
    ----------
    func : Callable[..., T]
        The function to be computed lazily.
    *args : Tuple[Any, ...]
        Positional arguments for the function.
    disable_cache : bool, optional
        If True, disables result caching, by default False.
    **kwargs : Dict[str, Any]
        Keyword arguments for the function.

    Attributes
    ----------
    latent_data : LatentData
        Storage for cached computation results.
    computed : bool
        Whether the computation has been performed and cached.

    Methods
    -------
    compute(force_recompute=False, recompute_dependencies=False, dont_cache=False)
        Execute the computation and return the result.
    update_func(func)
        Update the function to be computed.
    update_args(*args)
        Update the positional arguments.
    update_kwargs(**kwargs)
        Update the keyword arguments.
    clear_cache(dependencies=False, dependents=False)
        Clear all cached results in the computation graph.
    """

    def __init__(self, func: Callable[..., T], *args: Tuple[Any, ...], disable_cache: bool = False, **kwargs: Dict[str, Any]):
        self._func = func
        self._args = tuple(args)
        self._kwargs = kwargs
        self.disable_cache = disable_cache
        self.latent_data = LatentData()
        self._needs_recomputation = False  # True if the underlying function or arguments have been updated
        self._computing = False  # For tracking computation status
        self._dependents: Set[Latent] = set()  # Set of nodes that depend on this node

        for arg in args:
            if isinstance(arg, Latent):
                arg._dependents.add(self)
        for value in kwargs.values():
            if isinstance(value, Latent):
                value._dependents.add(self)

    @property
    def func(self) -> Callable[..., T]:
        """Get the function to be computed.

        Returns
        -------
        Callable[..., T]
            The function that will be executed when compute() is called.
        """
        return self._func

    @property
    def args(self) -> Tuple[Any, ...]:
        """Get the positional arguments for the function.

        Returns
        -------
        Tuple[Any, ...]
            The tuple of positional arguments.
        """
        return self._args

    @property
    def kwargs(self) -> Mapping[str, Any]:
        """Get the keyword arguments for the function.

        Returns
        -------
        Mapping[str, Any]
            The mapping of keyword arguments.
        """
        return self._kwargs

    @property
    def computed(self) -> bool:
        """Check if the computation has been performed and cached.

        Returns
        -------
        bool
            True if the result has been computed and cached, False otherwise.
        """
        return bool(self.latent_data)

    def update_func(self, func: Callable[..., T]) -> None:
        """Update the function to be computed.

        Parameters
        ----------
        func : Callable[..., T]
            The new function to use for computation.

        Notes
        -----
        This will clear the cached result and mark all dependent
        computations for recomputation.
        """
        self._func = func
        self._needs_recomputation = True
        self._update_dependents()
        self.latent_data.clear()

    def update_args(self, *args: Tuple[Any, ...]) -> None:
        """Update the positional arguments.

        Parameters
        ----------
        *args : Tuple[Any, ...]
            The new positional arguments.

        Notes
        -----
        This will clear the cached result and mark all dependent
        computations for recomputation.
        """
        self._args = args
        self._needs_recomputation = True
        self._update_dependents()
        self.latent_data.clear()

    def update_kwargs(self, full_reset: bool = False, **kwargs: Dict[str, Any]) -> None:
        """Update the keyword arguments.

        Parameters
        ----------
        full_reset : bool, optional
            If True, replace all existing kwargs. If False, update only
            the provided kwargs, by default False.
        **kwargs : Dict[str, Any]
            The new keyword arguments.

        Notes
        -----
        This will clear the cached result and mark all dependent
        computations for recomputation.
        """
        if full_reset:
            self._kwargs = kwargs
        else:
            self._kwargs.update(kwargs)
        self._needs_recomputation = True
        self._update_dependents()
        self.latent_data.clear()

    def _update_dependents(self, visited: Set = set()) -> None:
        """Recursively update all dependent nodes."""
        for dependent in self._dependents:
            if dependent not in visited:
                visited.add(dependent)
                dependent._needs_recomputation = True
                dependent.latent_data.clear()
                dependent._update_dependents(visited)

    def compute(self, force_recompute: bool = False, recompute_dependencies: bool = False, dont_cache: bool = False, maximum_depth: int = None) -> T:
        """Compute the result and cache if enabled.

        Will iteratively compute all dependencies in arguments and key-word arguments
        if they are also Latent objects.

        Parameters
        ----------
        force_recompute : bool, optional
            If True, recompute even if cached, by default False.
        recompute_dependencies : bool, optional
            If True, recompute all dependencies, by default False.
        dont_cache : bool, optional
            If True, skip caching the result, by default False.
        maximum_depth : int, optional
            Maximum depth for nested computations, by default None.

        Returns
        -------
        T
            The computed result.

        Raises
        ------
        RecursionError
            If a circular dependency is detected.
        Exception
            If the computation fails, with details about the failure.

        Notes
        -----
        This method will:
        1. Check for circular dependencies
        2. Validate the dependency graph
        3. Compute any required dependencies
        4. Execute the computation
        5. Cache the result (unless disabled)
        """
        if self._computing:
            raise RecursionError(f"Circular dependency detected in delayed computation of {self.func.__name__}")

        G = self.get_dependency_graph()
        validate_no_cycles(G)

        # Update dependents of any changed nodes
        correct_computed_status(G)

        # Get nodes that have been updated or have updated dependencies and need to be recomputed
        updated_nodes = get_updated_nodes(G)

        # Check if we can use a cached result
        # If force_recompute, never use cached result
        # If recompute_dependencies, never use cached result (also recompute all dependencies)
        # If updated_nodes, then a previously computed dependency needs to be recomputed
        # If there is not cache, we can't use the cache!
        can_use_cache = not force_recompute and not recompute_dependencies and not updated_nodes and self.latent_data
        if can_use_cache:
            return self.latent_data()

        try:
            # This Latent object is now trying to compute it's result
            self._computing = True

            kwargs = dict(
                force_recompute=recompute_dependencies,
                dont_cache=dont_cache,
                maximum_depth=maximum_depth,
            )
            computed_args = [compute_nested(arg, **kwargs) for arg in self.args]
            computed_kwargs = {key: compute_nested(value, **kwargs) for key, value in self.kwargs.items()}
            result = self.func(*computed_args, **computed_kwargs)
            if not self.disable_cache and not dont_cache:
                self.latent_data.set(result)
            return result

        except Exception as e:
            raise type(e)(f"Error in delayed computation of {self.func.__name__}: {str(e)}") from e

        finally:
            # Reset the computation flag
            self._computing = False

    def __bool__(self) -> bool:
        """Check if the computation has been performed.

        Returns
        -------
        bool
            True if the result has been computed, False otherwise.
        """
        return bool(self.latent_data)

    def __repr__(self) -> str:
        """Get the string representation of the delayed computation.

        Returns
        -------
        str
            A string showing the function name and computation status.
        """
        return f"Latent({self.func.__name__}):{'Computed' if self.latent_data else 'Not computed'}"

    def __len__(self):
        """Enable len() for delayed computations.

        Returns
        -------
        Latent
            A new Latent object that will return the length.
        """

        def get_len(obj):
            return len(obj)

        return Latent(get_len, self)

    def __iter__(self):
        """Enable iteration for delayed computations.

        Returns
        -------
        Latent
            A new Latent object that will return an iterator.
        """

        def get_iter(obj):
            return iter(obj)

        return Latent(get_iter, self)

    def clear_cache(self, dependencies: bool = False, dependents: bool = False) -> None:
        """Clear all cached results in this computation graph.

        Parameters
        ----------
        dependencies : bool, optional
            If True, clear caches of dependencies, by default False
        dependents : bool, optional
            If True, clear caches of dependents, by default False
        """
        self.latent_data.clear()

        if dependencies:
            for arg in self.args:
                if isinstance(arg, Latent):
                    arg.clear_cache(dependencies=True)
            for value in self.kwargs.values():
                if isinstance(value, Latent):
                    value.clear_cache(dependencies=True)

        if dependents:
            for dependent in self._dependents:
                dependent.clear_cache(dependents=True)

    def _get_node_id(self) -> str:
        """Generate a compact node ID."""
        name = self.func.__name__
        instance_id = str(id(self))[-4:]  # Use fewer digits

        # Create simplified arg representations
        arg_strs = []
        for arg in self.args:
            if isinstance(arg, Latent):
                # Just use the function name and id of delayed args
                arg_strs.append(arg.func.__name__ + f"#{str(id(arg))[-4:]}")
            else:
                # For non-delayed args, use a short hash
                try:
                    arg_str = str(hash(arg))[-4:]
                except TypeError:
                    arg_str = type(arg).__name__[:4]
                arg_strs.append(arg_str)

        # Handle kwargs similarly but more concisely
        kwarg_strs = []
        for k, v in sorted(self.kwargs.items()):
            if isinstance(v, Latent):
                kwarg_strs.append(f"{k[:4]}={v.func.__name__}")
            else:
                try:
                    v_str = str(hash(v))[-4:]
                except TypeError:
                    v_str = type(v).__name__[:4]
                kwarg_strs.append(f"{k[:4]}={v_str}")

        # Combine everything into a compact string
        content = f"{name}({','.join(arg_strs + kwarg_strs)})#{instance_id}"
        return content

    def get_dependency_graph(self) -> DiGraph:
        """Build and return a directed graph of computation dependencies.

        Returns
        -------
        DiGraph
            A directed graph where:
            - Nodes are computations
            - Edges represent dependencies
            - Node attributes include:
                - 'label': Description of the computation
                - 'computed': Boolean for cache status
                - 'func_name': Name of the function
        """
        G = DiGraph()
        self._build_graph(G, set())
        return G

    def _build_graph(self, G: DiGraph, visited: Set[str]) -> None:
        """Recursively build the dependency graph.

        Parameters
        ----------
        G : DiGraph
            The graph to build
        visited : Set[str]
            Set of node IDs already processed to avoid redundant traversal
        """
        node_id = self._get_node_id()
        if node_id in visited:
            return

        visited.add(node_id)

        # Add this node to the graph
        G.add_node(
            node_id,
            label=self.func.__name__,
            computed=bool(self.latent_data),
            needs_recomputation=self._needs_recomputation,
            delayed_obj=self,
        )

        # Process arguments
        for arg in self.args:
            if isinstance(arg, Latent):
                arg._build_graph(G, visited)
                G.add_edge(arg._get_node_id(), node_id)

        # Process keyword arguments
        for v in self.kwargs.values():
            if isinstance(v, Latent):
                v._build_graph(G, visited)
                G.add_edge(v._get_node_id(), node_id)


def latent(func=None, *, disable_cache=False):
    """Decorator to create a latent computation that executes only when requested.

    Parameters
    ----------
    func : callable or None
        The function to be delayed. Will be None if decorator is called with
        parameters.
    disable_cache : bool, optional
        If True, disables caching of computation results. Each call to compute()
        will re-execute the function, by default False.

    Returns
    -------
    callable or Latent
        If used as @delayed:
            Returns a Latent object holding the function and arguments
            for later execution.
        If used as @delayed(no_cache=...):
            Returns a decorator function that will create a Latent object.

    See Also
    --------
    Latent : The class that handles lazy evaluation of functions

    Examples
    --------
    Basic usage with default caching:

    >>> @delayed
    ... def expensive_computation(x):
    ...     return x * 2
    ...
    >>> result = expensive_computation(10)  # No computation yet
    >>> result.compute()  # Now computes
    20

    Disable caching for always-fresh results:

    >>> @delayed(no_cache=True)
    ... def always_recompute(x):
    ...     return x * 2
    ...
    >>> result = always_recompute(10)
    >>> result.compute()  # Computes without caching
    20

    Notes
    -----
    The decorated function's computation is deferred until the .compute()
    method is called on the returned Latent object. By default, results
    are cached based on input arguments unless no_cache=True.
    """
    # Called as @latent(disable_cache=...)
    if func is None:
        return lambda f: latent(f, disable_cache=disable_cache)

    # Called as @latent or latent(func, ...)
    @wraps(func)
    def wrapper(*args, **kwargs):
        return Latent(func, *args, **kwargs, disable_cache=disable_cache)

    return wrapper
