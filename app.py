from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('C:/Users/anamaciel/Documents/pousada_ypua/pousada_ypua.db')
    conn.row_factory = sqlite3.Row
    return conn

# Página inicial - Exibe dados dos hóspedes
@app.route('/')
def index():
    conn = get_db_connection()
    hospedes = conn.execute('SELECT * FROM hospedes').fetchall()
    conn.close()
    return render_template('index.html', hospedes=hospedes)

# Página de cadastro de hóspede - Aceita GET para exibir o formulário e POST para salvar os dados
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        email = request.form['email']
        data_nascimento = request.form['data_nascimento']

        conn = get_db_connection()
        conn.execute('INSERT INTO hospedes (nome, cpf, telefone, email, data_nascimento) VALUES (?, ?, ?, ?, ?)',
                     (nome, cpf, telefone, email, data_nascimento))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))

    return render_template('cadastro-hospede.html')

if __name__ == '__main__':
    app.run(debug=True)
