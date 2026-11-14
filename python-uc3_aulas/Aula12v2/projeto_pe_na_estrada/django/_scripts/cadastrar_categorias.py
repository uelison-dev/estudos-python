
"""
Script para cadastrar categorias no banco de dados Django.

Projeto: core
Aplicação: apps.produtos

Arquivo de dados:
    _dados/categorias.json

Execução:
    python _scripts/cadastrar_categorias.py
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
# 3. IMPORTAR O MODEL
# ============================================================

from apps.produtos.models import Categoria


# ============================================================
# 4. LOCALIZAR O ARQUIVO JSON
# ============================================================

ARQUIVO_DADOS = BASE_DIR / "_dados" / "categorias.json"


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
            "O arquivo JSON deve conter uma lista de categorias."
        )

    return dados


# ============================================================
# 6. CADASTRAR AS CATEGORIAS
# ============================================================

def cadastrar_categorias():

    dados = carregar_dados()

    cadastradas = 0
    existentes = 0
    ignoradas = 0

    print("\nIniciando cadastro de categorias...")
    print("-" * 50)

    for item in dados:

        if not isinstance(item, dict):
            ignoradas += 1
            print("[IGNORADA] Registro inválido.")
            continue

        nome = item.get("nome", "").strip()

        descricao = item.get("descricao", "")

        if not nome:
            ignoradas += 1
            print("[IGNORADA] Categoria sem nome.")
            continue

        categoria, criada = Categoria.objects.get_or_create(
            nome=nome,
            defaults={
                "descricao": descricao
            }
        )

        if criada:

            cadastradas += 1

            print(
                f"[OK] Categoria cadastrada: {categoria.nome}"
            )

        else:

            existentes += 1

            print(
                f"[EXISTENTE] {categoria.nome}"
            )

    # ========================================================
    # 7. EXIBIR RESULTADO
    # ========================================================

    print("\n" + "=" * 50)
    print("RESUMO DA IMPORTAÇÃO")
    print("=" * 50)

    print(f"Total de registros no JSON: {len(dados)}")
    print(f"Novas categorias:           {cadastradas}")
    print(f"Categorias existentes:      {existentes}")
    print(f"Registros ignorados:         {ignoradas}")
    print(f"Total no banco de dados:     {Categoria.objects.count()}")

    print("=" * 50)
    print("Processamento finalizado!")


# ============================================================
# 8. EXECUTAR O SCRIPT
# ============================================================

if __name__ == "__main__":

    try:

        cadastrar_categorias()

    except Exception as erro:

        print("\nERRO AO CADASTRAR CATEGORIAS:")
        print(erro)

        sys.exit(1)
