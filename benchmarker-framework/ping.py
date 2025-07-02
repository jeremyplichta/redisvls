import redis
from redis_benchmarker.executors import BaseQueryExecutor, enable_auto_main
from redis_benchmarker.utils import time_operation
import numpy as np
from redisvl.index import SearchIndex
from redisvl.query import VectorQuery, FilterQuery
from redisvl.query.filter import Tag, Num

class PingBenchmark(BaseQueryExecutor):

    def execute_query(self, redis_client: redis.Redis) -> dict:

        result = None
        with time_operation() as latency_ms:
            result = redis_client.ping()

        return {
            "result": result,
            "latency_ms": float(latency_ms),
            "metadata": {
                "query_type": "ping",
                "total_results": 1
            }
        }

# This one line enables full CLI functionality
enable_auto_main(__name__)