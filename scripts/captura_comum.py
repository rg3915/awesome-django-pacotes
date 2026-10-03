"""Funções comuns para as capturas com Playwright (Chromium, 1600x1000, DPR 2)."""
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8010"
SAIDA = Path(__file__).resolve().parents[2] / "captura"


def abrir(p, escuro=True):
    browser = p.chromium.launch()
    ctx = browser.new_context(
        viewport={"width": 1600, "height": 1000},
        device_scale_factor=2,
        color_scheme="dark" if escuro else "light",
        locale="pt-BR",
    )
    return browser, ctx


def login_admin(page, usuario="regis", senha="regis123"):
    page.goto(f"{BASE}/admin/login/")
    page.fill("input[name=username]", usuario)
    page.fill("input[name=password]", senha)
    page.click("[type=submit]")
    page.wait_for_load_state("networkidle")


def foto(page, nome, **kw):
    destino = SAIDA / nome
    page.screenshot(path=str(destino), **kw)
    print("salvo", destino)
