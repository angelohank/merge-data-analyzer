from flask import Flask, render_template, redirect, url_for
import os
import repository

app = Flask(__name__)

@app.route('/merges')
def list_merges():
    conn = repository.connection_db()
    cur = conn.cursor()
    cur.execute("select  m.id_merge, m.link, fgrevisado from merges m left join pipelines p on m.id_merge = p.id_merge where p.status = 'failed'")
    merges = cur.fetchall()
    cur.close()
    conn.close()

    current_path = os.path.dirname(os.path.abspath(__file__))
    return render_template('merge.html', merges=merges)

@app.route('/update_fgrevisado/<int:id_merge>', methods=['POST'])
def update_fgrevisado(id_merge):
    conn = repository.connection_db()
    cur = conn.cursor()
    cur.execute('UPDATE merges SET fgrevisado = %s WHERE id_merge = %s', ('T', id_merge))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('list_merges'))

if __name__ == '__main__':
    app.run(debug=True)