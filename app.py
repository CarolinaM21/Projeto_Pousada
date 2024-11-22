from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'batata'  # Chave secreta para sessões e mensagens flash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, 'pousada_ypua.db')

# Função para obter conexão com o banco de dados
def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Define a fábrica de linhas para permitir acesso por nome da coluna
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Página inicial - Redireciona para a tela de login
@app.route('/')
def index():
    return redirect(url_for('login'))

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verifica credenciais no banco de dados
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM usuarios WHERE nome_usuario = ? AND senha = ?', (username, password)).fetchone()
        conn.close()

        if user:
            # Armazena o usuário na sessão e redireciona para a página 'home'
            session['username'] = username
            return redirect(url_for('home'))
        else:
            # Mensagem de erro se as credenciais estiverem incorretas
            flash("Usuário ou senha incorretos.", "error")
    
    # Renderiza a página de login para GET ou após tentativa incorreta de login
    return render_template('html/login.html')

# Página inicial de hóspedes (exemplo de redirecionamento após login)
@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('html/home.html')

# Página de listagem de hóspedes
@app.route('/hospedes')
def listar_hospedes():
    conn = get_db_connection()
    hospedes = conn.execute('SELECT * FROM hospedes').fetchall() if conn else []
    if conn:
        conn.close()
    return render_template('html/index.html', hospedes=hospedes)

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
        if conn:
            conn.execute('INSERT INTO hospedes (nome, cpf, telefone, email, data_nascimento) VALUES (?, ?, ?, ?, ?)',
                         (nome, cpf, telefone, email, data_nascimento))
            conn.commit()
            conn.close()

        return redirect(url_for('listar_hospedes'))

    return render_template('html/cadastro_hospede.html')

# Página de listagem de reservas com nome do hóspede
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
            reservas.status,
            reservas.valor_total,
            reservas.data_reserva,
            hospedes.nome AS nome_hospede
        FROM reservas
        JOIN hospedes ON reservas.id_hospede = hospedes.id_hospede
    ''').fetchall() if conn else []
    conn.close()
    return render_template('html/reservas.html', reservas=reservas)

@app.route('/cadastro_reserva', methods=['GET', 'POST'])
def cadastro_reserva():
    if request.method == 'POST':
        id_hospede = request.form['id_hospede']
        id_acomodacao = request.form['id_acomodacao']
        data_checkin = request.form['data_checkin']
        data_checkout = request.form['data_checkout']
        status = request.form['status']
        valor_total = request.form['valor_total']

        conn = get_db_connection()
        if conn:
            conn.execute('''
                INSERT INTO reservas 
                (id_hospede, id_acomodacao, data_checkin, data_checkout, status, valor_total, data_reserva)
                VALUES (?, ?, ?, ?, ?, ?, DATE('now'))
            ''', (id_hospede, id_acomodacao, data_checkin, data_checkout, status, valor_total))
            conn.commit()
            conn.close()

        # Redireciona para a listagem de reservas após o cadastro
        return redirect(url_for('listar_reservas'))

    # Para GET, exibe o formulário
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

# Rotas para outras páginas com uso de url_for para links de rotas
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
