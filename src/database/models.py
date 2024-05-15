from sqlalchemy import MetaData, UniqueConstraint, ForeignKeyConstraint, CheckConstraint
from sqlalchemy import (
    Table,
    Column,
    Integer,
    Boolean,
    String,
    ForeignKey,
    DateTime,
    Enum,
    Float,
)
import enum
from sqlalchemy.sql import func

metadata_obj = MetaData()

# Thẻ Độc giả
user_table = Table(
    "user",
    metadata_obj,
    Column("user_id", Integer, primary_key=True),
    Column(
        "reader_type_id",
        Integer,
        ForeignKey("reader_type.reader_type_id"),
        nullable=True,
    ),
    # login with email and password
    Column("email", String, nullable=False, unique=True),
    Column("password_hash", String, nullable=False),
    Column("birthday", DateTime),
    Column("address", String),
    # multiple users could have the same name
    Column("user_name", String(30)),
    Column("is_admin", Boolean, default=False, nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
    Column("expiry_date", DateTime),
    Column("penalty_owed", Integer, CheckConstraint("penalty_owed>=0"), default=0),
)

# Loại độc giả
reader_type_table = Table(
    "reader_type",
    metadata_obj,
    Column("reader_type_id", Integer, primary_key=True),
    Column("reader_type", String, nullable=False),  # Loại độc giả X,Y
    UniqueConstraint("reader_type"),
)


# Thông Tin Tựa Sách
book_title_table = Table(
    "book_title",
    metadata_obj,
    Column("book_title_id", Integer, primary_key=True),
    Column("book_name", String(30), nullable=False),
    Column("genre_id", Integer, ForeignKey("book_genre.genre_id"), nullable=False),
    Column(
        "image_id",
        Integer,
        ForeignKey("image_path.image_id", ondelete="SET NULL", onupdate="CASCADE"),
    ),
)

# Thể loại Sách
book_genre_table = Table(
    "book_genre",
    metadata_obj,
    Column("genre_id", Integer, primary_key=True),
    Column("genre_name", String(30), nullable=False, unique=True),
    UniqueConstraint("genre_name"),
)

author_table = Table(
    "author",
    metadata_obj,
    Column("author_id", Integer, primary_key=True),
    Column("author_name", String(30), nullable=False, unique=True),
)


book_author_list = Table(
    "author_list",
    metadata_obj,
    Column(
        "book_title_id",
        Integer,
        ForeignKey("book_title.book_title_id"),
        primary_key=True,
    ),
    Column("author_id", Integer, ForeignKey("author.author_id"), primary_key=True),
)

publisher_table = Table(
    "publisher",
    metadata_obj,
    Column("publisher_id", Integer, primary_key=True),
    Column("publisher_name", String(30), nullable=False),
)

book_table = Table(
    "book",
    metadata_obj,
    Column("book_id", Integer, primary_key=True),
    Column(
        "book_title_id", Integer, ForeignKey("book_title.book_title_id"), nullable=False
    ),
    Column(
        "publication_year",
        Integer,
        CheckConstraint("publication_year>=1"),
        nullable=False,
    ),
    Column(
        "publisher_id", Integer, ForeignKey("publisher.publisher_id"), nullable=False
    ),
    Column("price", Integer, CheckConstraint("price>=1"), nullable=False),
    Column(
        "quantity", Integer, CheckConstraint("quantity>=0"), nullable=False, default=0
    ),
    Column(
        "available", Integer, CheckConstraint("available>=0"), nullable=False, default=0
    ),
)


book_receipt_table = Table(
    "book_receipt",
    metadata_obj,
    Column("book_receipt_id", Integer, primary_key=True),
    Column("entry_date", DateTime, nullable=False, server_default=func.now()),
)


book_receipt_detail_table = Table(
    "book_receipt_detail",
    metadata_obj,
    Column(
        "book_receipt_id",
        Integer,
        ForeignKey("book_receipt.book_receipt_id"),
        primary_key=True,
    ),
    Column("book_id", Integer, ForeignKey("book.book_id"), primary_key=True),
    Column("quantity", Integer, CheckConstraint("quantity>0"), nullable=False),
)

lending_table = Table(
    "lending",
    metadata_obj,
    Column("lending_id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.user_id"), nullable=False),
    Column("lending_date", DateTime, nullable=False, server_default=func.now()),
    Column("return_deadline", DateTime),  # hạn trả sách
    Column("return_date", DateTime),
    Column("penalty", Integer, default=0),  # số tiền phạt
    Column(
        "lending_lock", Boolean, default=True, unique=True, nullable=True
    ),  # chỉ 1 row có lending_lock là True (còn lại là Null)
    Column(
        "returned_lock",
        Integer,
        CheckConstraint("returned_lock>=0 and returned_lock<=1"),
        default=0,
    ),  # chỉ trả sách được 1 lần
)

# class LendingStatus(enum.Enum):
#     returned = 0
#     lost = 1
#     lended = 2


lending_detail_table = Table(
    "lending_detail",
    metadata_obj,
    Column("lending_id", Integer, ForeignKey("lending.lending_id"), primary_key=True),
    Column("book_id", Integer, ForeignKey("book.book_id"), primary_key=True),
    Column("quantity", Integer, nullable=False),
)


fines_collection_table = Table(
    "fines_collection",
    metadata_obj,
    Column("fine_collection_id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.user_id"), nullable=False),
    Column("amount", Integer, CheckConstraint("amount>0"), nullable=False),
)

report_by_genre_table = Table(
    "report_by_genre",
    metadata_obj,
    Column("report_id", Integer, primary_key=True),
    Column("report_date", DateTime),
)

report_by_genre_detail_table = Table(
    "report_by_genre_detail",
    metadata_obj,
    Column(
        "report_id", Integer, ForeignKey("report_by_genre.report_id"), primary_key=True
    ),
    Column("genre_id", Integer, ForeignKey("book_genre.genre_id"), primary_key=True),
    Column("lending_quantity", Integer, nullable=False),
    Column("ratio", Float, nullable=False),
)


late_return_report_table = Table(
    "late_return_report",
    metadata_obj,
    Column("report_id", Integer, primary_key=True),
    Column("report_date", DateTime),
)

late_return_report_detail_table = Table(
    "late_return_report_detail",
    metadata_obj,
    Column("report_id", Integer, ForeignKey("book.book_id"), primary_key=True),
    Column("book_id", Integer, ForeignKey("book.book_id"), primary_key=True),
    Column("lending_id", Integer, ForeignKey("lending.lending_id"), primary_key=True),
    Column("num_days_late", Integer),
)


parameter_table = Table(
    "parameter",
    metadata_obj,
    Column("id_lock", Integer, CheckConstraint("id_lock<=1"), primary_key=True),
    Column("minimum_age", Integer),
    Column("maximum_age", Integer),
    Column("maximum_account_age", Integer),
    Column("maximum_publication_year_gab", Integer),
    Column("maximum_lending_quantity", Integer),
    Column("maximum_lending_period", Integer),
    CheckConstraint("minimum_age < maximum_age"),
)

image_table = Table(
    "image_path",
    metadata_obj,
    Column("image_id", Integer, primary_key=True),
    Column("image_file_name", String, nullable=False),
    Column("file_path", String, nullable=False),
)
