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

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):

    list_display = ["foto", "usuario", "nome_social", "telefone", "data_nascimento", "sexo", "cpf"]

    search_fields = ["usuario", "cpf"]

    ordering = ["usuario", "cpf"]

@admin.register(EnderecoEntrega)
class EnderecoEntregaAdmin(admin.ModelAdmin):

    list_display = ["cliente", "logradouro", "numero", "complemento", "bairro", "cidade", "estado", "cep"]

    search_fields = ["cliente", "bairro", "cidade", "estado", "cep"]

    ordering = ["cliente"]

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):

    list_display = ["cliente", "status", "endereco_entrega", "criado_em", "atualizado_em"]

    search_fields = ["cliente", "status", "endereco_entrega", "criado_em"]

    ordering = ["cliente", "status"]

@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):

    list_display = ["pedido", "produto", "quantidade", "preco_unitario"]

    search_fields = ["pedido", "produto"]

    ordering = ["pedido"]

@admin.register(ComentarioAvaliacao)
class ComentarioAvaliacaoAdmin(admin.ModelAdmin):

    list_display = ["cliente", "produto", "criado_em", "nota", "texto"]

    search_fields = ["cliente", "produto"]

    ordering = ["produto", "cliente"]