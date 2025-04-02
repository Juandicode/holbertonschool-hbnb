import sqlite3
#la funcion lo que hace es conectarse a la db , abre el script, lo ejecuta y en el if llama a los archivos schema(tablas)
#y init data (lo que quiero insertar en el schema )
def run_sql_script(db_path, script_path):
    conn = sqlite3.connect(db_path)
    with open(script_path, 'r') as file:
        sql_script = file.read()
    try:
        conn.executescript(sql_script)
        print(f'Executed {script_path} successfully.')
    except Exception as exception:
        print(f'Error executting {script_path}: {exception}')
    finally:
        conn.close()

if __name__ == '__main__':
    db_file = 'development.db'
    run_sql_script(db_file, 'schema.sql')
    run_sql_script(db_file, 'init_data.sql')