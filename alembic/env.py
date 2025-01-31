from __future__ import absolute_import
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from alembic import context
from sqlalchemy.orm import sessionmaker
from app.models.models import Base  # Import your models here

config = context.config

from logging.config import fileConfig
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    engine = create_engine(config.get_main_option("sqlalchemy.url"))
    connection = engine.connect()
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
