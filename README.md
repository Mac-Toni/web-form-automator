# Web Form Automator 🤖

Este projeto é uma ferramenta de automação robusta desenvolvida para otimizar o processo de envio de mensagens através de formulários de contato em sites diversos. Ideal para prospecção e marketing direto em larga escala.

## ✨ Funcionalidades

- **Navegação Inteligente:** Utiliza Playwright para lidar com sites modernos (Single Page Applications).
- **Seletores Flexíveis:** Algoritmo que identifica campos de Nome, E-mail e Mensagem mesmo com IDs diferentes.
- **Detecção de Bloqueios:** Identifica automaticamente a presença de CAPTCHAs (reCAPTCHA/hCaptcha).
- **Relatório de Performance:** Gera um arquivo `.csv` detalhando o sucesso ou erro de cada envio.
- **Configuração Isolada:** Gerenciamento de mensagens e credenciais via arquivo JSON para maior segurança.

## 🚀 Tecnologias Utilizadas

- **Python 3.10+**
- **Playwright** (Automação de navegador)
- **Pandas** (Manipulação de dados e relatórios)

## 📋 Como Instalar

1. Clone o repositório:
   ```bash
   (https://github.com/Mac-Toni/web-form-automator.git)
   cd web-form-automator