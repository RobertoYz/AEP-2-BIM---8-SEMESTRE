import time
from abc import ABC, abstractmethod
from google import genai
from google.genai import types


class LLMProvider(ABC):
    @abstractmethod
    def gerar_resposta(self, system_instruction: str, prompt: str) -> tuple[str, int, int]:
        pass


class GeminiClient(LLMProvider):
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def _obter_modelos_disponiveis(self) -> list[str]:
        """Descobre automaticamente quais modelos Gemini estão liberados na chave de API."""
        preferidos = [
            "gemini-2.5-flash",
            "gemini-2.0-flash",
            "gemini-2.5-pro",
            "gemini-1.5-flash",
        ]
        descobertos = []
        try:
            for m in self.client.models.list():
                nome = m.name.replace("models/", "")
                if (
                    "gemini" in nome
                    and ("flash" in nome or "pro" in nome)
                    and "vision" not in nome
                    and "embedding" not in nome
                    and "tts" not in nome
                    and "image" not in nome
                ):
                    descobertos.append(nome)
        except Exception:
            pass

        lista_final = []
        for p in preferidos:
            if p in descobertos and p not in lista_final:
                lista_final.append(p)
        for d in descobertos:
            if d not in lista_final:
                lista_final.append(d)
        for p in preferidos:
            if p not in lista_final:
                lista_final.append(p)
        return lista_final

    def gerar_resposta(self, system_instruction: str, prompt: str) -> tuple[str, int, int]:
        modelos = self._obter_modelos_disponiveis()
        ultimo_erro = None

        for modelo in modelos:
            for tentativa in range(1, 4):
                try:
                    response = self.client.models.generate_content(
                        model=modelo,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.2,
                            max_output_tokens=2500,
                        ),
                    )
                    tokens_in = getattr(response.usage_metadata, "prompt_token_count", 0) or 0
                    tokens_out = getattr(response.usage_metadata, "candidates_token_count", 0) or 0
                    return response.text, tokens_in, tokens_out

                except Exception as e:
                    erro_str = str(e)
                    ultimo_erro = e
                    if "503" in erro_str or "UNAVAILABLE" in erro_str or "429" in erro_str:
                        time.sleep(2 * tentativa)
                        continue
                    elif "404" in erro_str or "NOT_FOUND" in erro_str or "400" in erro_str:
                        break
                    else:
                        raise e

        raise RuntimeError(f"Servidor da API indisponível no momento. Último erro: {ultimo_erro}")


class MockOpenAIClient(LLMProvider):
    def gerar_resposta(self, system_instruction: str, prompt: str) -> tuple[str, int, int]:
        return (
            "# ADR Simulado\n```sql\nCREATE TABLE teste (id INT PRIMARY KEY);\n```\n```mermaid\nerDiagram\n```",
            15,
            25,
        )


class LLMFactory:
    @staticmethod
    def criar_cliente(provedor: str, api_key: str) -> LLMProvider:
        if provedor.lower() == "gemini":
            return GeminiClient(api_key)
        elif provedor.lower() == "openai":
            return MockOpenAIClient()
        raise ValueError(f"Provedor '{provedor}' não suportado.")
