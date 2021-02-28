#!/usr/bin/env python3

from sqlalchemy import Column, String, BigInteger, ForeignKey
from common.data.db.base import BaseTable
from common.data.db.Something import Something


class Foobar(BaseTable):  # type: ignore

    some_id = Column("some_id",
                     String(128),
                     ForeignKey(Something.some_id),
                     primary_key=True,
                     nullable=False)

    version = Column(BigInteger,
                     nullable=False)

    __tablename__ = "foobar"
    __mapper_args__ = {'version_id_col': version}
