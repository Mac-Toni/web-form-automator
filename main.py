import json
import pandas as pd
from playwright.sync_api import sync_playwright

def clicar_no_botao_enviar(page):
    try:
        # Lista de textos comuns em botões de envio
        termos = ["Enviar", "Submit", "Send", "Contact", "Submit Message", "Confirmar"]
        
        for termo in termos:
            # exact=False ajuda a encontrar "Enviar Mensagem" apenas com "Enviar"
            botao = page.get_by_role("button", name=termo, exact=False)
            if botao.is_visible():
                # print(f"Botão '{termo}' encontrado!") # Removido o click real para segurança
                return True
        
        # Tenta pelo tipo do input caso não seja um <button>
        botao_input = page.locator("input[type='submit']")
        if botao_input.is_visible():
            return True

        return False
    except:
        return False

def preencher_formulario(page, config):
    try:
        # Preenchendo o Nome
        if page.locator("input[name*='name']").is_visible():
            page.locator("input[name*='name']").fill(config['nome'])
        elif page.get_by_placeholder("Nome").is_visible():
            page.get_by_placeholder("Nome").fill(config['nome'])
        
        # Preenchendo o E-mail
        if page.locator("input[name*='email']").is_visible():
            page.locator("input[name*='email']").fill(config['email'])
        
        # Preenchendo a Mensagem
        if page.locator("textarea").is_visible():
            page.locator("textarea").fill(config['mensagem'])

        # Tenta identificar o botão de envio
        botao_existe = clicar_no_botao_enviar(page)
        if botao_existe:
            print("Campos preenchidos e botão de envio detectado!")
        else:
            print("Campos preenchidos, mas botão de envio não detectado.")
            
    except Exception as e:
        print(f"Erro ao preencher: {e}")

def rodar_automacao():
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            df = pd.read_csv('sites.csv')
        except Exception as e:
            print(f"Erro ao ler sites.csv: {e}")
            return

        resultados = []

        for index, row in df.iterrows():
            url = row['url']
            try:
                page.goto(url, timeout=60000)
                page.wait_for_timeout(2000)

                if page.locator("iframe[src*='recaptcha']").is_visible() or \
                   page.locator("iframe[src*='hcaptcha']").is_visible():
                    status = "Bloqueado por CAPTCHA"
                else:
                    preencher_formulario(page, config)
                    status = "Sucesso (Simulado)"
                
            except Exception as e:
                status = f"Erro: {str(e)}"
            
            resultados.append({"URL": url, "Status": status})
            print(f"{url} -> {status}")

        df_report = pd.DataFrame(resultados)
        df_report.to_csv('relatorio_envios.csv', index=False)
        print("\n--- Processo finalizado! ---")
        browser.close()

if __name__ == "__main__":
    rodar_automacao()