from flask import Flask, request, redirect, url_for, render_template_string, send_file
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/foto')
def foto():
    for nome in ['foto.jpg', 'foto', 'foto.jpg.jpg', 'foto.jpeg', 'foto.png']:
        if os.path.exists(nome):
            return send_file(nome)
    return "Foto nao encontrada", 404

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

SERIAL_UNIDADE_1 = [
    ("01.12.0058","Acer","NXJHMAA0015242D7852P00","Sala 18"),
    ("01.12.0001","Lenovo","PF24GVA3","Sala 18"),
    ("01.12.0002","Lenovo","PX003477","Sala 12"),
    ("01.12.0003","Lenovo","PX000155","Sala 18"),
    ("01.12.0004","Lenovo","PF24FZR0","Sala 18"),
    ("01.12.0005","Lenovo","PF24K5ER","Sala 18"),
    ("01.12.0006","Lenovo","PX000909","Sala 18"),
    ("01.12.0008","Lenovo","PX20774","Sala 18"),
    ("01.12.0009","Lenovo","PX001210","Sala 18"),
    ("01.12.0010","Acer","NXHOHAL001909357CA9501","Sala 18"),
    ("01.12.0012","Acer","NXHKPAL0021909F19501","Sala 18"),
    ("01.12.0013","Acer","NXH0HAL00190935E639501","Sala 18"),
    ("01.12.0014","Lenovo","PF255DWQ","Sala 18"),
    ("01.12.0016","Lenovo","P209ZLQ7","Sala 18"),
    ("01.12.0019","Lenovo","P299B2W","Sala 18"),
    ("01.12.0020","Lenovo","PF24K0YM","Sala 18"),
    ("01.12.0021","Lenovo","PF24GAQ3","Sala 18"),
    ("01.12.0022","Lenovo","PF24K4C0","Sala 18"),
    ("01.12.0023","Lenovo","PF2257EZ","Sala 18"),
    ("01.12.0024","Lenovo","PF24HRKH","Sala 18"),
    ("01.12.0025","Lenovo","PF24LB80","Sala 18"),
    ("01.12.0027","Lenovo","P20A4G45","Sala 18"),
    ("01.12.0028","Lenovo","PF25X1J7","Sala 18"),
    ("01.12.0029","Acer","NXHAL001904292AC9501","Sala 13"),
    ("01.12.0030","Acer","NXH0HAL00190428D969501","Sala 18"),
    ("01.12.0031","Acer","NXH0HAL00190428DBA9501","Sala 18"),
    ("01.12.0032","Acer","NXH0HAL00190428D6E9501","Sala 18"),
    ("01.12.0033","Acer","NXH0HAL00192052CDB9501","Sala 18"),
    ("01.12.0034","Lenovo","PF255A0X","Sala 18"),
    ("01.12.0035","Acer","NXH0HAL00192052D2E9501","Sala 18"),
    ("01.12.0036","Lenovo","PX020982","Sala 6"),
    ("01.12.0037","Lenovo","PX021092","Sala 7"),
    ("01.12.0038","Lenovo","PX020770","Sala 18"),
    ("01.12.0039","Lenovo","P2099BV1","Sala 18"),
    ("01.12.0040","Lenovo","PF24GE08","Sala 18"),
    ("01.12.0041","Lenovo","PF24GAR3","Sala 18"),
    ("01.12.0042","Lenovo","PF24HW1P","Sala 18"),
    ("01.12.0043","Lenovo","PF24K31S","Sala 18"),
    ("01.12.0044","Lenovo","PX000015","Sala 9"),
    ("01.12.0045","Acer","NXH0HAL0019205256C9501","Biblioteca"),
    ("01.12.0046","Lenovo","PX004368","Sala 10"),
    ("01.12.0047","Lenovo","PX000982","Sala 8"),
    ("01.12.0048","Lenovo","PF24K03T","Sala 18"),
    ("01.12.0049","Lenovo","PF24GE0L","Sala 18"),
    ("01.12.0050","Lenovo","PF24JCTE","Sala 18"),
    ("01.12.0051","Lenovo","PF24K1DG","Sala 18"),
    ("01.12.0052","Acer","NXH0HAL00192052D1F9501","Sala 4"),
    ("01.12.0053","Lenovo","PF24GGBF","Sala 18"),
    ("01.12.0054","Lenovo","PF24HW3N","Sala 18"),
    ("01.12.0055","Lenovo","PX000704","Sala 18"),
    ("01.12.0056","Lenovo","PX008909","Sala 18"),
    ("01.12.0057","Acer","NXJHRAA001525254A82P00","Sala Maker"),
    ("01.12.0059","Acer","NXH0HAL001920526619501","Sala Prime"),
    ("01.12.0060","Lenovo","PF24K449","Sala 18"),
    ("01.12.0061","Lenovo","PX008652","Sala 5"),
    ("01.12.0062","Lenovo","PF24JJ4S","Sala 4"),
    ("01.12.0063","Acer","NXJHMAA001524306482P00","Sala 18"),
    ("01.12.0064","Lenovo","PF253XQC","Sala 18"),
    ("01.12.0065","Lenovo","PF254FGV","Sala 18"),
]

@app.route("/")
def index():
    hora_atual = datetime.now().hour
    for r in registros:
        if r['status'] == 'Em uso' and hora_atual >= 17:
            r['status'] = 'Não entregou no dia'
    linhas_unidade1 = "".join([f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a,b,c,d in SERIAL_UNIDADE_1])
    html = f"""
    <style>
    body{{font-family:Arial; background:#f2f2f2; padding:20px}}
    .box{{background:white; max-width:1000px; margin:auto; padding:20px; border-radius:10px}}
    input,select{{width:100%; padding:10px; margin:5px 0; box-sizing:border-box; border:1px solid #ccc; border-radius:6px}}
    button{{padding:8px 14px; border:none; border-radius:6px; cursor:pointer}}
    table{{width:100%; border-collapse:collapse; margin-top:15px}}
    th,td{{padding:8px; border-bottom:1px solid #ddd; text-align:center}}
    .badge{{padding:5px 12px; border-radius:20px; font-weight:bold; font-size:13px}}
    details{{margin:15px 0; border:1px solid #ddd; border-radius:8px; padding:10px}}
    summary{{font-weight:bold; cursor:pointer; padding:10px; background:#e11d48; color:white; border-radius:6px}}
    </style>
    <div class="box">
   <div style="display:flex; align-items:center; justify-content:space-between;">
<h3 style="text-align:center">EUCLIDES PLAY</h3>
<img src="/foto" style="width:130px; border-radius:10px;">
</div>
    <a href="/inventario" style="display:block;text-align:center;background:#111;color:#fff;padding:12px;border-radius:8px;text-decoration:none;font-weight:bold;margin:10px 0;">📋 VER INVENTÁRIO DE NOTEBOOKS</a>
    <form action="/cadastrar" method="post">
        <select name="unidade" id="unidadeSelect" onchange="mostrarSerial()" required>
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
        <div id="boxSerialUnidade1" style="display:none; background:#fff5f5; border:2px solid #e11d48; border-radius:8px; padding:12px; margin:10px 0;">
            <b style="color:#e11d48;">🔢 UNIDADE 1 - SERIAL DE TODOS OS CHROMES</b>
            <input id="buscaSerial" oninput="filtrarSerial()" placeholder="Buscar serial, patrimônio..." style="margin-top:8px;">
            <div style="max-height:300px; overflow:auto;">
            <table><thead><tr><th>Patrimônio</th><th>Marca</th><th>Serial</th><th>Sala</th></tr></thead><tbody id="tabelaSerial">{linhas_unidade1}</tbody></table>
            </div>
            <p style="font-size:13px;">Total Unidade 1: <b>59</b> | Falta: 01.12.0007</p>
        </div>
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
    function mostrarSerial(){{
        var u = document.getElementById('unidadeSelect').value;
        var box = document.getElementById('boxSerialUnidade1');
        if(u.includes('Unidade 1')){{ box.style.display='block'; }}
        else{{ box.style.display='none'; }}
    }}
    function filtrarSerial(){{
        var q = document.getElementById('buscaSerial').value.toLowerCase();
        document.querySelectorAll('#tabelaSerial tr').forEach(r=>{{
            r.style.display = r.innerText.toLowerCase().includes(q) ? '' : 'none';
        }});
    }}
    function pintarSelect(){{
        var s = document.getElementById('selectStatus');
        if(s.value == 'Em uso'){{ s.style.background='red'; s.style.color='white'; }}
        if(s.value == 'Devolvido'){{ s.style.background='green'; s.style.color='white'; }}
        if(s.value == 'Manutenção'){{ s.style.background='yellow'; s.style.color='black'; }}
    }}
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

@app.route('/inventario')
def inventario():
    dados = SERIAL_UNIDADE_1
    linhas = "".join([f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a,b,c,d in dados])
    return f"""
    <html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
    <title>Inventário - Euclides Play</title>
    <style>body{{font-family:Arial;background:#0f0f0f;color:#fff;padding:20px}} .box{{background:#1a1a1a;padding:20px;border-radius:12px;max-width:1000px;margin:auto}} input{{width:100%;padding:12px;border-radius:8px;border:1px solid #333;background:#222;color:#fff}} table{{width:100%;border-collapse:collapse;margin-top:10px}} th,td{{padding:10px;border-bottom:1px solid #333;text-align:left}} th{{background:#e11d48}} a{{color:#fff}}</style></head>
    <body><div class='box'><a href='/'>← Voltar</a><h1>Inventário - Notebooks</h1><p>Total: <b id='total'>59</b> | Falta: 01.12.0007</p><input id='busca' placeholder='Buscar por patrimônio, serial, marca...'><div style='overflow-x:auto'><table><thead><tr><th>Patrimônio</th><th>Marca</th><th>Serial</th><th>Sala</th></tr></thead><tbody id='tabela'>{linhas}</tbody></table></div></div>
    <script>const b=document.getElementById('busca'); b.addEventListener('input',()=>{{const q=b.value.toLowerCase(); let n=0; document.querySelectorAll('#tabela tr').forEach(r=>{{const ok=r.innerText.toLowerCase().includes(q); r.style.display=ok?'':'none'; if(ok)n++;}}); document.getElementById('total').textContent=n;}});</script>
    </body></html>
    """

@app.route('/unidade1')
def unidade1():
    linhas = "".join([f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a,b,c,d in SERIAL_UNIDADE_1])
    return f"""
    <html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
    <title>Unidade 1 - Serial de todos os Chromes</title>
    <style>body{{font-family:Arial;background:#0f0f0f;color:#fff;padding:20px}} .box{{background:#1a1a1a;padding:20px;border-radius:12px;max-width:1000px;margin:auto}} input{{width:100%;padding:12px;border-radius:8px;border:1px solid #333;background:#222;color:#fff}} table{{width:100%;border-collapse:collapse;margin-top:10px}} th,td{{padding:10px;border-bottom:1px solid #333;text-align:left}} th{{background:#e11d48}} a{{color:#fff}}</style></head>
    <body><div class='box'><a href='/'>← Voltar</a><h1>UNIDADE 1 - SERIAL DE TODOS OS CHROMES</h1><p>Total: <b id='total'>59</b></p><input id='busca' placeholder='Buscar...'><div style='overflow-x:auto'><table><thead><tr><th>Patrimônio</th><th>Marca</th><th>Serial</th><th>Sala</th></tr></thead><tbody id='tabela'>{linhas}</tbody></table></div></div>
    <script>const b=document.getElementById('busca'); b.addEventListener('input',()=>{{const q=b.value.toLowerCase(); let n=0; document.querySelectorAll('#tabela tr').forEach(r=>{{const ok=r.innerText.toLowerCase().includes(q); r.style.display=ok?'':'none'; if(ok)n++;}}); document.getElementById('total').textContent=n;}});</script>
    </body></html>
    """
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
