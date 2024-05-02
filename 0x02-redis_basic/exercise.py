#!/usr/bin/env python3

"""
Create a Cache class. In the __init__ method, store an instance
of the Redis client as a private variable named _redis
(using redis.Redis()) and flush the instance using flushdb.

Create a store method that takes a data argument and returns
a string. The method should generate a random key (e.g. using
uuid), store the input data in Redis using the random
key and return the key.

Type-annotate store correctly. Remember that data can
be a str, bytes, int or float.
"""

import redis
from uuid import uuid4
from typing import Any


class Cache:
    """
    Class Definition for Cache for redis
    """
    def __init__(self):
        """
        the __init__ method, store an instance of the Redis
        client as a private variable named _redis
        (using redis.Redis()) and flush the instance using flushdb.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Any) -> str:
        """
        store method that takes a data argument and returns a string.
        The method should generate a random key (e.g. using uuid), store
        the input data in Redis using the random key and return the key.
        """
        key = uuid4()
        self._redis.set(str(key), data)
        return str(key)