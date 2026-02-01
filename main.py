import json
import pandas as pd
from playwright.sync_api import sync_playwright

# 1. FUNÇÃO PARA SIMULAR O SOLVER DE CAPTCHA
def resolver_captcha(url, site_key, api_key):
    if api_key == "SUA_CHAVE_AQUI" or api_key == "":
        return None
    
    print(f"Enviando CAPTCHA de {url} para o 2Captcha...")
    # Aqui retornamos um token simulado
    return "TOKEN_SOLVED_BY_2CAPTCHA"

# 2. FUNÇÃO PARA DETECTAR O BOTÃO DE ENVIO
def clicar_no_botao_enviar(page):
    try:
        termos = ["Enviar", "Submit", "Send", "Contact", "Submit Message", "Confirmar"]
        for termo in termos:
            botao = page.get_by_role("button", name=termo, exact=False)
            if botao.is_visible():
                return True
        
        botao_input = page.locator("input[type='submit']")
        if botao_input.is_visible():
            return True
        return False
    except:
        return False

# 3. FUNÇÃO PARA PREENCHER OS CAMPOS
def preencher_formulario(page, config):
    try:
        if page.locator("input[name*='name']").is_visible():
            page.locator("input[name*='name']").fill(config['nome'])
        elif page.get_by_placeholder("Nome").is_visible():
            page.get_by_placeholder("Nome").fill(config['nome'])
        
        if page.locator("input[name*='email']").is_visible():
            page.locator("input[name*='email']").fill(config['email'])
        
        if page.locator("textarea").is_visible():
            page.locator("textarea").fill(config['mensagem'])

        botao_existe = clicar_no_botao_enviar(page)
        if botao_existe:
            print("Campos preenchidos e botão detectado!")
        else:
            print("Campos preenchidos, mas botão não encontrado.")
    except Exception as e:
        print(f"Erro ao preencher: {e}")

# 4. FUNÇÃO PRINCIPAL (O MOTOR DO ROBÔ)
def rodar_automacao():
    # Carrega Configurações
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"Erro ao ler config.json: {e}")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Lê os sites
        try:
            df = pd.read_csv('sites.csv')
        except Exception as e:
            print(f"Erro ao ler sites.csv: {e}")
            return

        resultados = []

        for index, row in df.iterrows():
            url = row['url']
            nome_arquivo = url.replace("https://", "").replace("http://", "").replace("/", "_").replace(".", "_")[:30]
            
            try:
                print(f"\nVisitando: {url}")
                page.goto(url, timeout=60000)
                page.wait_for_timeout(2000)

                # LÓGICA DE VERIFICAÇÃO DE CAPTCHA
                if page.locator("iframe[src*='recaptcha']").is_visible() or \
                   page.locator("iframe[src*='hcaptcha']").is_visible():
                    
                    status = "Tentando resolver CAPTCHA..."
                    token = resolver_captcha(url, "SITE_KEY_EXEMPLO", config.get('api_2captcha', ''))
                    
                    if token:
                        status = "Sucesso (Captcha Simulado)"
                    else:
                        status = "Bloqueado por CAPTCHA"
                        page.screenshot(path=f"screenshots/captcha_{nome_arquivo}.png")
                else:
                    preencher_formulario(page, config)
                    status = "Sucesso (Preenchido)"
                
            except Exception as e:
                status = f"Erro: {str(e)}"
                try:
                    page.screenshot(path=f"screenshots/erro_{nome_arquivo}.png")
                except: pass
            
            resultados.append({"URL": url, "Status": status})
            print(f"Resultado: {status}")

        # SALVAMENTO DO RELATÓRIO (FORA DO LOOP)
        df_report = pd.DataFrame(resultados)
        df_report.to_csv('relatorio_envios.csv', index=False)
        print("\n--- Automação Finalizada com Sucesso! ---")
        browser.close()

# INICIALIZAÇÃO
if __name__ == "__main__":
    rodar_automacao()