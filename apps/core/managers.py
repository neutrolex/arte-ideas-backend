from django.db import models


class TenantManager(models.Manager):

    def get_queryset(self):

        return super().get_queryset()
