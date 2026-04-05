"""Prometheus-compatible metrics registry."""

import os
import resource
import time
from collections import defaultdict
from threading import Lock


class MetricsRegistry:
    def __init__(self) -> None:
        self._lock = Lock()
        self._start_time = time.time()
        self._request_count: int = 0
        self._error_count: int = 0
        self._cache_hits: int = 0
        self._cache_misses: int = 0
        self._latency_sum: float = 0.0
        self._active_requests: int = 0
        self._latency_by_endpoint: dict[str, list[float]] = defaultdict(list)
        self._last_cpu_time = time.process_time()
        self._last_wall_time = time.time()

    def inc_active_requests(self) -> None:
        with self._lock:
            self._active_requests += 1

    def dec_active_requests(self) -> None:
        with self._lock:
            self._active_requests = max(0, self._active_requests - 1)

    def inc_request(self, endpoint: str, latency_s: float, is_error: bool, cache_hit: bool | None = None) -> None:
        with self._lock:
            self._request_count += 1
            self._latency_sum += latency_s
            self._latency_by_endpoint[endpoint].append(latency_s)
            if is_error:
                self._error_count += 1
            if cache_hit is True:
                self._cache_hits += 1
            elif cache_hit is False:
                self._cache_misses += 1

    def render(self) -> str:
        with self._lock:
            now = time.time()
            uptime = now - self._start_time
            avg_latency = (self._latency_sum / self._request_count * 1000) if self._request_count else 0
            cpu_time = time.process_time()
            wall_delta = max(now - self._last_wall_time, 0.001)
            cpu_delta = max(cpu_time - self._last_cpu_time, 0.0)
            cpu_percent = (cpu_delta / wall_delta) * 100
            self._last_cpu_time = cpu_time
            self._last_wall_time = now

            memory_bytes = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            if os.name != "posix":
                memory_bytes = int(memory_bytes)
            else:
                memory_bytes = int(memory_bytes * 1024)

            lines = [
                f"# HELP llm_gateway_up Whether the service is running",
                f"# TYPE llm_gateway_up gauge",
                f'llm_gateway_up{{service="llm-gateway"}} 1',
                f"",
                f"# HELP llm_gateway_uptime_seconds Seconds since start",
                f"# TYPE llm_gateway_uptime_seconds counter",
                f"llm_gateway_uptime_seconds {uptime:.1f}",
                f"",
                f"# HELP llm_gateway_requests_total Total requests processed",
                f"# TYPE llm_gateway_requests_total counter",
                f"llm_gateway_requests_total {self._request_count}",
                f"",
                f"# HELP llm_gateway_errors_total Total error responses",
                f"# TYPE llm_gateway_errors_total counter",
                f"llm_gateway_errors_total {self._error_count}",
                f"",
                f"# HELP llm_gateway_cache_hits_total Cache hits",
                f"# TYPE llm_gateway_cache_hits_total counter",
                f"llm_gateway_cache_hits_total {self._cache_hits}",
                f"",
                f"# HELP llm_gateway_cache_misses_total Cache misses",
                f"# TYPE llm_gateway_cache_misses_total counter",
                f"llm_gateway_cache_misses_total {self._cache_misses}",
                f"",
                f"# HELP llm_gateway_request_latency_ms_avg Average request latency",
                f"# TYPE llm_gateway_request_latency_ms_avg gauge",
                f"llm_gateway_request_latency_ms_avg {avg_latency:.2f}",
                f"",
                f"# HELP llm_gateway_active_requests Current in-flight requests",
                f"# TYPE llm_gateway_active_requests gauge",
                f"llm_gateway_active_requests {self._active_requests}",
                f"",
                f"# HELP llm_gateway_process_memory_bytes Resident memory usage",
                f"# TYPE llm_gateway_process_memory_bytes gauge",
                f"llm_gateway_process_memory_bytes {memory_bytes}",
                f"",
                f"# HELP llm_gateway_process_cpu_percent Process CPU percent",
                f"# TYPE llm_gateway_process_cpu_percent gauge",
                f"llm_gateway_process_cpu_percent {cpu_percent:.2f}",
                f"",
            ]

            for endpoint, latencies in self._latency_by_endpoint.items():
                if latencies:
                    p95 = sorted(latencies)[int(len(latencies) * 0.95)] * 1000
                    lines.extend([
                        f"# HELP llm_gateway_request_latency_ms_p95 P95 latency for {endpoint}",
                        f"# TYPE llm_gateway_request_latency_ms_p95 gauge",
                        f'llm_gateway_request_latency_ms_p95{{endpoint="{endpoint}"}} {p95:.2f}',
                        f"",
                    ])

            return "\n".join(lines)


registry = MetricsRegistry()
