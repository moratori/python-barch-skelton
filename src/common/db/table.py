#!/usr/bin/env python

from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SomethingTable(Base):  # type: ignore

    __tablename__ = "something_table"

    some_id = Column("some_id",
                     String(128),
                     primary_key=True,
                     nullable=False)

    some_value = Column("some_value",
                        String(512),
                        primary_key=False,
                        nullable=False)


class Foobar(Base):  # type: ignore

    __tablename__ = "foobar"

    some_id = Column("some_id",
                     String(128),
                     primary_key=True,
                     nullable=False)
