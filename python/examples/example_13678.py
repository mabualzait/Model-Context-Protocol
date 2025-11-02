# 📖 Chapter: Chapter 10: Security Considerations in MCP
# 📖 Section: 10.2 Identity Fragmentation and Mitigation

# Problematic: Each server has separate identity
server1_auth = authenticate_to_server1(user_id)  # Identity A
server2_auth = authenticate_to_server2(user_id)  # Identity B (different)
server3_auth = authenticate_to_server3(user_id)  # Identity C (different)

# No way to track that these are the same user