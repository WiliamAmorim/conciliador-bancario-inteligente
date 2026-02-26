# 💼 Conciliador Bancário Inteligente

Sistema backend para conciliação automática de transações bancárias utilizando tolerância de valor, tolerância de data e análise de similaridade textual.

---

## 🚀 Funcionalidades

- 📥 Importação de arquivos CSV (extrato)
- 📥 Importação de arquivos XLSX (controle interno)
- 🧠 Motor de conciliação com:
  - Tolerância de valor
  - Tolerância de dias
  - Similaridade textual
- 🔄 Classificação automática:
  - AUTO
  - SUGESTAO
- 📝 Registro de execuções
- 📊 Log estruturado por execução

---

## 🏗 Arquitetura

Projeto organizado em camadas:

- `services/` → regras de negócio
- `database/` → acesso ao banco
- `utils/` → utilidades
- `dados/` → arquivos de entrada
- `logs/` → logs por execução

---

## 🛠 Tecnologias

- Python 3.10+
- Pandas
- MySQL
- python-dotenv
- Logging estruturado

---

## ⚙️ Configuração

1. Criar banco MySQL
2. Executar `sql/schema.sql`
3. Criar arquivo `.env`:
