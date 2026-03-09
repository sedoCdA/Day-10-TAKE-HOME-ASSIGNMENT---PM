# Interview Answers — Day 10 PM (Functions, Scope, Closures)

---

## Q1 — The LEGB Rule

### What is LEGB?

LEGB is the order Python follows when looking up a variable name:
```
L — Local       : Inside the current function
E — Enclosing   : Inside any enclosing function (closures)
G — Global      : At the module (file) level
B — Built-in    : Python's built-in names (len, print, range...)
```

Python searches in this exact order and stops at the first match.

### Scope Diagram
```
+-----------------------------+
|  Built-in (len, print...)   |
|  +----------------------+   |
|  |  Global (module)     |   |
|  |  +--------------+    |   |
|  |  | Enclosing fn |    |   |
|  |  |  +--------+  |    |   |
|  |  |  | Local  |  |    |   |
|  |  |  +--------+  |    |   |
|  |  +--------------+    |   |
|  +----------------------+   |
+-----------------------------+
```

### Concrete Example
```python
x = "global"          # Global scope

def outer():
    x = "enclosing"   # Enclosing scope

    def inner():
        x = "local"   # Local scope
        print(x)      # Prints "local" — Local found first

    inner()
    print(x)          # Prints "enclosing"

outer()
print(x)              # Prints "global"
```

### Local vs Global — same variable name

When a variable exists in both local and global scope, Python always
uses the local one inside the function. The global variable is
not affected.
```python
count = 10            # global

def show():
    count = 99        # local — completely separate from global count
    print(count)      # 99

show()
print(count)          # still 10 — global unchanged
```

### The global keyword

`global` lets a function read and modify a module-level variable
instead of creating a local one.
```python
count = 0

def increment():
    global count
    count += 1

increment()
print(count)  # 1
```

### Why global is a code smell

- It creates hidden dependencies between functions and module state
- Any function anywhere in the file can modify the variable
- Makes code harder to test, debug, and reason about
- Breaks the principle that functions should only depend on their inputs

### The alternative — return values and parameters

Pass the value in, return the modified value out. No shared state needed.
```python
def increment(count: int) -> int:
    return count + 1

count = 0
count = increment(count)
print(count)  # 1
```

This is predictable, testable, and has no side effects.

---

## Q2 — Memoize Decorator
```python
import functools

def memoize(func):
    """
    Caches results of function calls.
    Returns cached result when called with the same arguments.

    Args:
        func: The function to cache.

    Returns:
        Wrapper function with a results cache attached.

    Example:
        @memoize
        def fibonacci(n):
            if n <= 1: return n
            return fibonacci(n-1) + fibonacci(n-2)
    """
    cache = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    wrapper.cache = cache   # expose cache for inspection if needed
    return wrapper


@memoize
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# Tests
print(fibonacci(10))   # 55
print(fibonacci(50))   # 12586269025 — instant with memoization
print(fibonacci(0))    # 0
print(fibonacci(1))    # 1

# Without memoization, fibonacci(50) would require
# 2^50 = ~1 quadrillion recursive calls and take hours.
# With memoization, each value is computed exactly once — O(n) total.
```

### How it works

- `cache = {}` is created once in the closure when the decorator runs
- Every call checks if `args` is already a key in cache
- If yes: returns stored result immediately — no recomputation
- If no: computes, stores, then returns the result
- The key is `args` as a tuple — tuples are hashable so they work as dict keys

---

## Q3 — Debug Problem

### Buggy code
```python
total = 0

def add_to_cart(item, cart=[]):      # Bug 1
    cart.append(item)
    total = total + len(cart)         # Bug 2
    return cart

print(add_to_cart('apple'))
print(add_to_cart('banana'))
```

### Bug 1 — Mutable default argument

Using `cart=[]` as a default parameter is a classic Python trap.
Default argument values are created ONCE when the function is defined,
not each time the function is called.

This means all calls that use the default share the SAME list object.
```
Call 1: add_to_cart('apple')  → cart = ['apple']
Call 2: add_to_cart('banana') → cart = ['apple', 'banana']  ← wrong!
```

Fix: use None as the default and create a new list inside the function.
```python
def add_to_cart(item, cart=None):
    if cart is None:
        cart = []
```

### Bug 2 — Scope issue (UnboundLocalError)

`total = total + len(cart)` tries to read `total` before assigning it
locally. Because Python sees the assignment `total = ...` in the
function, it treats `total` as a local variable throughout the function.
But on the right side, `total` has not been assigned yet locally,
so Python raises an `UnboundLocalError`.

Using `global` would fix the crash but is a code smell.
The clean fix is to pass `total` as a parameter and return it.

### Fully fixed version
```python
def add_to_cart(item, cart=None, total=0):
    """
    Adds an item to a cart and updates the total count.

    Args:
        item: Item to add to the cart.
        cart: Existing cart list. Defaults to a new empty list.
        total: Current total count. Defaults to 0.

    Returns:
        Tuple of (updated cart, updated total).
    """
    if cart is None:
        cart = []
    cart.append(item)
    total = total + len(cart)
    return cart, total

# Tests
cart, total = add_to_cart("apple")
print(cart, total)                       # ['apple'] 1

cart, total = add_to_cart("banana", cart, total)
print(cart, total)                       # ['apple', 'banana'] 3

# Each call with no cart gets a fresh list
cart2, total2 = add_to_cart("orange")
print(cart2, total2)                     # ['orange'] 1 — not polluted
