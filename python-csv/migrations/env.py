from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Этот файл будет импортировать ваше приложение/модель
# и применять миграции с использованием его метаданных.
# Замените `myapp.models` на модуль, содержащий ваши модели.
from models import *

# Конфигурируем Alembic
config = context.config

# Если у вас есть файл конфигурации логирования,
# это позволит Alembic использовать ту же конфигурацию.
if config.config_file_name:
    fileConfig(config.config_file_name)

# 'target_metadata' - это объект метаданных вашей базы данных,
# который будет использоваться Alembic.
# Установите его равным метаданным вашего приложения.
# Например: target_metadata = Base.metadata
target_metadata = Base.metadata

# Используем ваше подключение SQLAlchemy для создания движка
# и ассоциируем его с контекстом Alembic.
engine = engine_from_config(
    config.get_section(config.config_ini_section),
    prefix='sqlalchemy.',
    poolclass=pool.NullPool
)
connection = engine.connect()
context.configure(
    connection=connection,
    target_metadata=target_metadata
)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=config.get_main_option('sqlalchemy.url'),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()