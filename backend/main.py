import os
import psycopg2
from flask import Flask, request, redirect, url_for

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add':
            nowa_tresc = request.form.get('tresc')
            if nowa_tresc:
                cur.execute('INSERT INTO komunikaty (wiadomość) VALUES (%s)', (nowa_tresc,))
        
        elif action == 'delete':
            id_do_usuniecia = request.form.get('id_notatki')
            if id_do_usuniecia:
                cur.execute('DELETE FROM komunikaty WHERE id = %s', (id_do_usuniecia,))

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    cur.execute('SELECT id, wiadomość FROM komunikaty ORDER BY id DESC;')
    wiadomosci = cur.fetchall()
    
    cur.close()
    conn.close()

    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Projekt WiK</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; background-color: #f4f4f9; }}
            h1 {{ color: #2c3e50; text-align: center; }}
            
            /* Formularz dodawania */
            .add-form {{ display: flex; gap: 10px; margin-bottom: 30px; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            input[type="text"] {{ flex-grow: 1; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }}
            .btn-add {{ padding: 10px 20px; background-color: #27ae60; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; }}
            .btn-add:hover {{ background-color: #219150; }}

            /* Lista notatek */
            ul {{ list-style-type: none; padding: 0; }}
            li {{ background: white; border-bottom: 1px solid #eee; padding: 15px; margin-bottom: 10px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
            
            /* Przycisk usuwania */
            .btn-delete {{ background-color: #e74c3c; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-size: 0.9em; }}
            .btn-delete:hover {{ background-color: #c0392b; }}
        </style>
    </head>
    <body>
        <h1>📝 Menedżer Notatek</h1>
        
        <form method="POST" class="add-form">
            <input type="hidden" name="action" value="add">
            <input type="text" name="tresc" placeholder="Co masz do zrobienia?" required>
            <button type="submit" class="btn-add">Dodaj</button>
        </form>

        <h3>Twoje zadania:</h3>
        <ul>
            {''.join(f'''
                <li>
                    <span>{msg[1]}</span>
                    <form method="POST" style="margin:0;">
                        <input type="hidden" name="action" value="delete">
                        <input type="hidden" name="id_notatki" value="{msg[0]}">
                        <button type="submit" class="btn-delete">Usuń</button>
                    </form>
                </li>
            ''' for msg in wiadomosci)}
        </ul>
    </body>
    </html>
    """
    return html_template

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)