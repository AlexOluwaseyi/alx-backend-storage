#!/usr/bin/env python3

from exercise import *

cache = Cache()

# Call the store method to store some values
cache.store("foo")
cache.store("bar")
cache.store(42)

# Apply the replay decorator to the store method
# cache.store = replay(cache.store)

# Now calling replay(cache.store) should print the desired output
replay(cache.store)

