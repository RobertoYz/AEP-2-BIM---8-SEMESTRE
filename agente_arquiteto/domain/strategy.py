from abc import ABC, abstractmethod

class PromptStrategy(ABC):
    @abstractmethod
    def obter_system_instruction(self) -> str:
        pass

    @abstractmethod
    def construir_prompt(self, requisitos: str) -> str:
        pass

class ArquiteturaCompletaStrategy(PromptStrategy):
    def obter_system_instruction(self) -> str:
        return (
            "Você é o Agente Arquiteto (ODS 9). Seja direto, técnico e conciso. "
            "Proibido textos introdutórios ou conclusões genéricas. Gere apenas o ADR em Markdown:\n"
            "1. Estilo Arquitetural (1 parágrafo de justificativa).\n"
            "2. Tabela de Padrões: 1 GoF Criação, 1 Estrutural, 1 Comportamental, 2 GRASP (inclua Repository/Information Expert).\n"
            "3. Bloco ```sql com CREATE TABLE (PK e FK obrigatórias).\n"
            "4. Bloco ```mermaid com erDiagram compacto.\n"
            "5. Trade-offs em bullet points curtos."
        )

    def construir_prompt(self, requisitos: str) -> str:
        return f"REQUISITOS:\n{requisitos}"

class PersistenciaFocadaStrategy(PromptStrategy):
    def obter_system_instruction(self) -> str:
        return (
            "Você é o Arquiteto de Dados (ODS 9). Seja estritamente técnico e conciso.\n"
            "1. Explique em 3 linhas o isolamento via Repository e Information Expert.\n"
            "2. Gere bloco ```sql com CREATE TABLE (PK/FK).\n"
            "3. Gere bloco ```mermaid com erDiagram."
        )

    def construir_prompt(self, requisitos: str) -> str:
        return f"REGRA DE DADOS:\n{requisitos}"

class ArchitectureStrategy:
    @staticmethod
    def selecionar_estrategia(tipo: str) -> PromptStrategy:
        if tipo == "persistencia":
            return PersistenciaFocadaStrategy()
        return ArquiteturaCompletaStrategy()