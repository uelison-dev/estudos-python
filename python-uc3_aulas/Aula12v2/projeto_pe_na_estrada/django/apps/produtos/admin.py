from django.contrib import admin
from .models import (
    Categoria,
    Produto,
    Cliente,
    EnderecoEntrega,
    Pedido,
    ItemPedido,
    ComentarioAvaliacao,
    )
# Register your models here.

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):

    list_display = ["id", "nome", "descricao"]

    search_fields = ["nome", "descricao"]

    ordering = ["nome"]

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):

    list_display = ["nome", "categoria", "descricao", "quantidade_estoque", "preco", "criado_em", "atualizado_em"]
    
    search_fields = ["nome", "categoria", "descricao"]
    
    ordering = ["nome", "categoria"]

#@admin.register(Cliente)
#class ClienteAdmin(admin.ModelAdmin):

    #list_display = ["id", "nome", "descricao"]

 #   search_fields = ["nome", "descricao"]

   # ordering = ["nome"]


