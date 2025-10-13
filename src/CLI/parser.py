import argparse
from src.Storage.Simple_Storage import SimpleStorage


class CLI:
    def __init__(self):
        self.storage = SimpleStorage()

        self.commands = {
            "help": self.show_help,
            "create-project": self.create_project,
            "edit-project": self.edit_project,
            "add-task": self.add_task,
            "list-projects": self.list_projects,
            "list-tasks": self.list_tasks,
            "delete-project": self.delete_project,
            "delete-task": self.delete_task,
            "update-task": self.update_task_status,
            "exit": self.exit_cli,
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
                    print(
                        f"Unknown command: {command}. Type 'help' for available commands."
                    )
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit.")
            except Exception as e:
                print(f"Error: {e}")

    def show_help(self, args):
        """Show available commands."""
        print("\nAvailable commands:")
        print("  create-project <name> <desc>                   - Create a new project")
        print("  edit-project <prev_name> <new_name> <new_desc> - Create a new project")
        print(
            "  add-task <project> <title> <desc> <deadline-ARB> <status>  - Add a task to a project"
        )
        print("  list-projects                                  - List all projects")
        print(
            "  list-tasks <project>                           - List tasks in a project"
        )
        print("  delete-project <project>                       - Delete a project")
        print("  delete-task <project> <task_id>                - Delete a task")
        print("  update-task <project> <task_id> <status>       - Update task status")
        print(
            "  help                                           - Show this help message"
        )
        print("  exit                                           - Exit the application")

    def create_project(self, args):
        """Create a new project."""
        if len(args) < 2:
            print("Usage: create-project <name> <desc>")
            return

        name = args[0]
        desc = args[1]
        try:
            self.storage.create_project(name, desc)
        except ValueError as e:
            print(f"❌ Error: {e}")

    def edit_project(self, args):
        """Create a new project."""
        if len(args) != 3:
            print("edit-project <prev_name> <new_name> <new_desc>")
            return

        prev_name = args[0]
        new_name = args[1]
        desc = args[2]

        try:
            self.storage.edit_project(prev_name, new_name, desc)
        except ValueError as e:
            print(f"❌ Error: {e}")

    def add_task(self, args):
        """Add a task to a project."""
        if len(args) < 4:
            print("Usage: add-task <project> <title> <desc> <deadline-ARB> <status>")
            return

        project_name = args[0]
        task_title = args[1]
        task_desc = args[2]
        task_deadline = args[3]
        if len(args) == 5:
            status = args[4]
        else:
            status = None

        try:
            self.storage.add_task(
                project_name, task_title, task_desc, task_deadline, status
            )
        except ValueError as e:
            print(f"❌ Error: {e}")

    def list_projects(self):
        pass

    def list_tasks(self):
        pass

    def delete_project(self, args):
        """Delete a project."""
        if len(args) < 1:
            print("Usage: delete-project <project>")
            return

        name = args[0]

        try:
            self.storage.delete_project(name)
        except ValueError as e:
            print(f"❌ Error: {e}")

    def delete_task(self):
        pass

    def update_task_status(self, args):
        if len(args) != 3:
            print("Usage: update-task <project> <task_title> <status>")
            return

        project_name = args[0]
        task_title = args[1]
        new_status = args[2]

        success = self.storage.update_task_status(project_name, task_title, new_status)
        if not success:
            print(f"❌ Failed to update task status.")


    def exit_cli(self, args):
        """Exit the REPL."""
        print("Goodbye!")
        exit(0)
