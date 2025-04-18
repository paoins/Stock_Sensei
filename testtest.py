def random_search(objective_function: Callable[[np.ndarray], float],
                  bounds: np.ndarray, n_iterations: int) -> Tuple[np.ndarray, float, List[np.ndarray]]:
    """
    Perform a random search optimization.

    Parameters:
    - objective_function (Callable[[np.ndarray], float]): The function to be optimized. It should take a single
        argument (a candidate solution) and return a scalar value.
    - bounds (np.ndarray): A numpy array of shape (n, 2) where n is the number of dimensions. Each row specifies the
        lower and upper bounds for the corresponding dimension.
    - n_iterations (int): The number of iterations to perform the coordinate search.

    Returns:
    - best (np.ndarray): The best candidate solution found.
    - best_eval (float): The evaluation of the best candidate solution.
    - history (List[np.ndarray]): A list of all candidate solutions that were found to be the best at some point
        during the search.
    """
    best = None
    best_eval = float('inf')
    history = []

    #########################################################
    #
    # FILL IN THE CODE BELOW
    #
    #########################################################
    for _ in range(n_iterations):
        candidate = np.array([np.random.uniform(low, high) for (low, high) in bounds])
        evaluation = objective_function(candidate)

        if evaluation < best_eval:
            best, best_eval = candidate, evaluation
            history.append(best.copy())

    return best, best_eval, history
