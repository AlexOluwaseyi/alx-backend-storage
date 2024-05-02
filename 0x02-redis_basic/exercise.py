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
from functools import wraps
from uuid import uuid4
from typing import Callable, Union

union = Union[str, int, bytes, float]


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.
    """
    call_count = 0

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """incrememter"""
        key = method.__qualname__
        count = self._redis.incr(key)
        '''
        nonlocal call_count
        call_count += 1'''
        return method(self, *args, **kwargs)

    return wrapper


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

    @count_calls
    def store(self, data: Union[str, int, bytes, float]) -> str:
        """
        store method that takes a data argument and returns a string.
        The method should generate a random key (e.g. using uuid), store
        the input data in Redis using the random key and return the key.
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> union:
        """
        a get method that take a key string argument and an
        optional Callable argument named fn. This callable will
        be used to convert the data back to the desired format.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Retrieve data from the cache and convert to string
        """
        return self.get(key, fn=lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        Retrieve data from the cache and convert to integer
        """
        return self.get(key, fn=int)
