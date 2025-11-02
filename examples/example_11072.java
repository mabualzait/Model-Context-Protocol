# 📖 Chapter: Chapter 8: Integrating MCP into Applications
# 📖 Section: 8.2 IDE Integrations

import com.intellij.openapi.application.ApplicationManager;
import com.intellij.openapi.project.Project;
import org.jetbrains.annotations.NotNull;

public class MCPPlugin implements com.intellij.openapi.components.ApplicationComponent {
    private MCPClient mcpClient;
    
    @Override
    public void initComponent() {
        // Initialize MCP client
        mcpClient = new MCPClient(
            new ProcessBuilder("python", "-m", "filesystem-server")
        );
        
        try {
            mcpClient.connect();
        } catch (Exception e) {
            // Handle connection error
        }
    }
    
    public void addMCPActions(Project project) {
        // Add MCP-based actions to IDE
        ApplicationManager.getApplication().executeOnPooledThread(() -> {
            List<Tool> tools = mcpClient.listTools();
            
            for (Tool tool : tools) {
                // Register tool as IDE action
                registerToolAction(project, tool);
            }
        });
    }
}