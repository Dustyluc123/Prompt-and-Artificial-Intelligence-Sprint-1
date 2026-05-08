import os
import PyPDF2
from google import genai
from google.genai import types
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import glob


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("ERRO: Chave GEMINI_API_KEY nao encontrada no arquivo .env")

client = genai.Client(api_key=api_key)

app = FastAPI(title="API Sindico Virtual - EV ChargeOps")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MensagemUsuario(BaseModel):
    texto: str

def extrair_texto_pasta_pdfs(caminho_pasta: str) -> str:
    texto_total = ""
    # Busca todos os arquivos com extensao .pdf dentro da pasta informada
    arquivos_pdf = glob.glob(os.path.join(caminho_pasta, "*.pdf"))
    
    if not arquivos_pdf:
        print(f"AVISO CRITICO: Nenhum PDF encontrado na pasta '{caminho_pasta}'. A IA estara sem memoria tecnica.")
        return texto_total

    print(f"Iniciando leitura de {len(arquivos_pdf)} arquivo(s) PDF...")
    
    for caminho_arquivo in arquivos_pdf:
        try:
            with open(caminho_arquivo, 'rb') as arquivo:
                leitor = PyPDF2.PdfReader(arquivo)
                texto_arquivo = ""
                for pagina in leitor.pages:
                    texto_extraido = pagina.extract_text()
                    if texto_extraido:
                        texto_arquivo += texto_extraido + "\n"
                texto_total += f"\n--- DOCUMENTO: {os.path.basename(caminho_arquivo)} ---\n" + texto_arquivo
                print(f"[OK] Documento injetado: {os.path.basename(caminho_arquivo)}")
        except Exception as e:
            print(f"[ERRO] Falha ao ler o arquivo {caminho_arquivo}: {e}")
            
    return texto_total

# Descobre onde o arquivo main.py esta salvo fisicamente
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))

# Constroi o caminho exato para a pasta PDFs voltando uma pasta de forma segura
CAMINHO_PDFS = os.path.join(DIRETORIO_ATUAL, "..", "PDFs")

# Carrega o PDF na memoria quando o servidor liga
BASE_DE_CONHECIMENTO = extrair_texto_pasta_pdfs(CAMINHO_PDFS)

def obter_resposta_sindico(mensagem: str) -> str:
    system_instruction = f"""
    Você é o 'Síndico Virtual ChargeOps', um assistente especialista em gestão de recarga de veículos elétricos (EV) para condomínios, utilizando tecnologia GoodWe.
    
    BASE DE CONHECIMENTO TÉCNICO E REGRAS DO CONDOMÍNIO:
    Use as informações abaixo para basear suas respostas técnicas. Se a resposta não estiver neste texto, diga que não tem essa informação no momento.
    --- INÍCIO DA BASE DE CONHECIMENTO ---
    {BASE_DE_CONHECIMENTO}
    --- FIM DA BASE DE CONHECIMENTO ---
    
    REGRAS ABSOLUTAS:
    1. Responda APENAS sobre assuntos relacionados a condomínios, carregamento de veículos elétricos e energia.
    2. INTELIGÊNCIA EMOCIONAL (Chain of Thought): Antes de gerar a resposta final, analise o tom da mensagem do usuário.
        - Se o usuário estiver BRAVO, FRUSTRADO ou com URGÊNCIA: Sua resposta deve começar pedindo desculpas, sendo extremamente empática, calma e focada em resolver o problema imediatamente.
        - Se o usuário estiver NEUTRO ou buscando DADOS: Seja direto, técnico, educado e eficiente.
        - Se o usuário estiver FELIZ ou SATISFEITO: Seja amigável e encorajador.
    
    Retorne a sua resposta diretamente, sem incluir a sua análise interna de sentimento.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=mensagem,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2, 
            )
        )
        return response.text
    except Exception as e:
        print(f"Erro ao chamar Gemini: {e}")
        return "Desculpe, estou enfrentando instabilidades no painel central. Tente novamente em instantes."

@app.post("/chat")
async def chat_com_sindico(mensagem: MensagemUsuario):
    if not mensagem.texto.strip():
        raise HTTPException(status_code=400, detail="A mensagem nao pode estar vazia.")
    
    resposta = obter_resposta_sindico(mensagem.texto)
    return {
        "status": "sucesso",
        "resposta_ia": resposta
    }

@app.get("/")
async def root():
    return {"mensagem": "API do Sindico Virtual esta online e atualizada!"}