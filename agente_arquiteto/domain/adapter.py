import os
import PyPDF2
from domain.models import ADRModel

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_ARTEFATOS = os.path.join(BASE_DIR, "ARTEFATOS_AQUI")


class FileAdapter:
    @staticmethod
    def obter_pasta_artefatos() -> str:
        os.makedirs(PASTA_ARTEFATOS, exist_ok=True)
        return PASTA_ARTEFATOS

    @staticmethod
    def listar_arquivos_entrada() -> list[str]:
        pasta = FileAdapter.obter_pasta_artefatos()
        arquivos = []
        for nome in sorted(os.listdir(pasta)):
            if nome.lower().endswith((".pdf", ".txt")) and not nome.startswith("ADR_"):
                arquivos.append(nome)
        return arquivos

    @staticmethod
    def resolver_caminho_entrada(caminho_arquivo: str) -> str:
        limpo = caminho_arquivo.strip().strip('"').strip("'")
        pasta = FileAdapter.obter_pasta_artefatos()

        candidatos = [
            os.path.join(pasta, limpo),
            os.path.join(pasta, os.path.basename(limpo)),
            limpo,
            os.path.join(BASE_DIR, limpo),
        ]
        for candidato in candidatos:
            if os.path.isfile(candidato):
                return candidato

        raise FileNotFoundError(
            f"Arquivo '{limpo}' não encontrado na pasta 'ARTEFATOS_AQUI' ({pasta})."
        )

    @staticmethod
    def extrair_texto(caminho_arquivo: str) -> str:
        caminho_real = FileAdapter.resolver_caminho_entrada(caminho_arquivo)
        _, extensao = os.path.splitext(caminho_real)

        if extensao.lower() == ".pdf":
            texto = ""
            with open(caminho_real, "rb") as f:
                leitor = PyPDF2.PdfReader(f)
                for pagina in leitor.pages:
                    texto_pag = pagina.extract_text()
                    if texto_pag:
                        texto += texto_pag + "\n"
            return texto.strip()

        elif extensao.lower() == ".txt":
            with open(caminho_real, "r", encoding="utf-8") as f:
                return f.read().strip()
        else:
            raise ValueError(
                "Formato inválido. O Agente Arquiteto aceita apenas .pdf ou .txt"
            )

    @staticmethod
    def adaptar_para_adr(
        origem: str,
        escopo: str,
        resposta_bruta: str,
        validacao: tuple[bool, str],
        tempo: float,
        tokens_in: int = 0,
        tokens_out: int = 0,
        economia_pct: float = 0.0,
        usou_cache: bool = False,
    ) -> ADRModel:
        valido, msg = validacao
        nome_limpo = os.path.basename(origem.strip().strip('"').strip("'"))
        return ADRModel(
            arquivo_origem=nome_limpo,
            escopo_selecionado=escopo,
            conteudo_markdown=resposta_bruta,
            sql_valido=valido,
            detalhes_validacao=msg,
            tempo_resposta=tempo,
            tokens_entrada=tokens_in,
            tokens_saida=tokens_out,
            economia_chars_pct=max(0.0, economia_pct),
            usou_cache=usou_cache,
        )
