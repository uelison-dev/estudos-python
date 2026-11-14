
"""
Script para cadastrar produtos no banco de dados Django.

Projeto: core
Aplicação: apps.produtos

Arquivo de dados:
    _dados/produtos.json

Execução:
    python _scripts/cadastrar_produtos.py
"""

import os
import sys
import json

from pathlib import Path


# ============================================================
# 1. IDENTIFICAR A RAIZ DO PROJETO
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# 2. CONFIGURAR O AMBIENTE DJANGO
# ============================================================

sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "core.settings"
)

import django

django.setup()


# ============================================================
# 3. IMPORTAR OS MODELS
# ============================================================

from apps.produtos.models import Categoria, Produto


# ============================================================
# 4. LOCALIZAR O ARQUIVO JSON
# ============================================================

ARQUIVO_DADOS = BASE_DIR / "_dados" / "produtos.json"


# ============================================================
# 5. CARREGAR OS DADOS
# ============================================================

def carregar_dados():

    if not ARQUIVO_DADOS.exists():

        raise FileNotFoundError(
            f"Arquivo não encontrado: {ARQUIVO_DADOS}"
        )

    with open(
        ARQUIVO_DADOS,
        "r",
        encoding="utf-8"
    ) as arquivo:

        dados = json.load(arquivo)

    if not isinstance(dados, list):

        raise ValueError(
            "O arquivo JSON deve conter uma lista de produtos."
        )

    return dados


# ============================================================
# 6. CADASTRAR OS PRODUTOS
# ============================================================

def cadastrar_produtos():

    dados = carregar_dados()

    cadastrados = 0
    existentes = 0
    ignorados = 0

    print("\nIniciando cadastro de produtos...")
    print("-" * 60)

    for item in dados:

        if not isinstance(item, dict):

            ignorados += 1

            print("[IGNORADO] Registro inválido.")

            continue

        nome = item.get("nome", "").strip()

        nome_categoria = item.get("categoria", "").strip()

        descricao = item.get("descricao", "")

        preco = item.get("preco")

        quantidade_estoque = item.get("quantidade_estoque", 0)

        # ----------------------------------------------------
        # VALIDAR CAMPOS OBRIGATÓRIOS
        # ----------------------------------------------------

        if not nome or not nome_categoria or preco is None:

            ignorados += 1

            print(
                f"[IGNORADO] Dados obrigatórios ausentes: {nome}"
            )

            continue

        # ----------------------------------------------------
        # LOCALIZAR A CATEGORIA
        # ----------------------------------------------------

        try:

            categoria = Categoria.objects.get(
                nome=nome_categoria
            )

        except Categoria.DoesNotExist:

            ignorados += 1

            print(
                f"[ERRO] Categoria não encontrada: {nome_categoria}"
            )

            continue

        # ----------------------------------------------------
        # CADASTRAR O PRODUTO
        # ----------------------------------------------------

        produto, criado = Produto.objects.get_or_create(

            nome=nome,

            defaults={
                "categoria": categoria,
                "descricao": descricao,
                "preco": preco,
                "quantidade_estoque": quantidade_estoque,
            }
        )

        if criado:

            cadastrados += 1

            print(
                f"[OK] Produto cadastrado: {produto.nome}"
            )

        else:

            existentes += 1

            print(
                f"[EXISTENTE] {produto.nome}"
            )

    # ========================================================
    # 7. EXIBIR RESULTADO
    # ========================================================

    print("\n" + "=" * 60)

    print("RESUMO DA IMPORTAÇÃO DE PRODUTOS")

    print("=" * 60)

    print(f"Total de registros no JSON: {len(dados)}")

    print(f"Novos produtos:             {cadastrados}")

    print(f"Produtos existentes:        {existentes}")

    print(f"Registros ignorados:        {ignorados}")

    print(f"Total no banco de dados:    {Produto.objects.count()}")

    print("=" * 60)

    print("Processamento finalizado!")


# ============================================================
# 8. EXECUTAR O SCRIPT
# ============================================================

if __name__ == "__main__":

    try:

        cadastrar_produtos()

    except Exception as erro:

        print("\nERRO AO CADASTRAR PRODUTOS:")

        print(erro)

        sys.exit(1)
