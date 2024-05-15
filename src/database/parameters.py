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


def init_parameter_table(session=None):
    stmt = insert(parameter_table).values(
        minimum_age=18,
        maximum_age=55,
        maximum_account_age=6 * 31,  # 6 months
        maximum_publication_year_gab=8,  # in year
        maximum_lending_quantity=5,  # books
        maximum_lending_period=4,  # days
    )

    result = session.execute(stmt)


def get_parameter(param_name=None, session=None):
    stmt = select(parameter_table)

    result = session.execute(stmt).all()

    assert len(result) == 1

    result = result[0]._asdict()

    if param_name is not None:
        assert param_name in PARAM_NAMES
        return result[param_name]

    result.pop('id_lock', None)


    return result


def set_param(param_name, new_value, session=None):
    assert param_name in PARAM_NAMES

    stmt = update(parameter_table)
    session.execute(stmt, {param_name: new_value})
