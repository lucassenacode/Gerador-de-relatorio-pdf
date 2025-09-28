import json
import sys
import os 

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML  # <-- NOVO: Importar a biblioteca WeasyPrint


def generate_report():
    """
    Carrega os dados de um arquivo JSON e renderiza o template,
    salvando o resultado em um arquivo HTML e também em um PDF.
    """
    print("Iniciando a geração do relatório local...")

    # --- (Seção de carregar o JSON - sem alterações) ---
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            dados_completos = json.load(f)
        print("-> Arquivo data.json carregado com sucesso.")
    except FileNotFoundError:
        print("[ERRO] Arquivo 'data.json' não encontrado.")
        return
    except json.JSONDecodeError:
        print("[ERRO] O arquivo 'data.json' contém um erro de formatação.")
        return

    # --- (Seção para definir o nome do arquivo - sem alterações) ---
    report_data_final = {}
    nome_arquivo_saida_html = "relatorio_full-report.html"

    if len(sys.argv) > 1:
        tipo_relatorio_especifico = sys.argv[1]
        print(f"--> Solicitado relatório específico: '{tipo_relatorio_especifico}'")
        dados_originais = dados_completos.get("report_data", {})
        if tipo_relatorio_especifico in dados_originais:
            report_data_final[tipo_relatorio_especifico] = dados_originais[
                tipo_relatorio_especifico
            ]
            nome_arquivo_saida_html = f"relatorio_{tipo_relatorio_especifico}.html"
        else:
            print(
                f"[AVISO] Tipo de relatório '{tipo_relatorio_especifico}' não encontrado. Gerando relatório completo."
            )
            report_data_final = dados_originais
    else:
        print("--> Gerando relatório completo.")
        report_data_final = dados_completos.get("report_data", {})

    # --- (Seção de renderização do HTML - sem alterações) ---
    env = Environment(loader=FileSystemLoader("templates/"))
    template = env.get_template("project_report.html")
    print("-> Template 'project_report.html' carregado.")

    contexto = {
    "project_name": dados_completos.get("project_name"),
    "client_logo_url": dados_completos.get("client_logo_url"),
    "company_logo_url": dados_completos.get("company_logo_url"),
    "main_cover_image_url": dados_completos.get("main_cover_image_url"),
    "report_data": report_data_final,
    }

    html_renderizado = template.render(contexto)
    print("-> Template renderizado com os dados.")

    # --- Salvar o arquivo HTML (sem alterações) ---
    with open(nome_arquivo_saida_html, "w", encoding="utf-8") as f:
        f.write(html_renderizado)
    print(f"-> Relatório HTML salvo como '{nome_arquivo_saida_html}'.")

    # --- NOVO: Seção para gerar e salvar o PDF ---
    print("-> Gerando arquivo PDF...")

    # CORREÇÃO: Definir base_url antes de usar
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Define o nome do arquivo PDF com base no nome do HTML
    nome_arquivo_saida_pdf = nome_arquivo_saida_html.replace(".html", ".pdf")

    # Cria o objeto HTML do WeasyPrint a partir da string renderizada
    # O base_url é fundamental para que as imagens (ex: logo) apareçam no PDF
    html_para_pdf = HTML(string=html_renderizado, base_url=BASE_DIR)

    # Escreve o PDF no arquivo
    html_para_pdf.write_pdf(nome_arquivo_saida_pdf)

    print(f"-> Relatório PDF salvo como '{nome_arquivo_saida_pdf}'.")
    print("\n[SUCESSO] Arquivos HTML e PDF gerados.")


if __name__ == "__main__":
    generate_report()
