import sqlite3
from config import DATABASE, token


class DB_Manager:

    def __init__(self, database):
        self.database = database # Nama databasenya
        
    def create_tables(self):
        conn = sqlite3.connect(self.database)

        with conn:

        
            conn.execute('''CREATE TABLE IF NOT EXISTS skills (
                skill_id INTEGER PRIMARY KEY,
                skill_name TEXT
            )
            ''')

            conn.execute('''CREATE TABLE IF NOT EXISTS status (
                status_id INTEGER PRIMARY KEY,
                status_name TEXT
            )
            ''')

            conn.execute('''CREATE TABLE IF NOT EXISTS projects (
                project_id INTEGER PRIMARY KEY,
                project_name TEXT,
                description TEXT,
                url TEXT,
                user_id INTEGER,
                status_id INTEGER,
                FOREIGN KEY (status_id) REFERENCES status(status_id)
            )
            ''')

            conn.execute('''CREATE TABLE IF NOT EXISTS project_skills (
                project_id INTEGER,
                skill_id INTEGER,
                PRIMARY KEY (project_id, skill_id),
                FOREIGN KEY (project_id) REFERENCES projects(project_id),
                FOREIGN KEY (skill_id) REFERENCES skills(skill_id)
            )
            ''')

            columns = conn.execute("PRAGMA table_info(projects)").fetchall()
            if not any(column[1] == "screenshot" for column in columns):
                conn.execute("ALTER TABLE projects ADD COLUMN screenshot TEXT")

            conn.commit()

        print("database")

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()

    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()   


    def default_insert(self):
        skills = [ (_,) for _ in (['Python', 'SQL', 'API', 'Discord'])]
        statuses = [ (_,) for _ in (['Pembuatan Prototipe', 'Dalam Pengembangan', 'Selesai, siap digunakan', 'Diperbarui', 'Selesai, tapi tidak sedang dilanjutkan'])]


        sql = 'INSERT INTO skills (skill_name) values(?)'
        data = skills
        self.__executemany(sql, data)
        sql = 'INSERT INTO status (status_name) values(?)'
        data = statuses
        self.__executemany(sql, data)


    def insert_project(self, data):
        sql = """INSERT INTO projects 
(user_id, project_name, url, status_id) 
values(?, ?, ?, ?)"""
        self.__executemany(sql, [data])

    def get_statuses(self):
        sql="SELECT status_name from status"
        return self.__select_data(sql)

    def update_projects(self, param, data):
        sql = f"""UPDATE projects SET {param} = ? 
WHERE project_name = ? AND user_id = ?"""
        self.__executemany(sql, [data]) 
            
    def delete_project(self, user_id, project_id):
        sql = """DELETE FROM projects 
WHERE user_id = ? AND project_id = ? """
        self.__executemany(sql, [(user_id, project_id)])

    def get_projects(self, user_id):
        sql="""SELECT * FROM projects 
WHERE user_id = ?"""
        return self.__select_data(sql, data = (user_id,))

    def delete_skill(self, project_id, skill_id):
        sql = """DELETE FROM skills 
WHERE skill_id = ? AND project_id = ? """
        self.__executemany(sql, [(skill_id, project_id)])
                           
            