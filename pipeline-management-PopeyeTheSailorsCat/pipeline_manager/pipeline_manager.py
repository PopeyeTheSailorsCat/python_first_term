import functools


def pipeline():
    """
    :return: returns a decorator that allows to add steps to the pipeline
    """

    def handle(func=None, *, depends_on=[], remembered_func=[]):
        if func is None:  # If we got a dependent function
            def decorator(func):
                return handle(func, depends_on=depends_on)  # Remember the dependency

            return decorator
        remembered_func.append([func, depends_on])  # I remember the functions that were given to us and their dependencies

        def func_dependence_run(this_func_depends, *args, **kwargs):  # Run through the dependencies of our function and run them
            for dependence in this_func_depends:  # For all dependencies of this function
                for functions in remembered_func:  # For all the functions we wrapped
                    if dependence == functions[0].__name__:     # If we wrapped this function
                        func_dependence_run(*args, functions[1], **kwargs) # Run the dependency checking function for it
                        semi_res = functions[0](*args, **kwargs)  # We get the value of our function itself
                        # res+=semi_res #If we need to remember the values of the function
            return

        @functools.wraps(func)  # I give inner attributes of func
        def inner(*args, **kwargs):
            func_dependence_run(depends_on, *args, **kwargs)    # Running through the dependencies of the received function
            res = func(*args, **kwargs)   # We get and return the value of our function
            return res

        return inner    # Returning our function in the wrapper

    return handle   # Returning our decorator

