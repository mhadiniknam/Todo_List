# ToDo List CLI Application

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A robust, command-line interface (CLI) application for managing projects and their associated tasks, built with a clean, layered architecture in Python. The application features an interactive REPL (Read-Eval-Print Loop) and an integrated background scheduler for automated task management.

## Features

- **Project & Task Management**: Full CRUD (Create, Read, Update, Delete) operations for both projects and tasks.
- **Interactive CLI**: A user-friendly REPL for managing your workflow in real-time.
- **Persistent Storage**: Uses a PostgreSQL database to ensure your data is always saved.
- **Database Migrations**: Powered by `Alembic` for safe and version-controlled schema changes.
- **Automated Overdue Task Management**: An integrated background scheduler (`schedule` library running in a separate thread) automatically checks for and closes tasks that are past their deadline.
- **Clean Architecture**: Built with a clear separation of concerns into three layers:
    1.  **CLI (Presentation Layer)**: Handles user input and displays output.
    2.  **Service Layer**: Contains all business logic and validation rules.
    3.  **Repository Layer**: Manages all data access and communication with the database.

## Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management.
- [Docker](https://www.docker.com/products/docker-desktop/) for running the database.

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

2.  **Install Python dependencies:**
    Poetry will create a virtual environment and install all necessary packages.
    ```bash
    poetry install
    ```

3.  **Set up environment variables:**
    Create a `.env` file in the project root.
    ```bash
    cp .env.example .env
    ```
    Now, **edit the `.env` file** to match the database credentials you will use in the Docker command below:
    ```ini
    DB_USER=hadi
    DB_PASSWORD=12345678
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=mydb
    ```

### Database Setup with Docker

1.  **Run the PostgreSQL Container:**
    Open your terminal and run the following command. This will download the official PostgreSQL image, start a container in the background, and configure it with your credentials.

    ```bash
    docker run -d --name todolist-db -e POSTGRES_USER=hadi -e POSTGRES_PASSWORD=12345678 -e POSTGRES_DB=mydb -p 5432:5432 -v todolist_data:/var/lib/postgresql/data postgres
    ```
    *Note: The `-v todolist_data:/var/lib/postgresql/data` flag is crucial. It saves your database data to your local machine, so it isn't lost if the container is removed.*

2.  **To stop and remove the container:**
    ```bash
    docker stop todolist-db
    docker rm todolist-db
    ```

### Final Step: Run Database Migrations

Once your database container is running, initialize the schema using Alembic. This will create all the necessary tables.

```bash
poetry run alembic upgrade head
```

## Usage

To start the interactive command-line application, run:

```bash
poetry run python main.py
```

The application will start, and the background scheduler for closing overdue tasks will automatically begin its work. You will be greeted with a `>` prompt.