# 📖 Chapter: Chapter 13: Multi-Agent Systems with MCP
# 📖 Section: 13.2 Agent-to-Agent Communication via MCP

class AgentCommunicationManager:
    """Manage communication between agents via MCP."""
    
    def __init__(self, orchestrator: MultiAgentOrchestrator):
        self.orchestrator = orchestrator
        self.message_queue: Dict[str, List[Dict]] = {}  # agent_id -> messages
        self.subscriptions: Dict[str, List[str]] = {}  # agent_id -> [subscribed_topics]
    
    def send_message(self, from_agent_id: str, to_agent_id: str, 
                    message: Dict, priority: str = "normal"):
        """Send message from one agent to another."""
        if to_agent_id not in self.message_queue:
            self.message_queue[to_agent_id] = []
        
        message_entry = {
            "from_agent_id": from_agent_id,
            "to_agent_id": to_agent_id,
            "message": message,
            "priority": priority,
            "timestamp": time.time(),
            "id": str(uuid.uuid4())
        }
        
        self.message_queue[to_agent_id].append(message_entry)
        
        # Sort by priority
        priority_order = {"high": 0, "normal": 1, "low": 2}
        self.message_queue[to_agent_id].sort(
            key=lambda x: (priority_order.get(x["priority"], 1), x["timestamp"])
        )
        
        # Notify receiving agent via MCP resource
        if to_agent_id in self.orchestrator.agent_connections:
            client = self.orchestrator.agent_connections[to_agent_id]
            try:
                # Use MCP notification mechanism
                client.notify_resource_change(f"message://{to_agent_id}/new")
            except:
                pass  # Agent may not support notifications
    
    def get_messages(self, agent_id: str, max_messages: int = None) -> List[Dict]:
        """Get messages for agent."""
        messages = self.message_queue.get(agent_id, [])
        
        if max_messages:
            messages = messages[:max_messages]
        
        # Remove retrieved messages
        if agent_id in self.message_queue:
            if max_messages:
                self.message_queue[agent_id] = self.message_queue[agent_id][max_messages:]
            else:
                self.message_queue[agent_id] = []
        
        return messages
    
    def subscribe_to_topic(self, agent_id: str, topic: str):
        """Subscribe agent to topic for pub/sub communication."""
        if agent_id not in self.subscriptions:
            self.subscriptions[agent_id] = []
        
        if topic not in self.subscriptions[agent_id]:
            self.subscriptions[agent_id].append(topic)
    
    def publish_to_topic(self, from_agent_id: str, topic: str, message: Dict):
        """Publish message to topic (pub/sub pattern)."""
        subscribers = [
            agent_id for agent_id, topics in self.subscriptions.items()
            if topic in topics
        ]
        
        for subscriber_id in subscribers:
            if subscriber_id != from_agent_id:
                self.send_message(from_agent_id, subscriber_id, message)
    
    def broadcast_message(self, from_agent_id: str, message: Dict,
                         filter_capabilities: List[str] = None):
        """Broadcast message to multiple agents."""
        recipients = []
        
        for agent_id, agent in self.orchestrator.agents.items():
            if agent_id == from_agent_id:
                continue
            
            if filter_capabilities:
                agent_capabilities = set(agent["capabilities"])
                required_set = set(filter_capabilities)
                if not required_set.issubset(agent_capabilities):
                    continue
            
            recipients.append(agent_id)
        
        # Send to all recipients
        for recipient_id in recipients:
            self.send_message(from_agent_id, recipient_id, message)
    
    def establish_direct_communication(self, agent1_id: str, agent2_id: str) -> Dict:
        """Establish direct communication channel between two agents."""
        # Create shared resource for communication
        channel_id = f"{agent1_id}_{agent2_id}"
        
        # Both agents can read/write to this channel
        return {
            "channel_id": channel_id,
            "resource_uri": f"agent://channel/{channel_id}",
            "agents": [agent1_id, agent2_id],
            "established_at": time.time()
        }