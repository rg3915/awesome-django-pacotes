"""Tela de export com a lista de formatos visível (select expandido com size=N)."""
from captura_comum import BASE, abrir, foto, login_admin, sync_playwright

with sync_playwright() as p:
    browser, ctx = abrir(p)
    page = ctx.new_page()
    login_admin(page)
    page.goto(f"{BASE}/admin/loja/livro/export/")
    page.wait_for_load_state("networkidle")
    print(page.locator("select[name=format] option").all_inner_texts())
    page.eval_on_selector("select[name=format]", "s => { s.size = s.options.length; s.style.height = 'auto'; s.style.backgroundImage = 'none'; }")
    page.select_option("select[name=format]", label="csv")
    page.wait_for_timeout(300)
    foto(page, "v2_export.png")
    browser.close()
