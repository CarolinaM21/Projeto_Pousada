from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para obter conexão com o banco de dados
def get_db_connection():
    try:
        conn = sqlite3.connect('C:/Users/anamaciel/Documents/pousada_ypua/pousada_ypua.db')
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
        # Aqui você pode adicionar a lógica de autenticação do usuário
        # Exemplo simplificado de autenticação:
        username = request.form['username']
        password = request.form['password']

        # Verifica credenciais no banco de dados (exemplo simplificado)
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if user:
            # Login bem-sucedido, redireciona para a página 'home'
            return redirect(url_for('home'))
        else:
            # Login falhou, redireciona de volta para o login (ou exibe uma mensagem de erro)
            return render_template('html/login.html', error="Usuário ou senha incorretos.")

    return render_template('html/login.html')

# Página inicial de hóspedes (exemplo de redirecionamento após login)
@app.route('/home')
def home():
    return render_template('html/home.html')

# Página de listagem de hóspedes
@app.route('/hospedes')
def listar_hospedes():
    conn = get_db_connection()
    if conn:
        hospedes = conn.execute('SELECT * FROM hospedes').fetchall()
        conn.close()
    else:
        hospedes = []  # Caso ocorra um erro de conexão, hospedes será uma lista vazia
    return render_template('html/index.html', hospedes=hospedes)

# Página de cadastro de hóspede - Aceita GET para exibir o formulário e POST para salvar os dados
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        # Obtendo dados do formulário
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        email = request.form['email']
        data_nascimento = request.form['data_nascimento']

        # Inserindo dados no banco de dados
        conn = get_db_connection()
        if conn:
            conn.execute('INSERT INTO hospedes (nome, cpf, telefone, email, data_nascimento) VALUES (?, ?, ?, ?, ?)',
                         (nome, cpf, telefone, email, data_nascimento))
            conn.commit()
            conn.close()
        
        # Redireciona para a página de listagem de hóspedes
        return redirect(url_for('listar_hospedes'))

    # Exibe o formulário de cadastro
    return render_template('html/cadastro_hospede.html')

# Rotas para outras páginas
@app.route('/acomodacoes')
def acomodacoes():
    return render_template('html/acomodacoes.html')

@app.route('/add')
def add():
    return render_template('html/add.html')

@app.route('/administrador')
def administrador():
    return render_template('html/administrador.html')

@app.route('/agenda_geral')
def agenda_geral():
    return render_template('html/agenda_geral.html')

@app.route('/area_financeira_funcionario')
def area_financeira_funcionario():
    return render_template('html/area_finan_funcionario.html')

@app.route('/cadastro_reserva')
def cadastro_reserva():
    return render_template('html/cadastro_reserva.html')

@app.route('/funcionarios')
def funcionarios():
    return render_template('html/funcionarios.html')

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

# Executando o aplicativo
if __name__ == '__main__':
    app.run(debug=True)
