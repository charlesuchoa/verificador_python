from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import os

def gerar_relatorio_pdf(dados, arquivo_pdf="relatorios/relatorio_final.pdf"):
    os.makedirs(os.path.dirname(arquivo_pdf), exist_ok=True)
    c = canvas.Canvas(arquivo_pdf, pagesize=A4)
    largura, altura = A4
    y = altura - 2*cm

    def escreve_linha(texto, indent=0):
        nonlocal y
        if y < 2*cm:
            c.showPage()
            y = altura - 2*cm
        c.drawString(2*cm + indent*cm, y, texto)
        y -= 14

    c.setFont("Helvetica-Bold", 16)
    escreve_linha("Relatório de Verificação de Código Python")
    y -= 10

    c.setFont("Helvetica-Bold", 14)
    escreve_linha("Análise Bandit:")
    c.setFont("Helvetica", 11)
    for arquivo, issues in dados.get("bandit", {}).items():
        escreve_linha(f"Arquivo: {arquivo}", indent=0.5)
        for item in issues:
            escreve_linha(f"Linha {item['line_number']}: {item['issue_text']}", indent=1)

    c.setFont("Helvetica-Bold", 14)
    escreve_linha("Análise Flake8:")
    c.setFont("Helvetica", 11)
    for arquivo, issues in dados.get("flake8", {}).items():
        escreve_linha(f"Arquivo: {arquivo}", indent=0.5)
        for item in issues:
            escreve_linha(f"Linha {item['line']}: {item['message']}", indent=1)

    c.setFont("Helvetica-Bold", 14)
    escreve_linha("Verificação Formal:")
    c.setFont("Helvetica", 11)
    for item in dados.get("formal", []):
        if "propriedade" in item:
            escreve_linha(f"{item['propriedade']}: {item['resultado']}", indent=0.5)
        elif "assert" in item:
            escreve_linha(f"[assert] {item['assert']}: {item['resultado']}", indent=0.5)
        elif "erro" in item:
            escreve_linha(f"Erro: {item['erro']}", indent=0.5)
        else:
            escreve_linha(str(item), indent=0.5)

    c.save()
    print(f"Relatório PDF salvo em: {arquivo_pdf}")
