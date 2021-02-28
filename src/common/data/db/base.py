#!/usr/bin/env python3

from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


class BaseTable(DeclarativeBase):  # type: ignore

    created_at = Column("created_at",
                        DateTime,
                        server_default=func.now())

    updated_at = Column("updated_at",
                        DateTime,
                        onupdate=func.now())

    __abstract__ = True
