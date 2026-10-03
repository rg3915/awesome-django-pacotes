"""Admin padrão do Django (rodar o servidor com USE_UNFOLD=False) para o antes/depois."""
from captura_comum import BASE, abrir, foto, login_admin, sync_playwright

with sync_playwright() as p:
    for escuro, sufixo in [(True, ""), (False, "_claro")]:
        browser, ctx = abrir(p, escuro=escuro)
        page = ctx.new_page()
        login_admin(page)
        page.goto(f"{BASE}/admin/loja/livro/")
        page.wait_for_load_state("networkidle")
        foto(page, f"v2_admin_padrao{sufixo}.png")
        page.goto(f"{BASE}/admin/")
        page.wait_for_load_state("networkidle")
        foto(page, f"v2_admin_padrao_dashboard{sufixo}.png")
        browser.close()
