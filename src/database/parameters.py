from sqlalchemy import select, insert, null, update
import os
from hashlib import sha256

from .models import parameter_table
from .connection import Session

PARAM_NAMES = [
    "minimum_age",
    "maximum_age",
    "maximum_account_age",
    "maximum_publication_year_gab",
    "maximum_lending_quantity",
    "maximum_lending_period",
]

PARAM_DEFAULT_VALUES = [
    18,
    55,
    6 * 31,  # 6 months
    8,  # in year
    5,  # books
    4,  # days
]


def init_parameter_table(session=None):
    stmt = insert(parameter_table)

    result = session.execute(
        stmt,
        [
            {"parameter_name": p, "value": v}
            for p, v in zip(PARAM_NAMES, PARAM_DEFAULT_VALUES)
        ],
    )


def get_parameter(param_names=None, session=None):
    # return all if param_names is None
    stmt = select(parameter_table)

    if param_names is not None:
        stmt = stmt.filter(parameter_table.c.parameter_name.in_(param_names))

    result = session.execute(stmt).all()

    assert len(result) != 0

    return [i._asdict() for i in result]


def set_param(param_name, new_value, session=None):

    stmt = (
        update(parameter_table)
        .where(parameter_table.c.parameter_name == param_name)
        .values(value=new_value)
    )

    session.execute(stmt)
