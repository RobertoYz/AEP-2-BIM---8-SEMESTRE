import re
import json
import hashlib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TokenOptimizer:
    CACHE_FILE = os.path.join(BASE_DIR, "token_cache.json")

    @staticmethod
    def comprimir_requisitos(texto: str) -> str:
        """
        Remove ruídos de extração de PDF, múltiplos espaços e linhas vazias
        para economizar tokens de entrada (Input Tokens).
        """
        texto = re.sub(r'P[áa]gina\s+\d+\s+de\s+\d+', '', texto, flags=re.IGNORECASE)
        texto = re.sub(r'[ \t]+', ' ', texto)
        texto = re.sub(r'^\s*[\d\W]+\s*$', '', texto, flags=re.MULTILINE)
        texto = re.sub(r'\n\s*\n+', '\n', texto)
        return texto.strip()

    @staticmethod
    def gerar_hash(escopo: str, texto_comprimido: str) -> str:
        conteudo = f"{escopo}:{texto_comprimido}"
        return hashlib.sha256(conteudo.encode('utf-8')).hexdigest()

    @classmethod
    def buscar_cache(cls, chave_hash: str) -> dict | None:
        if not os.path.exists(cls.CACHE_FILE):
            return None
        try:
            with open(cls.CACHE_FILE, 'r', encoding='utf-8') as f:
                cache = json.load(f)
                return cache.get(chave_hash)
        except Exception:
            return None

    @classmethod
    def salvar_cache(cls, chave_hash: str, resposta: str, tokens_in: int, tokens_out: int):
        cache = {}
        if os.path.exists(cls.CACHE_FILE):
            try:
                with open(cls.CACHE_FILE, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
            except Exception:
                cache = {}

        cache[chave_hash] = {
            "resposta": resposta,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out
        }
        with open(cls.CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
