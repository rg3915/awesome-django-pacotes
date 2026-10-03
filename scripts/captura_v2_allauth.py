"""Tela de login do allauth (Google/GitHub) e a de 'verifique seu e-mail' após cadastro."""
import time

from captura_comum import BASE, abrir, foto, sync_playwright

with sync_playwright() as p:
    browser, ctx = abrir(p)
    page = ctx.new_page()
    page.goto(f"{BASE}/accounts/login/")
    page.wait_for_load_state("networkidle")
    foto(page, "v2_allauth_login.png")

    page.goto(f"{BASE}/accounts/signup/")
    email = f"leitora{int(time.time())}@exemplo.com"
    page.fill("input[name=email]", email)
    page.fill("input[name=password1]", "CapituOlhosDeRessaca#1899")
    page.fill("input[name=password2]", "CapituOlhosDeRessaca#1899")
    page.locator("form button[type=submit]").first.click()
    page.wait_for_load_state("networkidle")
    print("url após cadastro:", page.url)
    foto(page, "v2_allauth_confirmar.png")
    browser.close()
