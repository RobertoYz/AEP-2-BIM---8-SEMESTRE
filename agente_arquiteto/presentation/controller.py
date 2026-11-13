import time
from rich.prompt import Prompt
from presentation.view import CLIView
from domain.adapter import FileAdapter
from domain.strategy import ArchitectureStrategy
from domain.validator import PersistenceValidator
from domain.optimizer import TokenOptimizer
from infrastructure.llm_factory import LLMFactory


class ArchitectController:
    def __init__(self, api_key: str, provedor: str = "gemini"):
        self.view = CLIView()
        self.llm_client = LLMFactory.criar_cliente(provedor, api_key)

    def executar_fluxo(self):
        arquivos = FileAdapter.listar_arquivos_entrada()
        self.view.exibir_cabecalho(arquivos)

        padrao_arq = arquivos[0] if arquivos else "req_teste_01.txt"
        caminho = Prompt.ask(
            "\n[bold yellow]1. Arquivo de requisitos (.pdf/.txt) em ARTEFATOS_AQUI[/bold yellow]",
            default=padrao_arq,
        )
        escopo = Prompt.ask(
            "[bold yellow]2. Strategy de Arquitetura[/bold yellow]",
            choices=["completa", "persistencia"],
            default="completa",
        )

        try:
            inicio = time.time()

            # 1. Extração da pasta ARTEFATOS_AQUI e Compressão Local de Tokens
            texto_bruto = FileAdapter.extrair_texto(caminho)
            texto_comprimido = TokenOptimizer.comprimir_requisitos(texto_bruto)

            tam_bruto = max(len(texto_bruto), 1)
            economia_pct = ((tam_bruto - len(texto_comprimido)) / tam_bruto) * 100

            # 2. Verificação de Cache SHA-256 (Custo Zero em Re-execuções)
            chave_hash = TokenOptimizer.gerar_hash(escopo, texto_comprimido)
            dados_cache = TokenOptimizer.buscar_cache(chave_hash)

            if dados_cache:
                resposta_bruta = dados_cache["resposta"]
                tokens_in = dados_cache["tokens_in"]
                tokens_out = dados_cache["tokens_out"]
                usou_cache = True
            else:
                estrategia = ArchitectureStrategy.selecionar_estrategia(escopo)
                sys_inst = estrategia.obter_system_instruction()
                prompt = estrategia.construir_prompt(texto_comprimido)

                with self.view.console.status(
                    "[bold green]Consultando Gemini API e gerando artefatos...",
                    spinner="earth",
                ):
                    resposta_bruta, tokens_in, tokens_out = self.llm_client.gerar_resposta(
                        sys_inst, prompt
                    )
                TokenOptimizer.salvar_cache(chave_hash, resposta_bruta, tokens_in, tokens_out)
                usou_cache = False

            # 3. Validação Determinística (SQL DDL + DER Mermaid)
            validacao = PersistenceValidator.validar_sintaxe_ddl_der(resposta_bruta)
            tempo_total = time.time() - inicio

            adr_model = FileAdapter.adaptar_para_adr(
                origem=caminho,
                escopo=escopo,
                resposta_bruta=resposta_bruta,
                validacao=validacao,
                tempo=tempo_total,
                tokens_in=tokens_in,
                tokens_out=tokens_out,
                economia_pct=economia_pct,
                usou_cache=usou_cache,
            )

            # 4. Exibição e Exportação Automática na pasta ARTEFATOS_AQUI
            self.view.exibir_resultado(adr_model)

        except Exception as e:
            self.view.console.print(f"\n[bold red]❌ Erro:[/bold red] {e}")
