import sqlite3 as sq


def sql_start():
	global base, cur
	base = sq.connect('data.db')
	cur = base.cursor()
	cur.execute('''
		CREATE TABLE IF NOT EXISTS groups (
			id INTEGER PRIMARY KEY,
			"group" TEXT
			);
		''')
	base.commit()
        
	cur.execute('''
		CREATE TABLE IF NOT EXISTS files (
			id INTEGER PRIMARY KEY,
			doc_id TEXT,
            name TEXT
			);
		''')
	base.commit()


#Файлы
async def add_file(doc_id, name):
    cur.execute('INSERT INTO files (doc_id, name) VALUES (?, ?)', (doc_id, name)) 
    base.commit()

async def delete_file(name):
    cur.execute('DELETE FROM files WHERE name = ?', (name,))  
    base.commit()
    
async def file_exists(file_name: str) -> bool:
    cur.execute("SELECT COUNT(*) FROM files WHERE name=?", (file_name,))
    result = cur.fetchone()[0]

    # Если количество найденных совпадений больше 0, то файл существует
    if result > 0:
        return True
    else:
        return False

#Группы
async def get_group(id):
    return cur.execute('SELECT "group" FROM groups WHERE id=?', (id,)).fetchone()[0]

async def set_group_in_db(id, group):
    cur.execute('INSERT INTO groups VALUES (?, ?)', (id, group))
    base.commit()

async def change_group_in_db(id, group):
    cur.execute('UPDATE groups SET "group" = ? WHERE id = ?', (group, id))
    base.commit()
    