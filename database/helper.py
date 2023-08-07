import sqlite3 as sql

db = sql.connect("database/members.sdb")
curs = db.cursor()


def add_steam(author, steam_id):
    if curs.execute("SELECT steam_id FROM members WHERE id = ?", (author.id,)).fetchone() is None:
        curs.execute("INSERT INTO members (id, created_at, kaban, steam_id) VALUES (?, ?, ?, ?)", (author.id, author.created_at, 0, steam_id))
        db.commit()
        print(1)
    else:
        print(2)
        return
