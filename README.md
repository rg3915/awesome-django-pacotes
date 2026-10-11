# Livraria Awesome — 10 pacotes do awesomedjango.org num projeto real

Loja de livros simples (app `loja`: `Categoria` e `Livro`) com 30 livros brasileiros,
usada para gravar dois vídeos sobre pacotes do [awesomedjango.org](https://awesomedjango.org).

## Vídeos

| Parte | Vídeo completo | Short | Estreia |
|---|---|---|---|
| 1. Os 5 que estão em quase todo projeto | [youtu.be/DgAovvO3BkA](https://youtu.be/DgAovvO3BkA) | [shorts/ZV-wHV1W9E8](https://youtube.com/shorts/ZV-wHV1W9E8) | 17/10/2026, 09:00 |
| 2. 5 pacotes que parecem mágica | [youtu.be/Qw3HjPzrcm8](https://youtu.be/Qw3HjPzrcm8) | [shorts/PJY4A8yyA7c](https://youtube.com/shorts/PJY4A8yyA7c) | 24/10/2026, 10:00 |

Tutorial com o passo a passo: [Dicas de Django — 10 pacotes do Awesome Django num projeto real](https://www.dicas-de-django.com.br/126-awesome-django-pacotes)
· Canal: [@RegisdoPython](https://www.youtube.com/@RegisdoPython)

- **Django 6.1.1** + Python 3.12 — todos os pacotes funcionaram no Django 6.1, não foi preciso cair para o 5.2 LTS.
- Banco: SQLite. Versões exatas no `uv.lock`.

| Vídeo | Pacote | Onde está |
|---|---|---|
| 1 | django-cors-headers | `config/settings.py` (`CORS_ALLOWED_ORIGINS` vem do `.env`) |
| 1 | whitenoise | middleware + `CompressedManifestStaticFilesStorage` (gzip e Brotli) |
| 1 | django-filter + DRF | `loja/filters.py`, `loja/api.py` → `/api/livros/` |
| 1 | django-storages | `STORAGES["default"]` = S3 (MinIO) quando `AWS_S3_ENDPOINT_URL` está no `.env` |
| 1 | django-environ | topo do `config/settings.py` |
| 2 | django-simple-history | `history = HistoricalRecords()` no `Livro` + `SimpleHistoryAdmin` |
| 2 | django-import-export | `loja/resources.py` + `ImportExportModelAdmin` |
| 2 | django-unfold | tema do admin (escuro), com `unfold.contrib.import_export` e `unfold.contrib.simple_history` |
| 2 | django-allauth | `/accounts/login/` — login por e-mail, Google e GitHub (apps fictícios), confirmação obrigatória |
| 2 | django-silk | middleware + `/silk/`; `/relatorio/` tem um N+1 de propósito |

## Como rodar

```bash
uv sync
cp .env.example .env            # e troque a SECRET_KEY
uv run python manage.py migrate
uv run python manage.py popular_loja   # categorias, 30 livros, usuários, histórico, SocialApps
uv run python manage.py runserver 8010
```

Usuários criados pelo `popular_loja`: `regis` / `regis123`, `ana` / `senha123`, `bruno` / `senha123`
(os três são superusuários; o histórico do *Dom Casmurro* tem alterações de cada um).

URLs: `/api/livros/?preco__gt=50`, `?categoria=poesia`, `?publicado_em__year=1930` · `/admin/` ·
`/accounts/login/` · `/silk/` · `/relatorio/` (N+1) · `/relatorio-otimizado/` (`select_related`).

O e-mail de confirmação do allauth sai no console do `runserver` (`EMAIL_BACKEND` de console).

### django-storages com MinIO

A imagem `minio/minio` do Docker Hub não está mais disponível para pull (acesso negado, e o
quay.io pediu login), então foi usada a imagem `cgr.dev/chainguard/minio`:

```bash
docker run -d --name awesome-minio -p 9010:9000 -p 9011:9001 \
  -e MINIO_ROOT_USER=minioadmin -e MINIO_ROOT_PASSWORD=minioadmin \
  cgr.dev/chainguard/minio:latest server /tmp/data --console-address :9001
uv run python -c "import boto3; boto3.client('s3', endpoint_url='http://127.0.0.1:9010', \
  aws_access_key_id='minioadmin', aws_secret_access_key='minioadmin').create_bucket(Bucket='livraria')"
```

Sem `AWS_S3_ENDPOINT_URL` no `.env`, o projeto usa o `FileSystemStorage` (pasta `media/`).
Os dados do MinIO ficam dentro do container (em `/tmp/data`), então somem se ele for removido.

### Admin padrão × unfold (antes/depois)

```bash
USE_UNFOLD=False uv run python manage.py runserver 8010   # admin padrão do Django
```

### whitenoise em "produção"

```bash
DEBUG=False uv run python manage.py collectstatic --noinput
DEBUG=False uv run python manage.py runserver 8010
curl -I -H "Accept-Encoding: br" http://127.0.0.1:8010/static/admin/css/base.<hash>.css
```

## Capturas

Os scripts em `scripts/` (Playwright + Chromium, 1600×1000, deviceScaleFactor 2) geram os PNGs na pasta
`captura/` ao lado do projeto, com o servidor já rodando na porta 8010:

```bash
uv run python scripts/captura_v1.py                  # API filtrada (DRF)
uv run python scripts/captura_v2_admin.py 1          # unfold, histórico, import/export (id do Dom Casmurro)
uv run python scripts/captura_v2_export.py
uv run python scripts/captura_v2_allauth.py
uv run python scripts/captura_v2_silk.py             # gera tráfego e captura o silk
uv run python scripts/captura_v2_padrao.py           # servidor com USE_UNFOLD=False
```

`dados/livros_importar.csv` é o CSV usado na pré-visualização do import (3 atualizações + 4 livros novos).
A pré-visualização **não** foi confirmada, então o banco continua com 30 livros.

## Observações

- Só o **ano** de publicação é real; a data fica em 1º de janeiro (ex.: Dom Casmurro → 1899-01-01).
- Os botões Google/GitHub do allauth usam `SocialApp` com client id fictício: aparecem na tela, mas o login social não funciona de verdade.
- O template `templates/allauth/layouts/base.html` só aplica um tema escuro; os formulários são os do allauth.
