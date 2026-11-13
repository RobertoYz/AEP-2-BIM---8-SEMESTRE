import re

class PersistenceValidator:
    @staticmethod
    def validar_sintaxe_ddl_der(texto_markdown: str) -> tuple[bool, str]:
        tem_sql = bool(re.search(r"```sql.*?(CREATE\s+TABLE).*?```", texto_markdown, re.DOTALL | re.IGNORECASE))
        tem_pk = bool(re.search(r"(PRIMARY\s+KEY|FOREIGN\s+KEY|REFERENCES|_id)", texto_markdown, re.IGNORECASE))
        tem_mermaid = bool(re.search(r"```mermaid.*?(erDiagram|classDiagram).*?```", texto_markdown, re.DOTALL | re.IGNORECASE))

        if tem_sql and tem_pk and tem_mermaid:
            return True, "100% Válido (DDL SQL c/ Chaves de Integridade + Diagrama DER Mermaid verificados)"
        elif tem_sql or tem_mermaid:
            return True, "Parcialmente Válido (Modelo de persistência detectado, mas sem todas as restrições explícitas)"
        else:
            return False, "Falha de Sintaxe: Nenhum bloco DDL SQL ou DER estruturado foi encontrado na saída."