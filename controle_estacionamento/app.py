from flask import Flask, render_template, request, redirect, session
from datetime import datetime
from database.database import conexao, cursor

app = Flask(__name__)
app.secret_key = 'estacionamento123'

TOTAL_VAGAS = 50
TEMPO_TOLERANCIA_MINUTOS = 15
VALOR_POR_MINUTO_EXCEDENTE = 0.50

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        if usuario == 'admin' and senha == '123':
            session['usuario'] = usuario
            return redirect('/dashboard')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect('/')

    cursor.execute('SELECT * FROM veiculos WHERE saida IS NULL')
    veiculos = cursor.fetchall()

    vagas_ocupadas = len(veiculos)
    vagas_disponiveis = TOTAL_VAGAS - vagas_ocupadas

    return render_template(
        'dashboard.html',
        veiculos=veiculos,
        vagas=vagas_disponiveis,
        ocupadas=vagas_ocupadas)

@app.route('/entradas')
def entradas():
    if 'usuario' not in session:
        return redirect('/')
        
    cursor.execute('SELECT * FROM veiculos WHERE saida IS NULL')
    veiculos_ativos = cursor.fetchall()
    
    return render_template('entradas.html', veiculos=veiculos_ativos)

@app.route('/historico')
def historico():
    if 'usuario' not in session:
        return redirect('/')
        
    cursor.execute('SELECT * FROM veiculos WHERE saida IS NOT NULL ORDER BY saida DESC')
    historico_veiculos = cursor.fetchall()
    
    return render_template('historico.html', veiculos=historico_veiculos)

@app.route('/relatorios')
def relatorios():
    if 'usuario' not in session:
        return redirect('/')
        
    cursor.execute('SELECT SUM(valor) FROM veiculos WHERE saida IS NOT NULL')
    resultado = cursor.fetchone()
    faturamento_total = resultado[0] if resultado[0] is not None else 0.0
    
    return render_template('relatorios.html', faturamento=faturamento_total)

@app.route('/entrada', methods=['POST'])
def entrada():
    if 'usuario' not in session:
        return redirect('/')

    placa = request.form['placa']
    modelo = request.form['modelo']
    minutos = int(request.form['minutos'])
    entrada = datetime.now()
    valor_inicial = 0.0

    cursor.execute("""
    INSERT INTO veiculos(placa, modelo, minutos, entrada, valor)
    VALUES (?, ?, ?, ?, ?)
    """, (placa, modelo, minutos, entrada, valor_inicial))
    
    conexao.commit()
    return redirect('/dashboard')

@app.route('/saida/<int:id>')
def saida(id):
    if 'usuario' not in session:
        return redirect('/')

    cursor.execute('SELECT entrada FROM veiculos WHERE id = ?', (id,))
    dados = cursor.fetchone()

    try:
        entrada = datetime.fromisoformat(dados[0])
    except ValueError:
        entrada = datetime.strptime(dados[0].split('.')[0], '%Y-%m-%d %H:%M:%S')
        
    saida = datetime.now()
    diferenca_tempo = saida - entrada
    tempo_total_minutos = round(diferenca_tempo.total_seconds() / 60)

    if tempo_total_minutos <= TEMPO_TOLERANCIA_MINUTOS:
        valor_final = 0.0
    else:
        minutos_excedentes = tempo_total_minutos - TEMPO_TOLERANCIA_MINUTOS
        valor_final = minutos_excedentes * VALOR_POR_MINUTO_EXCEDENTE
    cursor.execute("""
    UPDATE veiculos
    SET saida = ?, valor = ?
    WHERE id = ?
    """, (saida, valor_final, id))
    
    conexao.commit()
    return redirect('/dashboard')

if __name__ == '__main__':
    app.run(debug=True, port=5001)