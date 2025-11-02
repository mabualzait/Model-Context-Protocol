# 📖 Chapter: Chapter 14: MCP and Enterprise Integration
# 📖 Section: 14.2 Legacy System Integration

from abc import ABC, abstractmethod
from typing import Dict, Any
import xml.etree.ElementTree as ET
import csv
import json

class LegacyAdapter(ABC):
    """Base class for legacy system adapters."""
    
    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to legacy system."""
        pass
    
    @abstractmethod
    def execute(self, operation: str, params: Dict) -> Dict:
        """Execute operation on legacy system."""
        pass
    
    @abstractmethod
    def disconnect(self):
        """Close connection to legacy system."""
        pass

class SOAPLegacyAdapter(LegacyAdapter):
    """Adapter for SOAP-based legacy systems."""
    
    def __init__(self, wsdl_url: str, namespace: str):
        self.wsdl_url = wsdl_url
        self.namespace = namespace
        self.client = None
    
    def connect(self) -> bool:
        """Connect to SOAP service."""
        try:
            # In production, use zeep or suds library
            # self.client = zeep.Client(wsdl=self.wsdl_url)
            self.client = MockSOAPClient(self.wsdl_url)
            return True
        except Exception as e:
            print(f"SOAP connection failed: {e}")
            return False
    
    def execute(self, operation: str, params: Dict) -> Dict:
        """Execute SOAP operation."""
        if not self.client:
            raise ConnectionError("Not connected to SOAP service")
        
        # Convert params to SOAP format
        soap_params = self._convert_to_soap(params)
        
        # Call SOAP method
        result = self.client.call(operation, soap_params)
        
        # Convert SOAP response to MCP format
        return self._convert_from_soap(result)
    
    def _convert_to_soap(self, params: Dict) -> Dict:
        """Convert MCP parameters to SOAP format."""
        # SOAP typically uses namespaced XML
        soap_params = {}
        for key, value in params.items():
            soap_key = f"{self.namespace}:{key}"
            soap_params[soap_key] = value
        return soap_params
    
    def _convert_from_soap(self, soap_result: Any) -> Dict:
        """Convert SOAP response to MCP format."""
        # Parse SOAP XML response
        if isinstance(soap_result, str):
            root = ET.fromstring(soap_result)
            return {"content": [{"type": "text", "text": ET.tostring(root, encoding='unicode')}]}
        return {"content": [{"type": "text", "text": json.dumps(soap_result)}]}
    
    def disconnect(self):
        """Disconnect from SOAP service."""
        self.client = None

class FileBasedLegacyAdapter(LegacyAdapter):
    """Adapter for file-based legacy systems."""
    
    def __init__(self, file_path: str, format: str = "csv"):
        self.file_path = file_path
        self.format = format
        self.data = None
    
    def connect(self) -> bool:
        """Load legacy file data."""
        try:
            if self.format == "csv":
                self.data = self._load_csv()
            elif self.format == "xml":
                self.data = self._load_xml()
            elif self.format == "json":
                self.data = self._load_json()
            return True
        except Exception as e:
            print(f"File load failed: {e}")
            return False
    
    def _load_csv(self) -> List[Dict]:
        """Load CSV file."""
        with open(self.file_path, 'r') as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    def _load_xml(self) -> Dict:
        """Load XML file."""
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        return self._xml_to_dict(root)
    
    def _load_json(self) -> Dict:
        """Load JSON file."""
        with open(self.file_path, 'r') as f:
            return json.load(f)
    
    def _xml_to_dict(self, element) -> Dict:
        """Convert XML element to dictionary."""
        result = {}
        for child in element:
            if len(child) == 0:
                result[child.tag] = child.text
            else:
                result[child.tag] = self._xml_to_dict(child)
        return result
    
    def execute(self, operation: str, params: Dict) -> Dict:
        """Execute operation on file data."""
        if operation == "read":
            return self._read_data(params)
        elif operation == "search":
            return self._search_data(params)
        elif operation == "filter":
            return self._filter_data(params)
        else:
            raise ValueError(f"Unknown operation: {operation}")
    
    def _read_data(self, params: Dict) -> Dict:
        """Read data from file."""
        limit = params.get("limit", 100)
        offset = params.get("offset", 0)
        
        data_slice = self.data[offset:offset+limit]
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(data_slice)
                }
            ]
        }
    
    def _search_data(self, params: Dict) -> Dict:
        """Search data in file."""
        search_field = params.get("field")
        search_value = params.get("value")
        
        results = [
            item for item in self.data
            if isinstance(item, dict) and item.get(search_field) == search_value
        ]
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(results)
                }
            ]
        }
    
    def _filter_data(self, params: Dict) -> Dict:
        """Filter data in file."""
        filters = params.get("filters", {})
        
        results = self.data
        for field, value in filters.items():
            results = [
                item for item in results
                if isinstance(item, dict) and item.get(field) == value
            ]
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(results)
                }
            ]
        }
    
    def disconnect(self):
        """Disconnect from file."""
        self.data = None

class LegacyAPIGateway:
    """Gateway for integrating legacy systems via MCP."""
    
    def __init__(self):
        self.legacy_endpoints: Dict[str, str] = {}
        self.adapters: Dict[str, LegacyAdapter] = {}
        self.connection_status: Dict[str, bool] = {}
    
    def register_adapter(self, system_name: str, adapter: LegacyAdapter):
        """Register adapter for legacy system."""
        self.adapters[system_name] = adapter
        
        # Attempt connection
        if adapter.connect():
            self.connection_status[system_name] = True
        else:
            self.connection_status[system_name] = False
            raise ConnectionError(f"Failed to connect to {system_name}")
    
    def call_legacy_system(self, system_name: str, operation: str, 
                          params: Dict) -> Dict:
        """Call legacy system through adapter."""
        if system_name not in self.adapters:
            raise ValueError(f"No adapter for system: {system_name}")
        
        if not self.connection_status.get(system_name):
            raise ConnectionError(f"System {system_name} is not connected")
        
        adapter = self.adapters[system_name]
        
        try:
            return adapter.execute(operation, params)
        except Exception as e:
            raise Exception(f"Legacy system operation failed: {e}")
    
    def list_legacy_systems(self) -> List[Dict]:
        """List available legacy systems."""
        return [
            {
                "system_name": name,
                "connected": self.connection_status.get(name, False),
                "adapter_type": type(adapter).__name__
            }
            for name, adapter in self.adapters.items()
        ]
    
    def reconnect(self, system_name: str) -> bool:
        """Reconnect to legacy system."""
        if system_name not in self.adapters:
            return False
        
        adapter = self.adapters[system_name]
        if adapter.connect():
            self.connection_status[system_name] = True
            return True
        else:
            self.connection_status[system_name] = False
            return False