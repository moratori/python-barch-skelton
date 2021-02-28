#!/usr/bin/env python3

from sqlalchemy import Column, String, BigInteger
from common.data.db.base import BaseTable


class Something(BaseTable):  # type: ignore

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

    __tablename__ = "something"
    __mapper_args__ = {'version_id_col': version}
