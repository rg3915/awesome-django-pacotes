from captura_comum import BASE, abrir, foto, sync_playwright

with sync_playwright() as p:
    browser, ctx = abrir(p, escuro=False)
    page = ctx.new_page()
    page.goto(f"{BASE}/api/livros/?preco__gt=50")
    page.wait_for_load_state("networkidle")
    foto(page, "v1_api_filtro.png")
    page.click("button:has-text('Filtros'), button:has-text('Filters')")
    page.wait_for_timeout(800)
    foto(page, "v1_api_filtro_form.png")
    browser.close()
