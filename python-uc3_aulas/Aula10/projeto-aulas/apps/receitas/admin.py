##
# APP: receitas - admin.py
##
# Importa o módulo de administração do Django.
# Ele fornece admin.site, o decorador @admin.register e a classe ModelAdmin.
from django.contrib import admin

# Importa os modelos que serão exibidos no painel administrativo.
# O ponto inicial indica importação relativa: estamos importando
# do arquivo models.py localizado na mesma aplicação.
from .models import Categoria, Receita


# Registra o modelo Categoria com a configuração padrão do Django Admin.
admin.site.register(Categoria)

# Registra o modelo Receita com a configuração padrão do Django Admin.
admin.site.register(Receita)

