# We aim to build a base Class for our models to inherit from
# Declarative Base is the way we are mapping the Classes to table ,Base actually determine how we are building the tables


from sqlalchemy.orm import Declarative_base

class Base(Declarative_base):
    pass
