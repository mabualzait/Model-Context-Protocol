# 📖 Chapter: Appendices
# 📖 Section: E.3 Performance Tuning Guide

# Batch multiple requests
operations = [
    {"method": "tools/call", "params": {"name": "tool1", "arguments": {}}},
    {"method": "tools/call", "params": {"name": "tool2", "arguments": {}}},
    {"method": "resources/read", "params": {"uri": "file://..."}}
]

results = client.batch_operations(operations)