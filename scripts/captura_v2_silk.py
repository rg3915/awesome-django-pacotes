"""Gera tráfego (inclui a view com N+1) e captura o silk: lista, SQL da request e uma query."""

from captura_comum import BASE, abrir, foto, login_admin, sync_playwright

with sync_playwright() as p:
    browser, ctx = abrir(p)
    page = ctx.new_page()
    login_admin(page)
    for url in [
        "/admin/", "/admin/loja/livro/", "/admin/loja/livro/?categoria__id__exact=1",
        "/admin/loja/livro/1/change/", "/api/livros/?preco__gt=50", "/api/livros/?categoria=poesia",
        "/api/livros/?publicado_em__year=1930", "/api/livros/?page=2", "/relatorio-otimizado/", "/relatorio/",
    ]:
        page.goto(BASE + url)
        page.wait_for_load_state("networkidle")

    page.goto(f"{BASE}/silk/requests/")
    page.wait_for_load_state("networkidle")
    foto(page, "v2_silk_requests.png")

    # request mais recente para /relatorio/ (a do N+1)
    page.goto(f"{BASE}/silk/requests/?view_style=row")
    href = page.locator("a[href*='/silk/request/']", has_text="/relatorio/").first
    if not href.count():
        href = page.locator("tr:has-text('/relatorio/') a[href*='/silk/request/']").first
    req_url = href.get_attribute("href")
    req_id = req_url.strip("/").split("/")[2]
    print("request N+1:", req_id)
    page.goto(f"{BASE}/silk/request/{req_id}/sql/")
    page.wait_for_load_state("networkidle")
    foto(page, "v2_silk_sql.png")

    # detalhe de uma das queries repetidas (mostra o SQL de verdade)
    detalhe = page.locator("tr.data-row").nth(1).get_attribute("data-sql-detail-url")
    page.goto(BASE + detalhe)
    page.wait_for_load_state("networkidle")
    print("detalhe:", page.url)
    foto(page, "v2_silk_sql_detalhe.png")
    browser.close()
