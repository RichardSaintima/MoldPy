import os

def crear_alembic_files(target_path: str):
    """Genera la configuración de Alembic (alembic.ini, alembic/env.py y alembic/script.py.mako)."""
    
    # 1. Crear alembic.ini
    with open(os.path.join(target_path, "alembic.ini"), "w", encoding="utf-8") as f:
        f.write(
            '[alembic]\n'
            'script_location = alembic\n'
            'prepend_sys_path = .\n'
            'version_locations = %(here)s/alembic/versions\n\n'
            '[loggers]\nkeys = root,sentry,alembic,sqlalchemy\n\n'
            '[handlers]\nkeys = console\n\n'
            '[formatters]\nkeys = generic\n\n'
            '[logger_root]\nlevel = WARN\nhandlers = console\n\n'
            '[logger_sentry]\nlevel = WARN\nhandlers = console\nqualname = sentry\n\n'
            '[logger_alembic]\nlevel = INFO\nhandlers = console\nqualname = alembic\n\n'
            '[logger_sqlalchemy]\nlevel = WARN\nhandlers = console\nqualname = sqlalchemy.engine\n\n'
            '[handler_console]\nclass = StreamHandler\nargs = (sys.stderr,)\nlevel = NOTSET\nformatter = generic\n\n'
            '[formatter_generic]\nformat = %(levelname)-5.5s [%(name)s] %(message)s\ndatefmt = %H:%M:%S\n'
        )

    # 2. Crear carpetas alembic/ y alembic/versions/
    alembic_dir = os.path.join(target_path, "alembic")
    versions_dir = os.path.join(alembic_dir, "versions")
    os.makedirs(versions_dir, exist_ok=True)

    # 3. Crear alembic/env.py
    with open(os.path.join(alembic_dir, "env.py"), "w", encoding="utf-8") as f:
        f.write(
            'import os\n'
            'import sys\n'
            'from logging.config import fileConfig\n'
            'from sqlalchemy import engine_from_config, pool\n'
            'from alembic import context\n'
            'from sqlmodel import SQLModel\n\n'
            'sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))\n\n'
            'from app.config import DATABASE_URL\n'
            'import app.models\n\n'
            'config = context.config\n'
            'if config.config_file_name:\n'
            '    fileConfig(config.config_file_name)\n\n'
            'target_metadata = SQLModel.metadata\n\n'
            'def run_migrations_offline() -> None:\n'
            '    url = DATABASE_URL\n'
            '    context.configure(\n'
            '        url=url,\n'
            '        target_metadata=target_metadata,\n'
            '        literal_binds=True,\n'
            '        dialect_opts={"paramstyle": "named"},\n'
            '    )\n'
            '    with context.begin_transaction():\n'
            '        context.run_migrations()\n\n'
            'def run_migrations_online() -> None:\n'
            '    configuration = config.get_section(config.config_ini_section) or {}\n'
            '    configuration["sqlalchemy.url"] = DATABASE_URL\n'
            '    connectable = engine_from_config(\n'
            '        configuration,\n'
            '        prefix="sqlalchemy.",\n'
            '        poolclass=pool.NullPool,\n'
            '    )\n'
            '    with connectable.connect() as connection:\n'
            '        context.configure(connection=connection, target_metadata=target_metadata)\n'
            '        with context.begin_transaction():\n'
            '            context.run_migrations()\n\n'
            'if context.is_offline_mode():\n'
            '    run_migrations_offline()\n'
            'else:\n'
            '    run_migrations_online()\n'
        )

    # 4. Crear alembic/script.py.mako corregido
    mako_content = """\"\"\"${message}

Revision ID: ${up_revision}
Revises: ${down_revision | repr, n}
Create Date: ${create_date}

\"\"\"
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlmodel
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
"""

    with open(os.path.join(alembic_dir, "script.py.mako"), "w", encoding="utf-8") as f:
        f.write(mako_content)