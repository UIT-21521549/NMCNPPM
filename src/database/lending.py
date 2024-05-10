from sqlalchemy import select, insert, null
from .connection import Session

from .models import (
    lending_table,
    LendingStatus,
    lending_detail_table,
    fines_collection_table,
)





