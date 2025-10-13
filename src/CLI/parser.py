import argparse
from src.Storage.Simple_Storage import SimpleStorage

class CLI:
    def __init__(self):
        self.storage = SimpleStorage()

        self.commands = {
            'help': self.show_help,
            'create-project': self.create_project,
            'add-task': self.add_task,
            'list-projects': self.list_projects,
            'list-tasks': self.list_tasks,
            'delete-project': self.delete_project,
            'delete-task': self.delete_task,
            'update-task': self.update_task_status,
            'exit': self.exit_cli
        }
    
    def start(self):
        """Start the REPL."""
        print("=== ToDoList REPL ===")
        print("Type 'help' for available commands or 'exit' to quit.")
        
        while True:
            try:
                command_input = input("\n> ").strip()
                if not command_input:
                    continue
                
                parts = command_input.split()
                command = parts[0].lower()
                args = parts[1:]
                
                if command in self.commands:
                    self.commands[command](args)
                else:
                    print(f"Unknown command: {command}. Type 'help' for available commands.")
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit.")
            except Exception as e:
                print(f"Error: {e}")
    
    def show_help(self,args):
        """Show available commands."""
        print("\nAvailable commands:")
        print("  create-project <name>              - Create a new project")
        print("  add-task <project> <title> <desc>  - Add a task to a project")
        print("  list-projects                      - List all projects")
        print("  list-tasks <project>               - List tasks in a project")
        print("  delete-project <project>           - Delete a project")
        print("  delete-task <project> <task_id>    - Delete a task")
        print("  update-task <project> <task_id> <status> - Update task status")
        print("  help                               - Show this help message")
        print("  exit                               - Exit the application")

    def create_project(self, args):
        """Create a new project."""
        if len(args) < 1:
            print("Usage: create-project <name>")
            return
        
        name = ' '.join(args)
        try:
            if self.storage.create_project(name):
                print(f"✅ Project '{name}' created successfully.")
            else:
                print(f"❌ Project '{name}' already exists.")
        except ValueError as e:
            print(f"❌ Error: {e}")

    def add_task(self):
        pass
    
    def list_projects(self):
        pass

    def list_tasks(self):
        pass
    
    def delete_project(self):
        pass

    def delete_task(self):
        pass
    
    def update_task_status(self):
        pass

    def exit_cli(self,args):
        """Exit the REPL."""
        print("Goodbye!")
        exit(0)