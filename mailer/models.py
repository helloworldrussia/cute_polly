from django.db import models


class Address(models.Model):
    email = models.CharField(max_length=255, unique=True, null=False, db_index=True,
                             verbose_name='Адрес получателя')
    status = models.TextField(null=False, default='new', verbose_name='Статус клиента')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'База рассылки'