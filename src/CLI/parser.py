from db.session import get_db_session
from repositories.project_repository import ProjectRepository
from repositories.task_repository import TaskRepository
from services.project_service import ProjectService
from services.task_service import TaskService

class CLI:
    def __init__(self):
        # The CLI no longer knows about storage. It only knows command names.
        self.commands = {
            "create-project": self.create_project,
            "list-projects": self.list_projects,
            "edit-project": self.edit_project,
            "delete-project": self.delete_project,
            "create-task": self.create_task,
            "list-tasks": self.list_tasks_for_project,
            "edit-task": self.edit_task,
            "delete-task": self.delete_task,
            "help": self.show_help,
            "exit": self.exit_cli,
        }

    def start(self):
        """Start the REPL loop, setting up dependencies for each command."""
        print("=== ToDoList REPL v2.0 ===")
        print("Type 'help' for available commands or 'exit' to quit.")

        while True:
            try:
                command_input = input("\n> ").strip()
                if not command_input:
                    continue

                parts = command_input.split()
                command_name = parts[0].lower()
                args = parts[1:]

                if command_name in self.commands:
                    # This is the Dependency Injection!
                    # For each command, we create a new session and new services.
                    with get_db_session() as db:
                        # 1. Create Repositories
                        project_repo = ProjectRepository(db)
                        task_repo = TaskRepository(db)
                        # 2. Create Services
                        project_service = ProjectService(project_repo)
                        task_service = TaskService(task_repo, project_repo)
                        # 3. Call the command method, passing the services
                        self.commands[command_name](args, project_service, task_service)
                else:
                    print(f"Unknown command: {command_name}. Type 'help'.")
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit.")
            except ValueError as e:
                # Catch business errors from the service layer
                print(f"❌ Error: {e}")
            except Exception as e:
                # Catch unexpected errors
                print(f"An unexpected error occurred: {e}")

    # --- Command Methods ---
    # They now receive services as arguments and print results.

    def create_project(self, args, project_service: ProjectService, _):
        if len(args) != 2:
            print("Usage: create-project <name> <description>")
            return
        data = {"name": args[0], "description": args[1]}
        project = project_service.create_project(data)
        print(f"✅ Project '{project.name}' created successfully with ID: {project.id}")

    def list_projects(self, _, project_service: ProjectService, __):
        projects = project_service.list_projects()
        if not projects:
            print("No projects found.")
            return
        print("--- Projects ---")
        for p in projects:
            print(f"ID: {p.id} | Name: {p.name}")

    def edit_project(self, args, project_service: ProjectService, _):
        if len(args) != 3:
            print("Usage: edit-project <id> <new_name> <new_description>")
            return
        project_id = int(args[0])
        update_data = {"name": args[1], "description": args[2]}
        project = project_service.edit_project(project_id, update_data)
        print(f"✅ Project ID {project.id} updated to '{project.name}'.")

    def delete_project(self, args, project_service: ProjectService, _):
        if len(args) != 1:
            print("Usage: delete-project <id>")
            return
        project_id = int(args[0])
        project = project_service.delete_project(project_id)
        print(f"✅ Project '{project.name}' (ID: {project.id}) deleted.")

    def create_task(self, args, _, task_service: TaskService):
        if len(args) < 3:
            print("Usage: create-task <project_id> <title> <description> [deadline YYYY-MM-DD] [status]")
            return
        data = {
            "project_id": int(args[0]),
            "title": args[1],
            "description": args[2],
            "deadline": args[3] if len(args) > 3 else None,
            "status": args[4] if len(args) > 4 else "todo",
        }
        task = task_service.create_task(data)
        print(f"✅ Task '{task.title}' created for Project ID: {task.project_id}")

    def list_tasks_for_project(self, args, _, task_service: TaskService):
        if len(args) != 1:
            print("Usage: list-tasks <project_id>")
            return
        project_id = int(args[0])
        tasks = task_service.list_tasks_for_project(project_id)
        if not tasks:
            print(f"No tasks found for Project ID {project_id}.")
            return
        print(f"--- Tasks for Project ID {project_id} ---")
        for t in tasks:
            print(f"ID: {t.id} | Status: {t.status.upper()} | Title: {t.title}")

    def edit_task(self, args, _, task_service: TaskService):
        if len(args) != 5:
            print("Usage: edit-task <task_id> <new_title> <new_desc> <new_deadline> <new_status>")
            return
        task_id = int(args[0])
        update_data = {
            "title": args[1],
            "description": args[2],
            "deadline": args[3],
            "status": args[4],
        }
        task = task_service.edit_task(task_id, update_data)
        print(f"✅ Task ID {task.id} updated to '{task.title}'.")

    def delete_task(self, args, _, task_service: TaskService):
        if len(args) != 1:
            print("Usage: delete-task <task_id>")
            return
        task_id = int(args[0])
        task = task_service.delete_task(task_id)
        print(f"✅ Task '{task.title}' (ID: {task.id}) deleted.")
    
    def show_help(self, *args):
        print("\nAvailable commands:")
        print("  create-project <name> <description>             - Create a new project")
        print("  list-projects                                 - List all projects")
        print("  edit-project <id> <new_name> <new_desc>       - Edit a project by its ID")
        print("  delete-project <id>                           - Delete a project by its ID")
        print("  create-task <proj_id> <title> <desc> ...      - Add a task to a project")
        print("  list-tasks <proj_id>                          - List tasks in a project")
        print("  edit-task <task_id> <title> <desc> ...        - Edit a task by its ID")
        print("  delete-task <task_id>                         - Delete a task by its ID")
        print("  help                                          - Show this help message")
        print("  exit                                          - Exit the application")

    def exit_cli(self, *args):
        print("Goodbye!")
        exit(0)