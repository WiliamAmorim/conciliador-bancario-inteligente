# 💼 Conciliador Bancário Inteligente

Sistema backend para conciliação automática de transações bancárias utilizando tolerância de valor, tolerância de data e análise de similaridade textual.

Projeto desenvolvido com foco em arquitetura em camadas, isolamento por execução e geração automatizada de relatórios em PDF.

---

## 🚀 Visão Geral

O sistema realiza a conciliação entre:

- 📄 Extrato bancário (CSV)
- 📊 Controle interno (XLSX)

Aplicando regras inteligentes para identificar correspondências entre lançamentos.

Cada execução é isolada por contexto, garantindo integridade histórica e rastreabilidade.

---

## 🧠 Estratégia de Conciliação

A conciliação ocorre em 4 etapas:

1. 🔎 Filtro por tipo (crédito/débito)
2. 💰 Tolerância de valor configurável
3. 📅 Tolerância de diferença de dias
4. ✍️ Similaridade textual entre descrições

Classificação final:

- ✅ **AUTO** → alta similaridade
- ⚠️ **SUGESTAO** → similaridade aceitável
- ❌ Não conciliado

---

## 🏗 Arquitetura do Projeto

```
consultafiistelegram/
│
├── main.py
├── config.py
├── importador.py
├── leitor.py
│
├── dados/
│   ├── entrada/
│   ├── erro/
│   ├── processados/
│   └── relatorios/
│
├── database/
│   ├── conciliacoes.py
│   ├── conexao.py
│   ├── execucoes.py
│   └── transacoes.py
│
├── logs/
│
├── services/
│   ├── motor_conciliacao.py
│   └── relatorio.py
│
├── sql/
│   └── schema.sql
│
├── utils/
│   ├── logger.py
│   └── similaridade.py
│
├── .env
├── requirements.txt
└── README.md
```

### 📂 Estrutura


services/ → regras de negócio
database/ → acesso ao banco
utils/ → utilidades
dados/ → arquivos de entrada e saída
logs/ → logs por execução
sql/ → estrutura do banco


Separação clara de responsabilidades e baixo acoplamento.

---

## 🔄 Fluxo de Execução

1. Criar nova execução
2. Importar extrato e controle vinculados ao `execucao_id`
3. Buscar candidatos à conciliação
4. Calcular similaridade textual
5. Classificar resultado
6. Registrar conciliações
7. Gerar resumo
8. Gerar relatório PDF

---

## 📊 Banco de Dados

### Tabelas principais:

- `execucoes`
- `transacoes`
- `conciliacoes`

Cada execução possui seu próprio conjunto de dados, garantindo isolamento e consistência histórica.

---

## 📄 Relatório PDF

Ao final de cada execução, o sistema gera automaticamente:

- ID da execução
- Totais de AUTO e SUGESTAO
- Lista detalhada das conciliações
- Percentual de similaridade

---

## 🛠 Tecnologias Utilizadas

- Python 3.10+
- Pandas
- MySQL
- ReportLab (PDF)
- python-dotenv
- Logging estruturado

---

## ⚙️ Configuração

### 1️⃣ Criar banco MySQL

Execute o script:


sql/schema.sql


### 2️⃣ Criar arquivo `.env`

Baseado em:


.env.example


### 3️⃣ Instalar dependências


pip install -r requirements.txt


### 4️⃣ Executar


python main.py


---

## 🔒 Boas Práticas Aplicadas

✔ Arquitetura em camadas  
✔ Isolamento por execução  
✔ Uso de variáveis de ambiente  
✔ Logging estruturado  
✔ Separação de responsabilidades  
✔ Índices no banco para performance  
✔ Relatório automatizado  

---

## 🎯 Objetivo do Projeto

Demonstrar:

- Modelagem de dados relacional
- Desenvolvimento backend estruturado
- Organização de código escalável
- Processamento de dados com Pandas
- Geração de relatórios automatizados
- Boas práticas de engenharia de software

---

## 👨‍💻 Autor

Desenvolvido por **Wiliam Amorim**

Projeto para portfólio backend Python.