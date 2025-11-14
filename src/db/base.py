from sqlalchemy.orm import declarative_base

# This file's ONLY job is to create and export the Base class.
# It should not import any models that depend on this Base.
Base = declarative_base()
# This will be the base for project and task mdoels
