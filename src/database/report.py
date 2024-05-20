from sqlalchemy import select, insert, null
from .connection import Session
from .models import report_by_genre_detail_table as rgt, late_return_report_detail_table as lgt

def update_rgt(genre_id, time):
    day, month, year = time.split('/')
    with Session() as session:
        session.execute(insert(rgt).values(genre_id=genre_id, month = month, year = year))
        session.commit()

def get_rgt(month, year):
    with Session() as session:
        results = session.execute(select(rgt).where(rgt.c.month == month and rgt.c.year == year)).all()

    # Khởi tạo một từ điển để lưu trữ số lượng 'genre_id' cho mỗi loại
    genre_id_count = {}

    # Lặp qua từng bản ghi trong kết quả
    for row in results:
        # Lấy giá trị 'genre_id' từ bản ghi
        genre_id = row[rgt.c.genre_id]

        # Kiểm tra xem 'genre_id' đã tồn tại trong từ điển chưa
        # Nếu chưa tồn tại, thêm 'genre_id' vào từ điển và đặt giá trị là 1
        # Nếu đã tồn tại, tăng giá trị của 'genre_id' lên 1
        if genre_id in genre_id_count:
            genre_id_count[genre_id] += 1
        else:
            genre_id_count[genre_id] = 1

    return genre_id_count
