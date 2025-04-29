
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

def init_db(db_name):
    database = QSqlDatabase.addDatabase('QSQLITE')
    database.setDatabaseName(db_name)

    # make sure to check if the database is open!
    if not database.open():
        print("Database failed to open:", database.lastError().text())
        return False

    query = QSqlQuery()
    # add entities
    query.exec("""
                CREATE TABLE IF NOT EXISTS calendar ( 
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    start_time TEXT,
                    end_time TEXT,
                    category TEXT,
                    description TEXT,
                    appt_type TEXT
                )
                """)
    return True

def fetch_appointments():
    query = QSqlQuery('SELECT * FROM calendar ORDER BY date DESC')
    appointments = [] # essentially a matrix. list full of lists, each list in expenses represents a row in the database
    while query.next():
        appointments.append([query.value(i) for i in range(7)]) # 7 is the number of entities in calendar
    return appointments

def add_appointment(date, start_time, end_time, category, description, appt_type):
    # id is automatically generated
    query = QSqlQuery()
    # prepare to add data, prepare to send data off to database
    query.prepare("""
                    INSERT INTO calendar (date, start_time, end_time, category, description, appt_type)
                    VALUES (?, ?, ?, ?, ?, ?)
                """)
    # bind all the values to the SQL query, type is 0 for regular, 1 relative, 2 series
    query.addBindValue(date)
    query.addBindValue(start_time)
    query.addBindValue(end_time)
    query.addBindValue(category)
    query.addBindValue(description)
    query.addBindValue(appt_type)

    return query.exec()

def delete_appointment(event_id):
    query = QSqlQuery()
    query.prepare('DELETE FROM calendar WHERE id = ?')
    query.addBindValue(event_id)
    return query.exec()
