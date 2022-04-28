from django.db import models


class Address(models.Model):
    email = models.CharField(max_length=255, unique=True, db_index=True,
                             verbose_name='Адрес получателя')
    status = models.TextField(null=False, default='new', verbose_name='Статус клиента')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    def __str__(self):
        return self.email

    def clean(self):
        if self.email == '' or self.email == ' ':
            raise ValueError("email cant be '' or ''")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"