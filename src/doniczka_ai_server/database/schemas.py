from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


class ViewBase(DeclarativeBase):
    """Base for read-only models mapped onto database views (e.g. TimescaleDB
    continuous aggregates). It has its own MetaData, so these models are
    ignored by `Base.metadata.create_all()` and by Alembic autogenerate.
    The views themselves are created in Alembic migrations."""

    pass
