from flask import Flask, request, redirect, url_for, render_template_string
from datetime import datetime

app = Flask(__name__)
registros = []
proximo_id = [1]

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
    hora_atual = datetime.now().hour
    for r in registros:
        if r['status'] == 'Em uso' and hora_atual >= 17:
            r['status'] = 'Não entregou no dia'
    html = """
    <style>
    body{font-family:Arial; background:#f2f2f2; padding:20px}
    .box{background:white; max-width:900px; margin:auto; padding:20px; border-radius:10px}
    input,select{width:100%; padding:10px; margin:5px 0; box-sizing:border-box; border:1px solid #ccc; border-radius:6px}
    button{padding:8px 14px; border:none; border-radius:6px; cursor:pointer}
    table{width:100%; border-collapse:collapse; margin-top:15px}
    th,td{padding:8px; border-bottom:1px solid #ddd; text-align:center}
    .badge{padding:5px 12px; border-radius:20px; font-weight:bold; font-size:13px}
    </style>
    <div class="box">
    <h3 style="text-align:center">EUCLIDES PLAY</h3>
    <form action="/cadastrar" method="post">
        <select name="unidade" required>
            <option value="">Selecione a Unidade</option>
            <option>Colégio Unidade 1</option>
            <option>Creche Vila da Penha Unidade 2</option>
            <option>Vila da Penha Unidade 3</option>
            <option>Cachambi Unidade 4</option>
            <option>Creche Cachambi</option>
            <option>Vila Isabel Unidade 5</option>
            <option>Valqueire Unidade 6</option>
            <option>Valqueire Unidade 7</option>
        </select>
        <input name="nome" placeholder="Nome do aluno" required>
        <input name="turma" placeholder="Turma ex: 901" required>
        <input name="chromebook" placeholder="N do Chromebook ex: CB-01" required>
        <select name="status" id="selectStatus" onchange="pintarSelect()" style="background:red; color:white; font-weight:bold;">
            <option style="background:red; color:white;">Em uso</option>
            <option style="background:green; color:white;">Devolvido</option>
            <option style="background:yellow; color:black;">Manutenção</option>
        </select>
        <button style="background:#00aaff;color:white; width:100%; padding:12px; font-weight:bold;">Cadastrar</button>
    </form>
    <script>
    function pintarSelect(){
        var s = document.getElementById('selectStatus');
        if(s.value == 'Em uso'){ s.style.background='red'; s.style.color='white'; }
        if(s.value == 'Devolvido'){ s.style.background='green'; s.style.color='white'; }
        if(s.value == 'Manutenção'){ s.style.background='yellow'; s.style.color='black'; }
    }
    </script>
    <table>
    <tr><th>ID</th><th>Unidade</th><th>Aluno</th><th>Turma</th><th>Chromebook</th><th>Status</th><th>Acao</th></tr>
    """
    for r in registros:
        estilo = cor_status(r['status'])
        html += f"""
        <tr>
        <td>{r['id']}</td>
        <td>{r['unidade']}</td>
        <td>{r['nome']}</td>
        <td>{r['turma']}</td>
        <td>{r['chromebook']}</td>
        <td><span class="badge" style="{estilo}">{r['status']}</span></td>
        <td><form action="/excluir/{r['id']}" method="post" style="display:inline"><button style="background:red;color:white">Excluir</button></form></td>
        </tr>
        """
    html += "</table></div>"
    return render_template_string(html)

@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    registros.append({"id": proximo_id[0],"unidade": request.form['unidade'],"nome": request.form['nome'],"turma": request.form['turma'],"chromebook": request.form['chromebook'],"status": request.form['status']})
    proximo_id[0] += 1
    return redirect(url_for('index'))

@app.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    global registros
    registros = [r for r in registros if r['id'] != id]
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
