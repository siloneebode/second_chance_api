from django.db import models


class Brand(models.Model):
    brand_slug = models.SlugField(max_length=255, allow_unicode=False, null=True)
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

