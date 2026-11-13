from dataclasses import dataclass

@dataclass
class ADRModel:
    arquivo_origem: str
    escopo_selecionado: str
    conteudo_markdown: str
    sql_valido: bool
    detalhes_validacao: str
    tempo_resposta: float
    tokens_entrada: int
    tokens_saida: int
    economia_chars_pct: float
    usou_cache: bool