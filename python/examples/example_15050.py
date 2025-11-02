# 📖 Chapter: Chapter 11: Monitoring and Observability
# 📖 Section: 11.4 Performance Profiling

import psutil
import os

class ResourceMonitor:
    """Monitor resource usage."""
    
    def __init__(self):
        self.process = psutil.Process(os.getpid())
    
    def get_cpu_usage(self) -> float:
        """Get CPU usage percentage."""
        return self.process.cpu_percent(interval=1)
    
    def get_memory_usage(self) -> Dict[str, float]:
        """Get memory usage."""
        memory_info = self.process.memory_info()
        return {
            "rss_mb": memory_info.rss / (1024 * 1024),
            "vms_mb": memory_info.vms / (1024 * 1024),
            "percent": self.process.memory_percent()
        }
    
    def get_network_stats(self) -> Dict:
        """Get network statistics."""
        net_io = psutil.net_io_counters()
        return {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv
        }
    
    def get_disk_usage(self) -> Dict:
        """Get disk usage."""
        disk_usage = psutil.disk_usage('/')
        return {
            "total_gb": disk_usage.total / (1024 ** 3),
            "used_gb": disk_usage.used / (1024 ** 3),
            "free_gb": disk_usage.free / (1024 ** 3),
            "percent": disk_usage.percent
        }