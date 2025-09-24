import logging
from logging.config import fileConfig
import os # Import os

from flask import current_app

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')


def get_engine():
    try:
        # this works with Flask-SQLAlchemy<3 and Alchemical
        return current_app.extensions['migrate'].db.get_engine()
    except TypeError:
        # this works with Flask-SQLAlchemy>=3
        return current_app.extensions['migrate'].db.engine


def get_engine_url():
    try:
        # Try to get URL from current_app first
        return get_engine().url.render_as_string(hide_password=False).replace(
            '%', '%%')
    except (AttributeError, RuntimeError): # Catch RuntimeError if current_app is not available
        # Fallback to environment variable
        return os.environ.get('DATABASE_URL', 'postgresql+pg8000://user:password@localhost/kwikconnect').replace('%', '%%')


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
config.set_main_option('sqlalchemy.url', get_engine_url())
# Only try to get target_db if current_app is available
if current_app:
    target_db = current_app.extensions['migrate'].db
else:
    # If current_app is not available, we need to import models directly
    # This is a simplified approach, for a more robust solution,
    # you might need to create a minimal app context here.
    from backend.models import User, Vendor, Product, Courier, Order, OrderItem, Errand, Wallet, Transaction, TokenBlocklist
    from backend import db # Import db from backend
    target_metadata = db.metadata # Assuming db is imported from backend

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_metadata():
    if current_app:
        if hasattr(target_db, 'metadatas'):
            return target_db.metadatas[None]
        return target_db.metadata
    else:
        # If current_app is not available, return the metadata from the imported db object
        from backend import db # Import db from backend
        return db.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=get_metadata(), literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # this callback is used to prevent an auto-migration from being generated
    # when there are no changes to the schema
    # reference: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            process_revision_directives=process_revision_directives,
            **current_app.extensions['migrate'].configure_args
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
