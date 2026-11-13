# 🏢 Agente Arquiteto — Escola de TI (ODS 9)

Repositório oficial da implementação e testes do **Agente Arquiteto**, desenvolvido para a **Atividade de Estudo Programado (AEP)** do 8º Semestre do curso de **Engenharia de Software (UniCesumar — Turma ESOFT8S-A)**.

O **Agente Arquiteto** atua na fase de concepção técnica do software e na arquitetura de persistência de dados, lendo documentos de requisitos e regras de negócio (`.pdf` ou `.txt`) na pasta `ARTEFATOS_AQUI/` e gerando **automaticamente** na mesma pasta:
1. **Documento de Decisão Arquitetural (ADR)** estruturado em Markdown (`ADR_<arquivo>_<strategy>.md`) com recomendação de Estilo Arquitetural, Tabela de Padrões GoF e GRASP, Script DDL, Diagrama DER e Trade-offs;
2. **Script físico de Banco de Dados SQL (DDL)** isolado (`DDL_<arquivo>_<strategy>.sql`);
3. **Diagrama Entidade-Relacionamento (DER)** em sintaxe Mermaid (`DER_<arquivo>_<strategy>.mmd`);
4. **Planilha de Métricas e Estatísticas** em formato CSV (`metricas_testes_arquiteto.csv`);
5. **Painel Visual HTML** (`Painel_Graficos_e_DER.html`) com gráficos de barras de desempenho/tokens e diagramas DER renderizados.

---

## 👥 Integrantes da Equipe (Turma ESOFT8S-A)
* **Ademar de Araújo Teisen** — RA: 23182969-2
* **Pedro Emanuel Ferreira de Andrade** — RA: 23167567-2
* **Roberto Yanez Sanz** — RA: 23079491-2

---

## 📂 Estrutura de Pastas do Projeto

```text
agente_arquiteto/
│
├── main.py                      # Ponto de entrada (CLI) e configuração da API Key do Google Gemini
├── requirements.txt             # Dependências do projeto (rich, google-genai, PyPDF2)
│
├── ARTEFATOS_AQUI/              # PASTA CENTRAL DE ENTRADA E SAÍDA AUTOMÁTICA DO AGENTE
│   ├── Artefato - Helpflow.pdf  # Entrada Teste 1 (Plataforma de Atendimento e SLA)
│   ├── Artefato - HealthSync.pdf# Entrada Testes 2 e 3 (Plataforma Hospitalar e Telemedicina)
│   ├── Artefato - Forgetwin.pdf # Entrada Teste 4 (Manufatura Inteligente e IIoT - ODS 9)
│   ├── borda_vago.txt           # Entrada Teste 5 (Cenário de Borda - Requisito Mínimo)
│   ├── req_teste_01.txt         # Requisito acadêmico complementar
│   ├── ADR_*.md                 # [Gerado Automaticamente] Documentos de Decisão Arquitetural
│   ├── DDL_*.sql                # [Gerado Automaticamente] Scripts SQL DDL com PK e FK
│   ├── DER_*.mmd                # [Gerado Automaticamente] Diagramas Entidade-Relacionamento Mermaid
│   ├── metricas_testes_arquiteto.csv # [Gerado Automaticamente] Planilha de métricas dos testes
│   └── Painel_Graficos_e_DER.html    # [Gerado Automaticamente] Gráficos e Diagramas DER visuais
│
├── presentation/                # CAMADA DE APRESENTAÇÃO (CLI / MVC View & Controller)
│   ├── controller.py            # GRASP Controller (ArchitectController)
│   └── view.py                  # MVC View (Rich CLI + Exportador Automático em ARTEFATOS_AQUI)
│
├── domain/                      # CAMADA DE DOMÍNIO (Regras de Negócio e Núcleo Determinístico)
│   ├── models.py                # MVC Model (ADRModel)
│   ├── adapter.py               # GoF Adapter (Leitura de PDF/TXT da pasta ARTEFATOS_AQUI)
│   ├── strategy.py              # GoF Strategy ('completa' vs 'persistencia')
│   ├── validator.py             # GRASP Information Expert (Validador determinístico Regex SQL/DER)
│   └── optimizer.py             # Compressor de ruído pré-prompt e Cache SHA-256
│
└── infrastructure/              # CAMADA DE INFRAESTRUTURA (Comunicação Externa)
    └── llm_factory.py           # GoF Factory Method + GRASP Baixo Acoplamento (Cliente Gemini API)
```

---

## 🛠️ Como Instalar e Executar o Projeto (Passo a Passo)

### 1. Instalar o Python
1. Baixe e instale o **Python 3.11 ou superior (recomendado Python 3.13)** em [python.org/downloads](https://www.python.org/downloads/).
2. **Importante (Windows):** Na primeira tela do instalador, marque obrigatoriamente a caixa **"Add python.exe to PATH"** antes de clicar em *Install Now*.

### 2. Clonar o Repositório e Acessar a Pasta do Agente
Abra o terminal de sua preferência (**CMD / Prompt de Comando** ou **PowerShell** / terminal do VS Code com `Ctrl + '`) e acesse a pasta `agente_arquiteto`:

**No CMD (Prompt de Comando) ou PowerShell:**
```cmd
git clone https://github.com/RobertoYz/AEP-2-BIM---8-SEMESTRE.git
cd AEP-2-BIM---8-SEMESTRE\agente_arquiteto
```

### 3. Instalar as Bibliotecas Necessárias
Dentro da pasta `agente_arquiteto`, instale as bibliotecas do Python (`rich`, `google-genai` e `PyPDF2`):

**No CMD (Prompt de Comando) ou PowerShell:**
```cmd
python -m pip install -r requirements.txt
```
*(Ou instale diretamente com: `python -m pip install rich google-genai PyPDF2`)*

---

### 4. ⚠️ Configurar a Chave da API do Google Gemini (`main.py`)
Por motivos de segurança, a chave da API não fica salva publicamente no repositório. Para rodar o agente:

1. Gere uma chave de API gratuita no [Google AI Studio](https://aistudio.google.com/).
2. **Opção A — Direto no arquivo `agente_arquiteto/main.py` (Recomendado):**
   Abra o arquivo **`agente_arquiteto/main.py`** e, na **linha 6**, substitua `"COLE_SUA_CHAVE_AQUI"` pela sua chave da API:
   ```python
   API_KEY = os.getenv("GEMINI_API_KEY", "SUA_CHAVE_AQUI")
   ```
3. **Opção B — Via variável de ambiente no terminal (sem editar o arquivo):**
   * **No CMD (Prompt de Comando):**
     ```cmd
     set GEMINI_API_KEY=SUA_CHAVE_AQUI
     ```
   * **No PowerShell:**
     ```powershell
     $env:GEMINI_API_KEY="SUA_CHAVE_AQUI"
     ```

---

### 5. Colocar os Documentos de Entrada na Pasta `ARTEFATOS_AQUI`
Coloque qualquer arquivo `.pdf` ou `.txt` que deseje analisar dentro da pasta **`agente_arquiteto/ARTEFATOS_AQUI/`**. Os documentos de teste (`Artefato - Helpflow.pdf`, `Artefato - HealthSync.pdf`, `Artefato - Forgetwin.pdf` e `borda_vago.txt`) já estão prontos dentro dessa pasta.

### 6. Iniciar o Agente
Com o terminal (**CMD** ou **PowerShell**) aberto dentro da pasta `agente_arquiteto`, execute:

**No CMD (Prompt de Comando):**
```cmd
python main.py
```

**No PowerShell:**
```powershell
python main.py
```

---

## 🖥️ Como Funcionam os Comandos do Agente

Ao rodar `python main.py`, o agente lista na tela todos os arquivos encontrados em `ARTEFATOS_AQUI/` e faz **2 perguntas sequenciais**:

### 1º Comando: `1. Arquivo de requisitos (.pdf/.txt) em ARTEFATOS_AQUI`
Digite apenas o **nome do arquivo** (com a extensão `.pdf` ou `.txt`) que está dentro da pasta `ARTEFATOS_AQUI/` e pressione `Enter`:
* `Artefato - Helpflow.pdf`
* `Artefato - HealthSync.pdf`
* `Artefato - Forgetwin.pdf`
* `borda_vago.txt`

### 2º Comando: `2. Strategy de Arquitetura [completa/persistencia]`
Escolha qual estratégia comportamental (**GoF Strategy**) o agente aplicará sobre o documento e pressione `Enter`:
* **`completa`** (`ArquiteturaCompletaStrategy`): Analisa o sistema por inteiro e gera um ADR completo contendo:
  1. Recomendação e justificativa do **Estilo Arquitetural**;
  2. **Tabela de Padrões de Projeto GoF** (Criação, Estrutural, Comportamental) e **GRASP** (*Repository* e *Information Expert*);
  3. **Script SQL (DDL)** com `CREATE TABLE`, `PRIMARY KEY` e `FOREIGN KEY`;
  4. **Diagrama Entidade-Relacionamento (DER)** em sintaxe Mermaid (`erDiagram`);
  5. Análise de **Trade-offs** (vantagens, desvantagens e riscos).
* **`persistencia`** (`PersistenciaFocadaStrategy`): Foca exclusivamente na **Arquitetura de Persistência e Modelagem de Banco de Dados** (reduzindo quase pela metade o consumo de tokens de saída). O agente gera diretamente a estratégia de desacoplamento via *Repository* e *Information Expert*, o **Script SQL (DDL)** e o **Diagrama DER (`erDiagram`)**.

Assim que você responde ao 2º comando, o agente valida deterministicamente o SQL e o DER gerados, exibe a tabela de métricas no terminal e salva **automaticamente** todos os artefatos (`.md`, `.sql`, `.mmd`, `.csv` e `.html`) dentro de `agente_arquiteto/ARTEFATOS_AQUI/`.
