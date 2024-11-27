from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from datetime import datetime
import re


app = Flask(__name__)
app.secret_key = 'batata' 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, 'pousada_ypua.db')

from flask import Flask, render_template
from datetime import datetime

# Definindo o filtro de data
@app.template_filter('datetimeformat')
def datetimeformat(value):
    if isinstance(value, str):  # Se for uma string de data
        try:
            return datetime.strptime(value, '%Y-%m-%d').strftime('%d/%m/%Y')
        except ValueError:
            return value  # Se não for possível converter, retorna o valor original
    elif isinstance(value, datetime.date):  # Se for um objeto datetime.date
        return value.strftime('%d/%m/%Y')  # Formata diretamente
    return value  # Se não for string nem date, retorna o valor original

#obtem conexão com o banco de dados
def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

#página inicial - redireciona para a tela de login
@app.route('/')
def index():
    return redirect(url_for('login'))

#tela de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #verifica as credenciais no banco de dados
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM usuarios WHERE nome_usuario = ? AND senha = ?', (username, password)).fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash("Usuário ou senha incorretos.", "error")
    
    #renderiza a página de login para GET ou após tentativa incorreta de login
    return render_template('html/login.html')

#página inicial de hóspedes (exemplo de redirecionamento após login)
@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('html/home.html')

#página de listagem de hóspedes
@app.route('/hospedes')
def listar_hospedes():
    conn = get_db_connection()
    hospedes = conn.execute('SELECT * FROM hospedes').fetchall() if conn else []
    if conn:
        conn.close()
    return render_template('html/index.html', hospedes=hospedes)

#página de cadastro de hóspede 
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        email = request.form['email']
        data_nascimento = request.form['data_nascimento']
     # Formata o telefone para o formato (XX) XXXXX-XXXX
        telefone = formatar_telefone(telefone)

        # Verifica se o telefone está no formato correto
        if not re.match(r'^\(\d{2}\) \d{5}-\d{4}$', telefone):
            flash("Telefone inválido! O formato correto é (XX) XXXXX-XXXX.", "error")
            return redirect(url_for('cadastro'))

        conn = get_db_connection()
        if conn:
            conn.execute('INSERT INTO hospedes (nome, cpf, telefone, email, data_nascimento) VALUES (?, ?, ?, ?, ?)',
                         (nome, cpf, telefone, email, data_nascimento))
            conn.commit()
            conn.close()

        return redirect(url_for('listar_hospedes'))

    return render_template('html/cadastro_hospede.html')

# Função para formatar o telefone
def formatar_telefone(telefone):
    # Remove tudo que não é número
    telefone = re.sub(r'\D', '', telefone)
    
    # Formata o telefone com DDD
    if len(telefone) == 11:  # Para números com DDD e 9 dígitos
        return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"
    elif len(telefone) == 10:  # Para números com DDD e 8 dígitos
        return f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}"
    else:
        return telefone  # Retorna o valor sem formatação se não for válido

#página de listagem de reservas 
@app.route('/reservas')
def listar_reservas():
    conn = get_db_connection()
    reservas = conn.execute('''
        SELECT 
            reservas.id_reserva,
            reservas.id_hospede,
            reservas.id_acomodacao,
            reservas.data_checkin,
            reservas.data_checkout,
            reservas.valor_total,
            reservas.data_reserva,
            hospedes.nome AS nome_hospede
        FROM reservas
        JOIN hospedes ON reservas.id_hospede = hospedes.id_hospede
    ''').fetchall() if conn else []
    conn.close()

    return render_template('html/reservas.html', reservas=reservas)

from datetime import datetime
from flask import Flask, render_template

from datetime import datetime


@app.route('/cadastro_reserva', methods=['GET', 'POST'])
def cadastro_reserva():
    if request.method == 'POST':
        id_hospede = request.form['id_hospede']
        id_acomodacao = request.form['id_acomodacao']
        data_checkin = request.form['data_checkin']
        data_checkout = request.form['data_checkout']
        valor_total = request.form['valor_total']

        conn = get_db_connection()
        if conn:
            conn.execute('''
                INSERT INTO reservas 
                (id_hospede, id_acomodacao, data_checkin, data_checkout, status, valor_total, data_reserva)
                VALUES (?, ?, ?, ?, ?, ?, DATE('now'))
            ''', (id_hospede, id_acomodacao, data_checkin, data_checkout, valor_total))
            conn.commit()
            conn.close()

        #redireciona para a listagem de reservas após o cadastro
        return redirect(url_for('listar_reservas'))

    #para GET, exibe o formulário
    conn = get_db_connection()
    hospedes = conn.execute('SELECT * FROM hospedes').fetchall() if conn else []
    acomodacoes = conn.execute('SELECT id_acomodacao, nomes FROM acomodacoes').fetchall() if conn else []
    conn.close()
    return render_template('html/cadastro_reserva.html', hospedes=hospedes, acomodacoes=acomodacoes)


@app.route('/funcionarios')
def funcionarios():
    conn = get_db_connection()
    funcionarios = conn.execute('SELECT * FROM funcionarios').fetchall() if conn else []
    conn.close()
    return render_template('html/funcionarios.html', funcionarios=funcionarios)

#rotas para outras páginas com uso de url_for para links de rotas
@app.route('/acomodacoes')
def acomodacoes():
    return render_template('html/acomodacoes.html')

@app.route('/add')
def add():
    return render_template('html/add_hospede.html')

@app.route('/administrador')
def administrador():
    return render_template('html/administrador.html')

@app.route('/agenda_geral')
def agenda_geral():
    return render_template('html/agenda_geral.html')

@app.route('/area_financeira_funcionario')
def area_financeira_funcionario():
    return render_template('html/area_finan_funcionario.html')

@app.route('/gerenciamento_hospedes')
def gerenciamento_hospedes():
    return render_template('html/gerenciamento_hospedes.html')

@app.route('/gerenciamento_reserva')
def gerenciamento_reserva():
    return render_template('html/gerenciamento_reserva.html')

@app.route('/privacidade')
def privacidade():
    return render_template('html/privacidade.html')

@app.route('/servico')
def servico():
    return render_template('html/serviço.html')

# Página de logout para finalizar a sessão do usuário
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Executando o aplicativo
if __name__ == '__main__':
    app.run(debug=True)
