import os
import PyPDF2
from google import genai
from google.genai import types
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

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

# Funcao para ler o PDF
def extrair_texto_pdf(caminho_arquivo: str) -> str:
    texto = ""
    try:
        if os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, 'rb') as arquivo:
                leitor = PyPDF2.PdfReader(arquivo)
                for pagina in leitor.pages:
                    texto += pagina.extract_text() + "\n"
            print(f"Base de conhecimento carregada: {caminho_arquivo}")
        else:
            print(f"AVISO: Arquivo {caminho_arquivo} nao encontrado. Rodando sem base de dados.")
    except Exception as e:
        print(f"Erro ao ler PDF: {e}")
    return texto

# Carrega o PDF na memoria quando o servidor liga
BASE_DE_CONHECIMENTO = extrair_texto_pdf("manual_goodwe.pdf")

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