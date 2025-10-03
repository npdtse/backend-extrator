import os
import tempfile
import pandas as pd
import io
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS 

from extrator import extrair_dados_modelo_ge

app = Flask(__name__)
CORS(app)  # <--- 2. HABILITE O CORS PARA TODA A APLICAÇÃO

@app.route('/api/extract-and-download', methods=['POST'])
def upload_e_download():
    # ... O RESTO DO SEU CÓDIGO CONTINUA EXATAMENTE O MESMO ...
    # ... (não precisa mudar mais nada aqui) ...
    # 1. Validação do arquivo enviado
    if 'file' not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400

    arquivo = request.files['file']

    if arquivo.filename == '' or not arquivo.filename.lower().endswith('.pdf'):
        return jsonify({"erro": "Arquivo inválido, por favor envie um PDF"}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        arquivo.save(temp_pdf.name)
        caminho_temporario = temp_pdf.name

    dados_extraidos = []
    try:
        dados_extraidos = extrair_dados_modelo_ge(caminho_temporario)
    finally:
        os.remove(caminho_temporario)

    if not dados_extraidos:
        return jsonify({"erro": "Nenhum dado foi extraído. Verifique se o PDF corresponde ao modelo da GE Serviços."}), 404

    try:
        df = pd.DataFrame(dados_extraidos)
        output_buffer = io.BytesIO()
        df.to_excel(output_buffer, index=False, engine='openpyxl')
        output_buffer.seek(0)

        return send_file(
            output_buffer,
            download_name="dados_extraidos.xlsx",
            as_attachment=True,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        return jsonify({"erro": f"Falha ao gerar a planilha: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)