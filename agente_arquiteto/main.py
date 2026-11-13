import os
from presentation.controller import ArchitectController

if __name__ == "__main__":
    # Defina no terminal ou substitua "COLE_SUA_CHAVE_AQUI" pela sua chave do Google AI Studio
    API_KEY = os.getenv("GEMINI_API_KEY", "COLE_SUA_CHAVE_AQUI")

    if API_KEY == "COLE_SUA_CHAVE_AQUI" or not API_KEY.strip():
        print("⚠️ Configure sua GEMINI_API_KEY no arquivo agente_arquiteto/main.py (linha 6) antes de rodar!")
    else:
        controller = ArchitectController(api_key=API_KEY, provedor="gemini")
        controller.executar_fluxo()
