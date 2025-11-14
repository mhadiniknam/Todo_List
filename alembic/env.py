import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from models.project import Project
from models.task import Task
from alembic import context

# --- THIS IS THE CRITICAL PART ---

# 1. ADD THE 'src' DIRECTORY TO THE PYTHON PATH
# This line is essential. It tells Python to look inside your 'src'
# folder, allowing it to find your 'db' and 'models' modules.
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# 2. IMPORT THE 'Base' OBJECT FROM YOUR APPLICATION
# This line imports the Base class from your db/base.py file. All of your
# models (Project, Task) are tied to this 'Base' object.
from db.base import Base

# --- END OF CRITICAL PART ---

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3. SET THE 'target_metadata'
# This is the most important line for autogeneration. It tells Alembic
# that the structure defined by your models (via Base.metadata) is the
# "target" state it should compare the database against.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.QueuePool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()