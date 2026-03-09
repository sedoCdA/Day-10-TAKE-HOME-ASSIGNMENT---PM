# decorators.py
# Day 10 PM - Decorators: timer, logger, retry

import time
import functools


# -----------------------------------------
# 1. @timer
# -----------------------------------------
def timer(func):
    """
    Decorator that measures and prints the execution time of a function.

    Args:
        func: The function to wrap.

    Returns:
        Wrapper function that prints elapsed time after each call.

    Example:
        @timer
        def slow_function():
            time.sleep(1)
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start  = time.time()
        result = func(*args, **kwargs)
        end    = time.time()
        print(f"[timer] '{func.__name__}' ran in {end - start:.6f} seconds")
        return result
    return wrapper


# -----------------------------------------
# 2. @logger
# -----------------------------------------
def logger(func):
    """
    Decorator that logs function name, arguments, and return value.

    Args:
        func: The function to wrap.

    Returns:
        Wrapper function that prints call details before and after execution.

    Example:
        @logger
        def add(a, b):
            return a + b
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[logger] Calling '{func.__name__}'")
        print(f"         args   : {args}")
        print(f"         kwargs : {kwargs}")
        result = func(*args, **kwargs)
        print(f"[logger] '{func.__name__}' returned: {result}")
        return result
    return wrapper


# -----------------------------------------
# 3. @retry
# -----------------------------------------
def retry(max_attempts: int = 3):
    """
    Decorator factory that retries a function up to max_attempts times
    if it raises an exception.

    Args:
        max_attempts: Maximum number of attempts before giving up.
                      Defaults to 3.

    Returns:
        Decorator that wraps the function with retry logic.

    Example:
        @retry(max_attempts=3)
        def unstable_function():
            ...
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"[retry] '{func.__name__}' attempt {attempt}/{max_attempts} failed: {e}")
            print(f"[retry] '{func.__name__}' failed after {max_attempts} attempts.")
            raise last_exception
        return wrapper
    return decorator


# -----------------------------------------
# Demo
# -----------------------------------------
if __name__ == "__main__":

    # --- timer demo ---
    @timer
    def compute_sum(n: int) -> int:
        return sum(range(n))

    compute_sum(1_000_000)

    # --- logger demo ---
    @logger
    def add(a: int, b: int) -> int:
        return a + b

    add(10, 20)
    add(5, b=15)

    # --- retry demo ---
    attempt_count = 0

    @retry(max_attempts=3)
    def flaky_function():
        global attempt_count
        attempt_count += 1
        if attempt_count < 3:
            raise ConnectionError("Service unavailable")
        return "Success on attempt 3"

    result = flaky_function()
    print(f"[demo] Final result: {result}")

    # --- retry exhausted demo ---
    @retry(max_attempts=2)
    def always_fails():
        raise ValueError("This always fails")

    try:
        always_fails()
    except ValueError as e:
        print(f"[demo] Caught after retries exhausted: {e}")

    # --- stacking decorators ---
    @timer
    @logger
    def multiply(a: int, b: int) -> int:
        return a * b

    multiply(6, 7)
