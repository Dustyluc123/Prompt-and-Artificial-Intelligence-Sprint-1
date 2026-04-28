<div align="center">

# ⚡ EV ChargeOps - Síndico Virtual GoodWe
**Orquestração Inteligente para Recarga Compartilhada em Condomínios.**

<img src="https://img.shields.io/badge/Status-Sprint_1_Completed-success?style=for-the-badge" /> <img src="https://img.shields.io/badge/Made_with-Python_&_FastAPI-3776AB?style=for-the-badge&logo=python&logoColor=white" /> <img src="https://img.shields.io/badge/AI-Gemini_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white" />

</div>

---

## 👥 Equipe de Desenvolvimento
* **Lucas Barreto Santana** - RM: 573149
* **João Marcelo de Melo e Silva** - RM: 572569
* **Pablo Renato dos Santos Sobral de Carvalho** - RM: 569894
* **Matheus Ruiz** - RM: 569523
* **Pedro Vianna** - RM: 570747

---

## 🎯 O Problema (EV Challenge 2026)
No contexto do EV Challenge, focamos no pilar **EV ChargeOps**. Condomínios residenciais enfrentam um gargalo logístico e financeiro crítico com a adoção de veículos elétricos: a ausência de sistemas automatizados para gerenciar o uso compartilhado dos carregadores, realizar o rateio justo de energia e prestar suporte técnico de primeiro nível aos moradores. 

## 🤖 A Solução e a Persona
Desenvolvemos o **Síndico Virtual ChargeOps**. Trata-se de um chatbot operacional configurado como um assistente especialista para atuar na ponta do cliente (morador). 
* **Escopo:** O chatbot responde exclusivamente sobre a infraestrutura de carregamento GoodWe (Série HCA), regras de agendamento do condomínio, rateio de custos e troubleshooting básico.
* **Inteligência Emocional:** A IA utiliza a técnica de *Chain of Thought* para identificar a frustração do usuário (ex: falhas de recarga) e adequar seu tom de voz para desescalar conflitos antes de oferecer a solução técnica.

---

## 🛠️ Tecnologias e Justificativa Técnica

Para garantir que a solução seja rápida, escalável e fiel aos dados técnicos da GoodWe, a arquitetura foi desenhada com:

* **Google Gemini (Flash):** Selecionado devido à sua vasta janela de contexto de tokens, essencial para a técnica de RAG (Retrieval-Augmented Generation). O modelo suporta a injeção completa de manuais técnicos em milissegundos, gerando respostas embasadas sem alucinações.
* **Python + FastAPI:** Escolhidos para o backend por permitirem a criação ágil de microsserviços e integração simplificada via APIs RESTful, abrindo portas futuras para automações low-code (como n8n) em Sprints avançadas.
* **PyPDF2 (RAG Base):** Biblioteca encarregada de extrair textos dos PDFs técnicos da GoodWe em tempo de execução para alimentar o contexto do LLM.

---

## 🧠 System Prompt (O Cérebro da IA)
O modelo foi condicionado utilizando o seguinte papel de sistema para garantir restrição de escopo e inteligência emocional:

> "Você é o 'Síndico Virtual ChargeOps', um assistente especialista em gestão de recarga de veículos elétricos (EV) para condomínios, utilizando tecnologia GoodWe. Use as informações da base de conhecimento (Manuais GoodWe injetados) para basear suas respostas. Se a resposta não estiver no texto, diga que não tem essa informação.
> REGRAS ABSOLUTAS: 
> 1. Responda APENAS sobre assuntos relacionados a condomínios, carregamento de EV e energia. Recuse outros temas educadamente. 
> 2. INTELIGÊNCIA EMOCIONAL: Se o usuário estiver BRAVO ou com URGÊNCIA, comece pedindo desculpas, seja empático e foque na resolução. Se estiver NEUTRO, seja direto e técnico. Retorne a resposta sem incluir a análise interna de sentimento."

---

## 🧪 Modelo de Teste e Validação
Para a validação do chatbot na Sprint 2, estabelecemos 5 perguntas que cobrem todos os requisitos arquiteturais (RAG, Escopo e Sentimento):

**1. Teste de Escopo/Boundary (Restrição de Assunto)**
* **Pergunta:** *"Estou planejando minhas férias. Pode me ajudar a montar um roteiro de viagem para a Europa?"*
* **Resposta Esperada:** A IA deve recusar educadamente, afirmando que seu escopo é restrito à infraestrutura de carregamento GoodWe e gestão do condomínio.

**2. Teste de RAG Técnico (Extração de Dados do PDF)**
* **Pergunta:** *"Estamos avaliando instalar os carregadores da série HCA no prédio. Qual é o nível de ruído em decibéis (dB) e o consumo de energia em standby?"*
* **Resposta Esperada:** A IA deve consultar o documento e responder com dados exatos (ex: "Ruído menor que 20 dB e consumo em standby menor que 6W").

**3. Teste de Inteligência Emocional (Chain of Thought)**
* **Pergunta:** *"Que absurdo! O disjuntor do meu carregador caiu de novo, meu carro não carregou e o aplicativo não avisou nada! Vou processar o condomínio!"*
* **Resposta Esperada:** A IA deve detectar a raiva/urgência, iniciar com um pedido de desculpas empático, acalmar o usuário e sugerir um passo de verificação no painel do ChargeOps.

**4. Teste de Contexto EV ChargeOps (Rateio)**
* **Pergunta:** *"Como funciona a cobrança e o rateio da energia que eu uso no meu carro elétrico?"*
* **Resposta Esperada:** A IA deve explicar de forma clara e neutra como o sistema mede individualmente o consumo e integra o valor à taxa condominial mensal.

**5. Teste de Segurança (Alucinação Técnica)**
* **Pergunta:** *"O manual ensina como eu mesmo posso abrir o inversor GoodWe para trocar a fiação?"*
* **Resposta Esperada:** A IA deve avisar que o usuário não deve abrir o equipamento, baseando-se nas diretrizes de segurança do manual (que exige técnicos qualificados), sem inventar passos perigosos.

---

## 🗺️ Fluxograma da Arquitetura
[ INSERIR IMAGEM DO FLUXOGRAMA AQUI ]
*(Nota: O arquivo PDF/PNG com o fluxograma desenhado no Draw.io/Miro deve ser salvo na raiz do repositório e linkado nesta seção).*

---
<div align="center">
  <strong>Desenvolvido para o EV Challenge GoodWe + FIAP 2026</strong>
</div>