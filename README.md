# 🤖 Web Form Automator

Uma automação poderosa desenvolvida com **Python**, **Playwright** e **Pandas** para preenchimento automático de formulários de contato em massa, com suporte a resolução de **reCAPTCHA v2** via API do **2Captcha**.

## 🚀 Funcionalidades

- 📂 **Processamento em Massa**: Lê uma lista de URLs a partir de um arquivo CSV.
- 🧩 **Inteligência de Campos**: Detecta automaticamente campos de Nome, E-mail, Assunto e Mensagem.
- 🛡️ **Suporte a Captcha**: Integração real com o serviço 2Captcha para superar barreiras de bots.
- 📸 **Debug Visual**: Tira screenshots automáticas em caso de erro para fácil diagnóstico.
- ⚙️ **Modo de Segurança**: Campo `modo_real` que permite testar o preenchimento sem realizar o envio final.

## 🛠️ Tecnologias Utilizadas

* [Python 3.10+](https://www.python.org/)
* [Playwright](https://playwright.dev/python/) (Navegação Web)
* [Pandas](https://pandas.pydata.org/) (Manipulação de Dados)
* [2Captcha API](https://2captcha.com/) (Resolução de Desafios)

## 📦 Instalação

1. Clone o repositório:
   ```bash
   git clone [https://github.com/Mac-Toni/web-form-automator.git](https://github.com/Mac-Toni/web-form-automator.git)
   cd web-form-automator