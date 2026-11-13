import csv
import json
import os
import re
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from domain.models import ADRModel
from domain.adapter import FileAdapter


class CLIView:
    NOME_CSV = "metricas_testes_arquiteto.csv"
    NOME_HTML = "Painel_Graficos_e_DER.html"

    def __init__(self):
        self.console = Console()

    def exibir_cabecalho(self, arquivos_disponiveis: list[str] | None = None):
        self.console.clear()
        self.console.print(
            Panel.fit(
                "[bold green]🏢 Agente Arquiteto — Escola de TI (ODS 9)[/bold green]\n"
                "[dim]Arquitetura em Camadas | GoF & GRASP | Validador Determinístico DDL/DER[/dim]\n"
                "[dim]Leitura e Exportação Automática em: ARTEFATOS_AQUI/ (.md, .sql, .mmd, .csv, .html)[/dim]",
                border_style="green",
            )
        )
        if arquivos_disponiveis:
            lista_str = " | ".join(f"[cyan]{arq}[/cyan]" for arq in arquivos_disponiveis)
            self.console.print(f"📂 [bold]Artefatos em ARTEFATOS_AQUI/:[/bold] {lista_str}")

    def exibir_resultado(self, adr: ADRModel):
        pasta_artefatos = FileAdapter.obter_pasta_artefatos()
        nome_sem_ext = os.path.splitext(os.path.basename(adr.arquivo_origem))[0]
        sufixo = f"{nome_sem_ext}_{adr.escopo_selecionado}"

        nome_md = f"ADR_{sufixo}.md"
        nome_sql = f"DDL_{sufixo}.sql"
        nome_mmd = f"DER_{sufixo}.mmd"

        caminho_md = os.path.join(pasta_artefatos, nome_md)
        caminho_sql = os.path.join(pasta_artefatos, nome_sql)
        caminho_mmd = os.path.join(pasta_artefatos, nome_mmd)
        caminho_csv = os.path.join(pasta_artefatos, self.NOME_CSV)
        caminho_html = os.path.join(pasta_artefatos, self.NOME_HTML)

        # 1. Salva o ADR completo em Markdown (.md) dentro de ARTEFATOS_AQUI
        with open(caminho_md, "w", encoding="utf-8") as f:
            f.write(adr.conteudo_markdown)

        # 2. Extrai e salva o Script DDL isolado (.sql) dentro de ARTEFATOS_AQUI
        match_sql = re.search(
            r"```sql\s*(.*?)\s*```", adr.conteudo_markdown, re.DOTALL | re.IGNORECASE
        )
        conteudo_sql = match_sql.group(1).strip() if match_sql else "-- Nenhum bloco SQL detectado"
        with open(caminho_sql, "w", encoding="utf-8") as f:
            f.write(conteudo_sql + "\n")

        # 3. Extrai e salva o Diagrama DER isolado (.mmd) dentro de ARTEFATOS_AQUI
        match_der = re.search(
            r"```mermaid\s*(.*?)\s*```", adr.conteudo_markdown, re.DOTALL | re.IGNORECASE
        )
        conteudo_der = match_der.group(1).strip() if match_der else "erDiagram"
        with open(caminho_mmd, "w", encoding="utf-8") as f:
            f.write(conteudo_der + "\n")

        # 4. Atualiza automaticamente a Planilha CSV de Métricas dentro de ARTEFATOS_AQUI
        linhas_existentes = []
        cabecalho = [
            "Caso_Teste",
            "Arquivo_Entrada",
            "Strategy_GoF",
            "Tempo_Resposta_s",
            "Status_Validacao_SQL_DER",
            "Compressao_Ruido_Pct",
            "Tokens_Entrada",
            "Tokens_Saida",
            "Tokens_Total",
            "Origem_Dados",
            "ADR_Markdown",
            "Script_SQL",
            "Diagrama_Mermaid",
        ]
        if os.path.exists(caminho_csv):
            try:
                with open(caminho_csv, "r", encoding="utf-8-sig", newline="") as csvfile:
                    reader = list(csv.reader(csvfile, delimiter=";"))
                    if len(reader) > 1:
                        linhas_existentes = reader[1:]
            except Exception:
                linhas_existentes = []

        num_teste = len(linhas_existentes) + 1
        nova_linha = [
            str(num_teste),
            adr.arquivo_origem,
            adr.escopo_selecionado,
            f"{adr.tempo_resposta:.2f}",
            "APROVADO (100%)" if adr.sql_valido else "REPROVADO",
            f"{adr.economia_chars_pct:.1f}%",
            str(adr.tokens_entrada),
            str(adr.tokens_saida),
            str(adr.tokens_entrada + adr.tokens_saida),
            "CACHE_LOCAL" if adr.usou_cache else "API_GEMINI",
            nome_md,
            nome_sql,
            nome_mmd,
        ]
        linhas_existentes.append(nova_linha)

        with open(caminho_csv, "w", newline="", encoding="utf-8-sig") as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            writer.writerow(cabecalho)
            writer.writerows(linhas_existentes)

        # 5. Gera/Atualiza automaticamente o Painel Visual HTML (Gráficos + Diagramas DER)
        self._atualizar_painel_html(pasta_artefatos, caminho_html, linhas_existentes)

        # 6. Exibe a tabela de métricas no terminal (CLI Rich)
        tabela = Table(title="📊 Métricas de Execução do Caso de Teste (Entrega 2)")
        tabela.add_column("Métrica / Critério", style="cyan")
        tabela.add_column("Resultado Obtido", style="magenta")

        tabela.add_row("Arquivo de Entrada (ARTEFATOS_AQUI)", adr.arquivo_origem)
        tabela.add_row("Estratégia Aplicada (GoF Strategy)", adr.escopo_selecionado)
        tabela.add_row("Tempo de Resposta", f"{adr.tempo_resposta:.2f} segundos")

        status_cor = (
            "[bold green]APROVADO[/bold green]"
            if adr.sql_valido
            else "[bold red]REPROVADO[/bold red]"
        )
        tabela.add_row(
            "Validação Determinística (SQL/DER)", f"{status_cor} - {adr.detalhes_validacao}"
        )
        tabela.add_row(
            "Artefatos Criados em ARTEFATOS_AQUI/",
            f"{nome_md} | {nome_sql} | {nome_mmd}",
        )
        tabela.add_row(
            "Planilha CSV e Painel de Gráficos/DER",
            f"{self.NOME_CSV} | {self.NOME_HTML}",
        )

        origem_resp = (
            "[bold cyan]CACHE LOCAL (0 Tokens gastos agora)[/bold cyan]"
            if adr.usou_cache
            else "API Remota (Gemini)"
        )
        tabela.add_row("Origem da Resposta", origem_resp)
        tabela.add_row(
            "Compressão Pré-Prompt", f"{adr.economia_chars_pct:.1f}% de ruído removido"
        )
        tabela.add_row(
            "Consumo de Tokens",
            f"In: {adr.tokens_entrada} | Out: {adr.tokens_saida} | Total: {adr.tokens_entrada + adr.tokens_saida}",
        )

        self.console.print("\n")
        self.console.print(tabela)
        self.console.print("\n[bold yellow]📄 Prévia do ADR Gerado:[/bold yellow]")
        self.console.print(Panel(Markdown(adr.conteudo_markdown), border_style="blue"))

    def _atualizar_painel_html(
        self, pasta_artefatos: str, caminho_html: str, linhas_csv: list[list[str]]
    ):
        labels = []
        tempos = []
        tokens_in = []
        tokens_out = []
        blocos_der_html = []

        for linha in linhas_csv:
            if len(linha) < 13:
                continue
            num, arq, strat, tempo_s, _, _, t_in, t_out, _, _, _, _, arq_mmd = linha
            rotulo = f"Teste {num}: {arq} ({strat})"
            labels.append(rotulo)
            try:
                tempos.append(float(tempo_s))
            except ValueError:
                tempos.append(0.0)
            try:
                tokens_in.append(int(t_in))
            except ValueError:
                tokens_in.append(0)
            try:
                tokens_out.append(int(t_out))
            except ValueError:
                tokens_out.append(0)

            caminho_mmd = os.path.join(pasta_artefatos, arq_mmd)
            codigo_mmd = "erDiagram"
            if os.path.exists(caminho_mmd):
                try:
                    with open(caminho_mmd, "r", encoding="utf-8") as fm:
                        codigo_mmd = fm.read().strip()
                except Exception:
                    pass

            blocos_der_html.append(
                f'<div class="der-item"><h4>{rotulo}</h4><div class="mermaid">\n{codigo_mmd}\n</div></div>'
            )

        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Gráficos e Diagramas DER - Agente Arquiteto (Entrega 2)</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
</script>
<style>
body {{ font-family: Segoe UI, sans-serif; background: #f4f6f9; padding: 20px; color: #222; }}
.card {{ background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 30px; max-width: 1000px; margin-left: auto; margin-right: auto; }}
h2 {{ color: #1b5e20; border-bottom: 2px solid #1b5e20; padding-bottom: 8px; }}
.der-box {{ display: flex; gap: 20px; flex-wrap: wrap; justify-content: space-around; }}
.der-item {{ border: 1px solid #ddd; padding: 15px; border-radius: 6px; background: #fafafa; width: 45%; overflow-x: auto; }}
</style>
</head>
<body>
<div class="card">
<h2>Gráfico 1: Tempo de Resposta (s) por Caso de Teste — Agente Arquiteto</h2>
<canvas id="graficoTempo" height="110"></canvas>
</div>
<div class="card">
<h2>Gráfico 2: Consumo de Tokens (Entrada vs. Saída) por Caso de Teste</h2>
<canvas id="graficoTokens" height="110"></canvas>
</div>
<div class="card">
<h2>Diagramas Entidade-Relacionamento (DER) Gerados Automaticamente</h2>
<div class="der-box">
{''.join(blocos_der_html)}
</div>
</div>
<script>
const labels = {json.dumps(labels, ensure_ascii=False)};
const tempos = {json.dumps(tempos)};
const tokensIn = {json.dumps(tokens_in)};
const tokensOut = {json.dumps(tokens_out)};

new Chart(document.getElementById('graficoTempo'), {{
  type: 'bar',
  data: {{
    labels: labels,
    datasets: [{{
      label: 'Tempo de Execução (Segundos)',
      data: tempos,
      backgroundColor: ['#2e7d32', '#1565c0', '#6a1b9a', '#ef6c00', '#00838f', '#c62828']
    }}]
  }}
}});

new Chart(document.getElementById('graficoTokens'), {{
  type: 'bar',
  data: {{
    labels: labels,
    datasets: [
      {{ label: 'Tokens de Entrada (Input)', data: tokensIn, backgroundColor: '#1976d2' }},
      {{ label: 'Tokens de Saída (ADR Gerado)', data: tokensOut, backgroundColor: '#43a047' }}
    ]
  }}
}});
</script>
</body>
</html>
"""
        with open(caminho_html, "w", encoding="utf-8") as f:
            f.write(html)
