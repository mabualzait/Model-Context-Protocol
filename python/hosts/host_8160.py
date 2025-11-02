# 📖 Chapter: Chapter 6: The Host: Orchestrating MCP Sessions
# 📖 Section: 6.5 Advanced Host Patterns

class HighAvailabilityMCPHost(MCPHost):
    """Host with high availability and failover."""
    
    def __init__(self):
        super().__init__()
        self.primary_servers: Dict[str, str] = {}
        self.backup_servers: Dict[str, List[str]] = {}
        self.server_health: Dict[str, bool] = {}
        self.health_check_interval = 30
        self.health_check_thread = None
    
    def register_server_with_backup(self, server_id: str, primary_config: Dict, backup_configs: List[Dict]):
        """Register server with backup instances."""
        self.primary_servers[server_id] = primary_config
        self.backup_servers[server_id] = backup_configs
        self.server_health[server_id] = True
    
    def start_health_monitoring(self):
        """Start health monitoring thread."""
        def health_check_loop():
            while True:
                self._check_server_health()
                time.sleep(self.health_check_interval)
        
        self.health_check_thread = threading.Thread(target=health_check_loop, daemon=True)
        self.health_check_thread.start()
    
    def _check_server_health(self):
        """Check health of all servers."""
        for server_id in self.primary_servers.keys():
            try:
                # Check primary server
                health = self._check_server_health_single(server_id, self.primary_servers[server_id])
                self.server_health[server_id] = health
                
                # If primary is down, try to promote backup
                if not health and server_id in self.backup_servers:
                    self._promote_backup(server_id)
            except Exception as e:
                logger.error(f"Health check failed for {server_id}: {e}")
                self.server_health[server_id] = False
    
    def _check_server_health_single(self, server_id: str, config: Dict) -> bool:
        """Check health of a single server."""
        try:
            # Create temporary connection for health check
            if config.get("transport") == "stdio":
                connection = StdioServerConnection(config["command"])
            else:
                connection = HTTPServerConnection(config["url"])
            
            # Try to initialize (health check)
            connection.initialize({
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "health-check", "version": "1.0.0"}
            })
            
            connection.close()
            return True
        except Exception:
            return False
    
    def _promote_backup(self, server_id: str):
        """Promote backup server to primary."""
        if server_id not in self.backup_servers:
            return
        
        backups = self.backup_servers[server_id]
        for backup_config in backups:
            if self._check_server_health_single(server_id, backup_config):
                # Promote this backup to primary
                self.primary_servers[server_id] = backup_config
                self.server_health[server_id] = True
                logger.info(f"Promoted backup server for {server_id}")
                return
    
    def route_request(self, session_id: str, request: Dict) -> Dict:
        """Route request with failover."""
        session = self.get_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        # Determine target server
        server_id = self._determine_server(session, request)
        
        # Try primary first
        try:
            if self.server_health.get(server_id, False):
                config = self.primary_servers[server_id]
                connection = self._create_connection(config)
                return connection.send_request(request)
        except Exception as e:
            logger.warning(f"Primary server failed for {server_id}: {e}")
            self.server_health[server_id] = False
        
        # Try backups
        if server_id in self.backup_servers:
            for backup_config in self.backup_servers[server_id]:
                try:
                    connection = self._create_connection(backup_config)
                    response = connection.send_request(request)
                    
                    # Backup worked, optionally promote it
                    if self._check_server_health_single(server_id, backup_config):
                        self.primary_servers[server_id] = backup_config
                        self.server_health[server_id] = True
                    
                    return response
                except Exception as e:
                    logger.warning(f"Backup server failed for {server_id}: {e}")
                    continue
        
        raise RuntimeError(f"All servers unavailable for {server_id}")