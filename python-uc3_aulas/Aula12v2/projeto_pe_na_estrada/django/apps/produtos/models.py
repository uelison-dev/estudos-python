from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models

class Categoria(models.Model):
    nome = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nome",
    )

    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descrição",
    )

    class Meta:
        # Nome legível exibido no Django Admin.
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

        # Ordena as categorias em ordem alfabética pelo nome.
        ordering = ["nome"]

    def __str__(self):
        # Representação textual do objeto.
        return self.nome