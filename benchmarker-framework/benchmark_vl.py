import redis
from redis_benchmarker.executors import BaseQueryExecutor, enable_auto_main
from redis_benchmarker.utils import time_operation
import numpy as np
from redisvl.index import SearchIndex
from redisvl.query import VectorQuery, FilterQuery
from redisvl.query.filter import Tag, Num

class BenchmarkVL(BaseQueryExecutor):
    def prepare(self, redis_client: redis.Redis) -> None:
        self.index = SearchIndex.from_existing(self.config.index_name or "redisvl", redis_client=redis_client)

    def execute_query(self, redis_client: redis.Redis) -> dict:
        num_results = self.config.num_results or 3
        vector_data = self.get_vector_from_pool()
        result = None
        with time_operation() as latency_ms:
            query = VectorQuery(
                vector=vector_data,
                vector_field_name="vector",
                num_results=num_results,
                return_fields=["id"],
                return_score=True,
            )
            result = self.index.query(query)

        return {
            "result": result,
            "latency_ms": float(latency_ms),
            "metadata": {
                "query_type": "vector_search",
                "total_results": len(result)
            }
        }

# This one line enables full CLI functionality
enable_auto_main(__name__)