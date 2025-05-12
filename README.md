# Extrator de Texto de PDFs e HTMLs

Projeto em Python para extrair texto de arquivos PDF e HTML, com geração de relatório de desempenho e salvamento em disco.

## 📂 Estrutura

```
/documentos/
├── documentos/    → coloque os arquivos PDF e HTML aqui
├── script.py → script principal
├── texts/         → textos extraídos
├── relatorio/     → relatório final
```

## ⚙️ Funcionalidades

- Extração de texto de arquivos PDF e HTML
- Processamento multithread
- Relatório com:
  - Tempo total
  - Sucesso e falhas
  - Tempo médio por tipo de arquivo
- Salvamento automático dos textos e relatório

## 📦 Requisitos

- Python 3.13+
- pdfminer.six
- beautifulsoup4
