from flask import Flask, request, redirect
app = Flask(__name__)
chromebooks = []
proximo_id = 1
HTML = """<!DOCTYPE html><html lang="pt-br"><head><meta charset="UTF-8"><title><title>EUCLIDES PLAY</title>
<style>body{font-family:Arial;background:#f0f2f5;padding:20px}.card{background:white;padding:20px;border-radius:10px;max-width:900px;margin:auto}input,select{padding:8px;margin:5px;width:95%}button{background:#1a73e8;color:white;border:none;padding:10px 20px;border-radius:5px}table{width:100%;border-collapse:collapse;margin-top:15px}th,td{border:1px solid #ddd;padding:8px}</style></head>
<body><div class="card"<h2>EUCLIDES PLAY</h2>
<form method="POST" action="/adicionar">
<select name="unidade" required><option value="">Selecione a Unidade</option><option>Colegio</option><option>Creche Vila Da Penha</option><option>Vila da Penha</option><option>Cachambi</option><option>Creche Cachambi</option><option>Vila Valqueire</option><option>Vila Valqueire 2</option><option>Vila Isabel</option></select>
<input name="nome" placeholder="Nome do aluno" required><input name="turma" placeholder="Turma ex: 901" required><input name="numero" placeholder="N do Chromebook ex: CB-01" required><select name="status"><option>Em uso</option><option>Devolvido</option><option>Manutencao</option></select><br><button type="submit">Cadastrar</button></form>
<table><tr><th>ID</th><th>Unidade</th><th>Aluno</th><th>Turma</th><th>Chromebook</th><th>Status</th><th>Acao</th></tr>"""
@app.route("/")
def index():
    linhas = ""
    for c in chromebooks:
        linhas += f"<tr><td>{c['id']}</td><td>{c['unidade']}</td><td>{c['nome']}</td><td>{c['turma']}</td><td>{c['numero']}</td><td>{c['status']}</td><td><a href='/excluir/{c['id']}'>Excluir</a></td></tr>"
    return HTML + linhas + "</table></div></body></html>"
@app.route("/adicionar", methods=["POST"])
def adicionar():
    global proximo_id
    chromebooks.append({"id": proximo_id, "unidade": request.form["unidade"], "nome": request.form["nome"], "turma": request.form["turma"], "numero": request.form["numero"], "status": request.form["status"]})
    proximo_id += 1
    return redirect("/")
@app.route("/excluir/<int:id>")
def excluir(id):
    global chromebooks
    chromebooks = [c for c in chromebooks if c["id"] != id]
    return redirect("/")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
