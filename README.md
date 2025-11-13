# ToDo List CLI Application

A simple command-line based ToDo List manager to create projects, add tasks, and manage work effectively from the terminal.

## Features

- Create, edit, and delete projects with descriptions.
- Add, edit, update status, and delete tasks associated with projects.
- View all projects with project IDs, names, and descriptions.
- List all tasks in a project with their IDs, titles, statuses, and deadlines.
- Enforce limits on the number of projects and tasks (configurable via `.env`).
- Validate inputs including task statuses, string lengths, and deadline formats.
- User-friendly interactive REPL interface with helpful command list.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/todo-list-cli.git
cd todo-list-cli
```

2. Install dependencies (if any):

```bash
pip install -r requirements.txt
```

3. Create a `.env` file with environment variables:

```
MAX_NUMBER_OF_PROJECT=10
MAX_NUMBER_OF_TASK=50
```

4. Run the CLI application:

```bash
python main.py
```

## Usage

Start the application, then use commands such as:

- `create-project <name> <description>` - Create a new project.
- `edit-project <old_name> <new_name> <new_description>` - Edit project details.
- `delete-project <name>` - Delete a project.
- `add-task <project> <title> <description> <deadline> <status>` - Add a task.
- `edit-task <project> <task_title> <new_title> <new_description> <deadline> <status>` - Edit a task.
- `delete-task <project> <task_title>` - Delete a task.
- `list-projects` - List all projects.
- `list-tasks <project>` - List all tasks in a project.
- `update-task <project> <task_title> <status>` - Update task status.
- `help` - Display available commands.
- `exit` - Exit the application.

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements.

## License

This project is licensed under the MIT License.

***

This README covers installation, usage, feature summary, and contribution guidelines — all in a clean, engaging format suitable for GitHub or other repos. Let me know if you want it customized further. 

### Check the PEP8 structure with

```
poetry run flake8 src/
```

To automaticly align the coding Structure of the project 
```
poetry run black src
```