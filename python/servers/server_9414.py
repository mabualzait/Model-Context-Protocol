# 📖 Chapter: Chapter 7: Building Your First MCP Server
# 📖 Section: 7.5 Testing and Debugging

import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import shutil

from my_mcp_server.resources import FileSystemResources
from my_mcp_server.tools import FileSystemTools

class TestFileSystemResources(unittest.TestCase):
    """Test file system resources."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.resources = FileSystemResources(self.temp_dir)
        
        # Create test files
        (Path(self.temp_dir) / "test.txt").write_text("Test content")
        (Path(self.temp_dir) / "subdir" / "nested.txt").mkdir(parents=True)
        (Path(self.temp_dir) / "subdir" / "nested.txt").write_text("Nested content")
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_list_resources(self):
        """Test listing resources."""
        resources = self.resources.list_resources()
        
        self.assertGreater(len(resources), 0)
        self.assertTrue(any(r.uri.startswith("file://") for r in resources))
    
    def test_read_resource(self):
        """Test reading resource."""
        uri = f"file://{Path(self.temp_dir) / 'test.txt'}"
        content = self.resources.read_resource(uri)
        
        self.assertEqual(content, "Test content")
    
    def test_read_resource_security(self):
        """Test resource access security."""
        # Try to access file outside root
        outside_path = Path(self.temp_dir).parent / "outside.txt"
        outside_path.write_text("Outside content")
        
        uri = f"file://{outside_path}"
        
        with self.assertRaises(PermissionError):
            self.resources.read_resource(uri)
        
        outside_path.unlink()

class TestFileSystemTools(unittest.TestCase):
    """Test file system tools."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.tools = FileSystemTools(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_read_file_tool(self):
        """Test read file tool."""
        test_file = Path(self.temp_dir) / "test.txt"
        test_file.write_text("Test content")
        
        result = self.tools.call_tool("read_file", {"path": "test.txt"})
        
        self.assertFalse(result["isError"])
        self.assertEqual(result["content"][0]["text"], "Test content")
    
    def test_write_file_tool(self):
        """Test write file tool."""
        result = self.tools.call_tool("write_file", {
            "path": "new_file.txt",
            "content": "New content"
        })
        
        self.assertFalse(result["isError"])
        
        # Verify file was created
        new_file = Path(self.temp_dir) / "new_file.txt"
        self.assertTrue(new_file.exists())
        self.assertEqual(new_file.read_text(), "New content")
    
    def test_list_directory_tool(self):
        """Test list directory tool."""
        (Path(self.temp_dir) / "file1.txt").touch()
        (Path(self.temp_dir) / "file2.txt").touch()
        
        result = self.tools.call_tool("list_directory", {"path": "."})
        
        self.assertFalse(result["isError"])
        self.assertIn("file1.txt", result["content"][0]["text"])
        self.assertIn("file2.txt", result["content"][0]["text"])

if __name__ == "__main__":
    unittest.main()