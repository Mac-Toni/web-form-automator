import json
import os
import time
import requests
import pandas as pd
from playwright.sync_api import sync_playwright

# 1. FUNÇÃO PARA RESOLVER CAPTCHA (REAL)
def resolver_captcha(url, site_key, api_key):
    if not api_key or api_key == "SUA_CHAVE_AQUI" or api_key == "":
        print("Erro: API Key do 2Captcha não configurada no config.json.")
        return None
    
    try:
        print(f"Enviando desafio para 2Captcha (Site Key: {site_key})...")
        post_url = "http://2captcha.com/in.php"
        payload = {
            'key': api_key,
            'method': 'userrecaptcha',
            'googlekey': site_key,
            'pageurl': url,
            'json': 1
        }
        
        response = requests.post(post_url, data=payload).json()
        if response.get("status") != 1:
            print(f"Erro no envio: {response.get('request')}")
            return None

        request_id = response.get("request")
        fetch_url = f"http://2captcha.com/res.php?key={api_key}&action=get&id={request_id}&json=1"
        
        print("Aguardando resolução (30-90s)...")
        for _ in range(40): 
            time.sleep(5)
            res = requests.get(fetch_url).json()
            if res.get("status") == 1:
                print("CAPTCHA resolvido pelo 2Captcha!")
                return res.get("request")
            if res.get("request") == "CAPCHA_NOT_READY":
                continue
            break
        return None
    except Exception as e:
        print(f"Erro na comunicação com API: {e}")
        return None

# 2. FUNÇÃO PARA DETECTAR E CLICAR NO BOTÃO DE ENVIO
def clicar_no_botao_enviar(page, modo_real):
    if not modo_real:
        print("--- MODO TESTE: O botão de envio NÃO foi clicado ---")
        return True

    try:
        termos = ["Enviar", "Submit", "Send", "Contact", "Confirmar", "Mensagem"]
        for termo in termos:
            botao = page.get_by_role("button", name=termo, exact=False)
            if botao.is_visible():
                botao.click()
                return True
        
        botao_input = page.locator("input[type='submit']")
        if botao_input.is_visible():
            botao_input.click()
            return True
        return False
    except:
        return False

# 3. FUNÇÃO PARA PREENCHER OS CAMPOS (AGORA SINCRONIZADA COM SEU JSON)
def preencher_formulario(page, config):
    try:
        # Preenche o Nome
        if page.locator("input[name*='name']").is_visible():
            page.locator("input[name*='name']").fill(config['nome'])
        
        # Preenche o Email
        if page.locator("input[name*='email']").is_visible():
            page.locator("input[name*='email']").fill(config['email'])

        # Sincronizando o campo ASSUNTO
        # Tenta localizar por 'subject' (inglês) ou 'assunto' (português)
        selector_assunto = page.locator("input[name*='subject'], input[name*='assunto']")
        if selector_assunto.first.is_visible():
            selector_assunto.first.fill(config['assunto'])
        
        # Preenche a Mensagem
        if page.locator("textarea").is_visible():
            page.locator("textarea").fill(config['mensagem'])

        return True
    except Exception as e:
        print(f"Erro ao preencher: {e}")
        return False

# 4. MOTOR PRINCIPAL
def rodar_automacao():
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')

    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"Erro ao ler config.json: {e}")
        return

    with sync_playwright() as p:
        # headless=False permite que você veja o que está acontecendo
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
            nome_arquivo = url.replace("https://", "").replace("http://", "").replace("/", "_")[:20]
            status = ""
            
            try:
                print(f"\n--- Visitando: {url} ---")
                page.goto(url, timeout=60000, wait_until="networkidle")

                # 1. Preenche os campos (Nome, Email, Assunto, Mensagem)
                preencher_formulario(page, config)

                # 2. Lógica de CAPTCHA
                captcha_frame = page.locator("iframe[src*='recaptcha/api2/anchor']").first
                
                if captcha_frame.is_visible():
                    print("CAPTCHA detectado. Tentando resolver...")
                    site_key = page.locator(".g-recaptcha, [data-sitekey]").get_attribute("data-sitekey")
                    
                    token = resolver_captcha(url, site_key, config.get('api_2captcha'))
                    
                    if token:
                        page.evaluate(f'document.getElementById("g-recaptcha-response").innerHTML="{token}";')
                        status = "Sucesso (Captcha Resolvido)"
                    else:
                        status = "Falha (Captcha não resolvido)"
                else:
                    status = "Sucesso (Sem Captcha)"

                # 3. Clique final (Respeitando o 'modo_real' do seu JSON)
                sucesso_envio = clicar_no_botao_enviar(page, config.get('modo_real', False))
                if not sucesso_envio:
                    status += " - Botão de envio não detectado"
                
                page.wait_for_timeout(2000)

            except Exception as e:
                status = f"Erro: {str(e)[:50]}"
                page.screenshot(path=f"screenshots/erro_{nome_arquivo}.png")
            
            resultados.append({"URL": url, "Status": status})
            print(f"Resultado: {status}")

        df_report = pd.DataFrame(resultados)
        df_report.to_csv('relatorio_envios.csv', index=False)
        print("\n--- Processo concluído! Relatório salvo em relatorio_envios.csv ---")
        browser.close()
