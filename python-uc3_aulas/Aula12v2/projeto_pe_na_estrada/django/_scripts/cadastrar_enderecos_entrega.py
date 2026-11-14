
"""
Script para cadastrar endereços de entrega no banco de dados Django.

Projeto: core
Aplicação: apps.produtos

Arquivo de dados:
    _dados/enderecos_entrega.json

Execução:
    python _scripts/cadastrar_enderecos_entrega.py
"""

import os
import sys
import json

from pathlib import Path

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

from apps.produtos.models import Cliente, EnderecoEntrega

User = get_user_model()


# ============================================================
# 4. LOCALIZAR O ARQUIVO JSON
# ============================================================

ARQUIVO_DADOS = (
    BASE_DIR / "_dados" / "enderecos_entrega.json"
)


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
            "O arquivo JSON deve conter uma lista de endereços."
        )

    return dados


# ============================================================
# 6. LOCALIZAR O CLIENTE
# ============================================================

def localizar_cliente(username):

    campo_usuario = User.USERNAME_FIELD

    # Localiza o cliente pelo username do usuário relacionado.

    filtro = {
        f"usuario__{campo_usuario}": username
    }

    try:

        return Cliente.objects.get(**filtro)

    except Cliente.DoesNotExist:

        raise ValueError(
            f"Cliente não encontrado para o usuário: {username}"
        )

    except Cliente.MultipleObjectsReturned:

        raise ValueError(
            f"Mais de um cliente encontrado para: {username}"
        )


# ============================================================
# 7. CADASTRAR ENDEREÇO DE ENTREGA
# ============================================================

def cadastrar_endereco(item):

    # --------------------------------------------------------
    # IDENTIFICAR O CLIENTE
    # --------------------------------------------------------

    username = item.get("username", "").strip()

    if not username:

        raise ValueError(
            "Username não informado no endereço."
        )

    cliente = localizar_cliente(username)

    # --------------------------------------------------------
    # PREPARAR OS DADOS DO ENDEREÇO
    # --------------------------------------------------------

    campos_obrigatorios = [
        "logradouro",
        "numero",
        "bairro",
        "cidade",
        "estado",
        "cep",
    ]

    for campo in campos_obrigatorios:

        if not str(item.get(campo, "")).strip():

            raise ValueError(
                f"Campo obrigatório não informado: {campo}"
            )

    estado = item["estado"].strip().upper()

    if len(estado) != 2:

        raise ValueError(
            f"Estado inválido para o cliente {username}: {estado}"
        )

    endereco_dados = {
        "logradouro": item["logradouro"].strip(),
        "numero": item["numero"].strip(),
        "complemento": (
            item.get("complemento") or ""
        ).strip() or None,
        "bairro": item["bairro"].strip(),
        "cidade": item["cidade"].strip(),
        "estado": estado,
        "cep": item["cep"].strip(),
    }

    # --------------------------------------------------------
    # CADASTRAR OU LOCALIZAR ENDEREÇO
    # --------------------------------------------------------

    endereco, criado = EnderecoEntrega.objects.get_or_create(

        cliente=cliente,

        **endereco_dados
    )

    return endereco, criado


# ============================================================
# 8. PROCESSAR IMPORTAÇÃO
# ============================================================

def cadastrar_enderecos_entrega():

    dados = carregar_dados()

    cadastrados = 0
    existentes = 0

    print("\nIniciando cadastro de endereços de entrega...")
    print("-" * 65)

    # A importação inteira será executada em uma transação.
    # Em caso de erro, todos os novos registros serão revertidos.

    with transaction.atomic():

        for item in dados:

            if not isinstance(item, dict):

                raise ValueError(
                    "Foi encontrado um registro inválido no JSON."
                )

            endereco, criado = cadastrar_endereco(item)

            if criado:

                cadastrados += 1

                print(
                    f"[OK] Endereço cadastrado: "
                    f"{endereco.cliente.usuario.get_username()} - "
                    f"{endereco.cidade}/{endereco.estado}"
                )

            else:

                existentes += 1

                print(
                    f"[EXISTENTE] "
                    f"{endereco.cliente.usuario.get_username()} - "
                    f"{endereco.cidade}/{endereco.estado}"
                )

    # ========================================================
    # 9. EXIBIR RESULTADO
    # ========================================================

    print("\n" + "=" * 65)

    print("RESUMO DA IMPORTAÇÃO DE ENDEREÇOS")

    print("=" * 65)

    print(f"Total de registros no JSON: {len(dados)}")

    print(f"Novos endereços:            {cadastrados}")

    print(f"Endereços existentes:       {existentes}")

    print(
        f"Total de endereços no banco: "
        f"{EnderecoEntrega.objects.count()}"
    )

    print("=" * 65)

    print("Processamento finalizado!")


# ============================================================
# 10. EXECUTAR O SCRIPT
# ============================================================

if __name__ == "__main__":

    try:

        cadastrar_enderecos_entrega()

    except Exception as erro:

        print("\nERRO AO CADASTRAR ENDEREÇOS:")

        print(erro)

        sys.exit(1)
