# 📖 Chapter: Chapter 3: MCP in the Ecosystem
# 📖 Section: 3.5 Detailed Platform Implementation Examples

// Zed's MCP integration (simplified)
use mcp::Client;

pub struct ZedMCPIntegration {
    client: Client,
    project_root: PathBuf,
}

impl ZedMCPIntegration {
    pub fn new(project_root: PathBuf) -> Result<Self, Error> {
        // Connect to file system MCP server
        let client = Client::new_stdio("mcp-filesystem-server")?;
        client.connect()?;
        
        Ok(Self {
            client,
            project_root,
        })
    }
    
    pub fn get_file_context(&self, file_path: &Path) -> Result<String, Error> {
        // Read file via MCP
        let uri = format!("file://{}", file_path.to_string_lossy());
        let content = self.client.read_resource(&uri)?;
        
        // Get related files for context
        let related_files = self.get_related_files(file_path)?;
        let related_content: Vec<String> = related_files
            .iter()
            .filter_map(|path| self.client.read_resource(&format!("file://{}", path.to_string_lossy())).ok())
            .collect();
        
        // Build context for AI
        let context = format!(
            "Current file:\n{}\n\nRelated files:\n{}",
            content,
            related_content.join("\n\n---\n\n")
        );
        
        Ok(context)
    }
    
    pub fn apply_ai_suggestion(&self, suggestion: CodeSuggestion) -> Result<(), Error> {
        // Use MCP tool to apply changes
        self.client.call_tool("write_file", json!({
            "path": suggestion.file_path.to_string_lossy(),
            "content": suggestion.new_content
        }))?;
        
        Ok(())
    }
    
    fn get_related_files(&self, file_path: &Path) -> Result<Vec<PathBuf>, Error> {
        // Use MCP to find related files (imports, tests, etc.)
        let imports = self.client.call_tool("find_imports", json!({
            "path": file_path.to_string_lossy()
        }))?;
        
        Ok(imports["files"].as_array()
            .unwrap()
            .iter()
            .filter_map(|v| v.as_str())
            .map(|s| PathBuf::from(s))
            .collect())
    }
}