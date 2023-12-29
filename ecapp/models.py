from django.db import models


class ItemModel(models.Model):
    title = models.CharField(null=True, blank=True) # 必須フィールド
    name = models.CharField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    item_image = models.ImageField(upload_to="", null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title