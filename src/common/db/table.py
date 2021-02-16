#!/usr/bin/env python

from sqlalchemy import Column, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Something(Base):  # type: ignore

    some_id = Column("some_id",
                     String(128),
                     primary_key=True,
                     nullable=False)

    some_value = Column("some_value",
                        String(512),
                        primary_key=False,
                        nullable=False)

    version = Column(BigInteger,
                     nullable=False)

    __tablename__ = "something_table"
    __mapper_args__ = {'version_id_col': version}


class Foobar(Base):  # type: ignore

    some_id = Column("some_id",
                     String(128),
                     primary_key=True,
                     nullable=False)

    version = Column(BigInteger,
                     nullable=False)

    __tablename__ = "foobar"
    __mapper_args__ = {'version_id_col': version}
