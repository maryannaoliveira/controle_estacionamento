import sqlite3

conexao = sqlite3.connect(
    'database/estacionamento.db',
    check_same_thread=False
)

cursor = conexao.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS veiculos(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    placa TEXT,

    modelo TEXT,

    minutos INTEGER,

    entrada TEXT,

    saida TEXT,

    valor REAL

)

""")

conexao.commit()