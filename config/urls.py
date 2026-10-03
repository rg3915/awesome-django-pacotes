from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter

from loja.api import LivroViewSet
from loja.views import relatorio_n_mais_1, relatorio_otimizado

router = DefaultRouter()
router.register("livros", LivroViewSet)

urlpatterns = [
    path("", RedirectView.as_view(url="/api/livros/")),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path("accounts/", include("allauth.urls")),
    path("silk/", include("silk.urls", namespace="silk")),
    path("relatorio/", relatorio_n_mais_1),
    path("relatorio-otimizado/", relatorio_otimizado),
]
