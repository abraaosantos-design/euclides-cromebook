from flask import Flask, request, redirect, url_for, render_template_string
from datetime import datetime

app = Flask(__name__)

chromebooks = []
for i in range(1, 31):
    chromebooks.append({"numero": i, "nome": "", "turma": "", "status": "Devolvido"})

# CORES DOS STATUS - DO JEITO QUE VOCÊ PEDIU
def cor_status(status):
    if status == "Em uso":
        return "background:red; color:white;"
    if status == "Devolvido":
        return "background:green; color:white;"
    if status == "Manutenção":
        return "background:yellow; color:black;"
    if status == "Não entregou no dia":
        return "background:purple; color:white;"
    return "background:gray; color:white;"

@app.route("/")
def index():
    # REGRA DAS 17H - SE AINDA ESTÁ EM USO VIRA ROXO
    hora_atual = datetime.now().hour
    for c in chromebooks:
        if c['status'] == 'Em uso' and hora_atual >= 17:
            c['status'] = 'Não entregou no dia'

    html = """
    <style>
    body{font-family:Arial; background:#f2f2f2; padding:20px}
    h1{text-align:center}
    table{width:100%; background:white; border-collapse:collapse}
    th,td{padding:10px; border-bottom:1px solid #ddd; text-align:center}
    .badge{padding:5px 12px; border-radius:20px; font-weight:bold; font-size:13px}
    button{padding:6px 10px; border:none; border-radius:6px; cursor:pointer; margin:2px}
    input{padding:6px; margin:2px}
    </style>
    <h1>Escola Euclides da Cunha - Chromebooks</h1>
    <table>
    <tr><th>Número</th><th>Aluno</th><th>Turma</th><th>Status</th><th>Ação</th></tr>
    """
    for c in chromebooks:
        estilo = cor_status(c['status'])
        html += f"""
        <tr>
        <td>{c['numero']}</td>
        <td>{c['nome']}</td>
        <td>{c['turma']}</td>
        <td><span class="badge" style="{estilo}">{c['status']}</span></td>
        <td>
            <form action="/saida/{c['numero']}" method="post" style="display:inline">
                <input name="nome" placeholder="Nome" required>
                <input name="turma" placeholder="Turma" required>
                <button style="background:#2563eb;color:white">Registrar Saída</button>
            </form>
            <form action="/devolver/{c['numero']}" method="post" style="display:inline">
                <button style="background:green;color:white">Devolver</button>
            </form>
            <form action="/manutencao/{c['numero']}" method="post" style="display:inline">
                <button style="background:#facc15">Manutenção</button>
            </form>
        </td>
        </tr>
        """
    html += "</table>"
    return render_template_string(html)

@app.route("/saida/<int:numero>", methods=["POST"])
def saida(numero):
    for c in chromebooks:
        if c['numero'] == numero:
            c['nome'] = request.form['nome']
            c['turma'] = request.form['turma']
            c['status'] = 'Em uso'
    return redirect(url_for('index'))

@app.route("/devolver/<int:numero>", methods=["POST"])
def devolver(numero):
    for c in chromebooks:
        if c['numero'] == numero:
            c['nome'] = ""
            c['turma'] = ""
            c['status'] = 'Devolvido'
    return redirect(url_for('index'))

@app.route("/manutencao/<int:numero>", methods=["POST"])
def manutencao(numero):
    for c in chromebooks:
        if c['numero'] == numero:
            c['status'] = 'Manutenção'
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


🔴 Em uso = Vermelho
🟢 Devolvido = Verde
🟡 Manutenção = Amarelo
🟣 Depois das 17h e não devolveu = Roxo


