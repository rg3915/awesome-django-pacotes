"""Capturas do admin com unfold: lista, dashboard, histórico, revert, import e export."""
import sys
from pathlib import Path

from captura_comum import BASE, abrir, foto, login_admin, sync_playwright

ID_DOM = sys.argv[1]
CSV = Path(__file__).resolve().parents[1] / "dados" / "livros_importar.csv"

with sync_playwright() as p:
    browser, ctx = abrir(p)
    page = ctx.new_page()
    login_admin(page)

    page.goto(f"{BASE}/admin/")
    page.wait_for_load_state("networkidle")
    foto(page, "v2_unfold_dashboard.png")

    page.goto(f"{BASE}/admin/loja/livro/")
    page.wait_for_load_state("networkidle")
    foto(page, "v2_unfold_lista.png")

    page.goto(f"{BASE}/admin/loja/livro/{ID_DOM}/history/")
    page.wait_for_load_state("networkidle")
    foto(page, "v2_history_lista.png")

    # abre a 2ª versão mais antiga (o preço original) para reverter
    links = page.locator("a[href*='/history/']").evaluate_all("els => els.map(e => e.getAttribute('href'))")
    versoes = [h for h in links if h.rstrip('/').split('/')[-1].isdigit()]
    page.goto(BASE + versoes[-1])
    page.wait_for_load_state("networkidle")
    foto(page, "v2_history_revert.png")

    page.goto(f"{BASE}/admin/loja/livro/export/")
    page.wait_for_load_state("networkidle")
    foto(page, "v2_export.png")

    page.goto(f"{BASE}/admin/loja/livro/import/")
    page.wait_for_load_state("networkidle")
    page.set_input_files("input[type=file]", str(CSV))
    fmt = page.locator("select[name=format]")
    if fmt.count():
        fmt.select_option(label="csv")
    page.locator("form [type=submit]").last.click()
    page.wait_for_load_state("networkidle")
    foto(page, "v2_import_preview.png")
    browser.close()
