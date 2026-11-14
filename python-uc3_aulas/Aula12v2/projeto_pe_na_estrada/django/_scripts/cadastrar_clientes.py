
"""
Script para cadastrar clientes no banco de dados Django.

Projeto: core
Aplicação: apps.produtos

Arquivo de dados:
    _dados/clientes.json

Execução:
    python _scripts/cadastrar_clientes.py
"""

import os
import sys
import json

from pathlib import Path
from datetime import date

from django.db import transaction
from django.contrib.auth import get_user_model


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

from apps.produtos.models import Cliente

# Obtém o model de usuário configurado no projeto.

User = get_user_model()


# ============================================================
# 4. LOCALIZAR O ARQUIVO JSON
# ============================================================

ARQUIVO_DADOS = BASE_DIR / "_dados" / "clientes.json"


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
            "O arquivo JSON deve conter uma lista de clientes."
        )

    return dados


# ============================================================
# 6. CADASTRAR USUÁRIO
# ============================================================

def cadastrar_usuario(item):

    username = item.get("username", "").strip()

    if not username:

        raise ValueError("Username não informado.")

    campo_usuario = User.USERNAME_FIELD

    usuario, criado = User.objects.get_or_create(

        **{campo_usuario: username},

        defaults={
            "email": item.get("email", ""),
            "first_name": item.get("first_name", ""),
            "last_name": item.get("last_name", ""),
        }
    )

    if criado:

        # Não define uma senha conhecida para os usuários de teste.
        usuario.set_unusable_password()

        usuario.save()

    return usuario, criado


# ============================================================
# 7. CADASTRAR CLIENTE
# ============================================================

def cadastrar_cliente(item):

    # --------------------------------------------------------
    # VALIDAR DADOS
    # --------------------------------------------------------

    cpf = item.get("cpf", "").strip()

    if not cpf:

        raise ValueError("CPF não informado.")

    sexo = item.get("sexo", "N")

    sexos_validos = {
        valor for valor, descricao in Cliente.Sexo.choices
    }

    if sexo not in sexos_validos:

        raise ValueError(
            f"Sexo inválido para o cliente: {sexo}"
        )

    # --------------------------------------------------------
    # CADASTRAR OU LOCALIZAR USUÁRIO
    # --------------------------------------------------------

    usuario, usuario_criado = cadastrar_usuario(item)

    # --------------------------------------------------------
    # VERIFICAR DATA DE NASCIMENTO
    # --------------------------------------------------------

    data_nascimento = item.get("data_nascimento")

    if data_nascimento:

        data_nascimento = date.fromisoformat(
            data_nascimento
        )

    # --------------------------------------------------------
    # CADASTRAR OU LOCALIZAR CLIENTE
    # --------------------------------------------------------

    cliente, cliente_criado = Cliente.objects.get_or_create(

        usuario=usuario,

        defaults={
            "telefone": item.get("telefone") or None,
            "sexo": sexo,
            "nome_social": item.get("nome_social") or None,
            "data_nascimento": data_nascimento,
            "cpf": cpf,
        }
    )

    return cliente, cliente_criado, usuario_criado


# ============================================================
# 8. PROCESSAR IMPORTAÇÃO
# ============================================================

def cadastrar_clientes():

    dados = carregar_dados()

    clientes_cadastrados = 0
    clientes_existentes = 0
    usuarios_criados = 0
    ignorados = 0

    print("\nIniciando cadastro de clientes...")
    print("-" * 60)

    # Toda a importação será executada em uma transação.
    # Se ocorrer um erro, os registros desta execução
    # serão revertidos.

    with transaction.atomic():

        for item in dados:

            if not isinstance(item, dict):

                ignorados += 1

                print("[IGNORADO] Registro inválido.")

                continue

            try:

                cliente, cliente_criado, usuario_criado = (
                    cadastrar_cliente(item)
                )

                if usuario_criado:
                    usuarios_criados += 1

                if cliente_criado:

                    clientes_cadastrados += 1

                    print(
                        f"[OK] Cliente cadastrado: "
                        f"{cliente.usuario.username}"
                    )

                else:

                    clientes_existentes += 1

                    print(
                        f"[EXISTENTE] "
                        f"{cliente.usuario.username}"
                    )

            except Exception as erro:

                raise RuntimeError(
                    f"Erro ao processar o cliente "
                    f"{item.get('username', 'desconhecido')}: {erro}"
                ) from erro

    # ========================================================
    # 9. EXIBIR RESULTADO
    # ========================================================

    print("\n" + "=" * 60)

    print("RESUMO DA IMPORTAÇÃO DE CLIENTES")

    print("=" * 60)

    print(f"Total de registros no JSON: {len(dados)}")

    print(f"Novos usuários:             {usuarios_criados}")

    print(f"Novos clientes:             {clientes_cadastrados}")

    print(f"Clientes existentes:        {clientes_existentes}")

    print(f"Registros ignorados:        {ignorados}")

    print(f"Total de clientes no banco: {Cliente.objects.count()}")

    print("=" * 60)

    print("Processamento finalizado!")


# ============================================================
# 10. EXECUTAR O SCRIPT
# ============================================================

if __name__ == "__main__":

    try:

        cadastrar_clientes()

    except Exception as erro:

        print("\nERRO AO CADASTRAR CLIENTES:")

        print(erro)

        sys.exit(1)
