import sqlite3


def negotiations(file, condition1, condition2, sortField):
    with sqlite3.connect(file) as db:
        cur = db.cursor()

        resName = cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table';")
        for i in resName:
            dbName = i[0]

        resList = cur.execute(
            f"""SELECT condition FROM {dbName}
            WHERE {condition1} AND {condition2} ORDER BY {sortField}""")
        for j in resList:
            print(j[0])


if __name__ == "__main__":
    file = input()
    condition1 = input()
    condition2 = input()
    sortField = input()
    negotiations(file, condition1, condition2, sortField)