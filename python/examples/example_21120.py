# 📖 Chapter: Appendices
# 📖 Section: E.3 Performance Tuning Guide

# Profile request performance
import time

start_time = time.time()
result = client.call_tool("tool_name", {})
duration = time.time() - start_time

if duration > 1.0:  # Log slow requests
    logger.warning(f"Slow request: {duration}s")