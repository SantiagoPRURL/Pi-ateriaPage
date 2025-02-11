from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Product(models.Model):
    CHOICES = [
        ('piñatas-niño', 'Piñatas-niño'),
        ('piñatas-niña', 'Piñatas-niña'),
        ('piñatas-adulto', 'Piñatas-adulto'),
        ('porcelanicron-matrimonio', 'Porcelanicron-matrimonio'),
        ('porcelanicron-quinceañeras', 'Porcelanicron-quinceañeras'),
        ('porcelanicron-animados', 'Porcelanicron-animados'),
        ('porcelanicron-profesiones', 'Porcelanicron-profesiones'),
        ('porcelanicron-comunion', 'Porcelanicron-comunion'),
        ('porcelanicron-grados', 'Porcelanicron-grados'),
        ('stickers-niño', 'Stickers-niño'),
        ('stickers-niña', 'Stickers-niña'),
        ('stickers-adulto', 'Stickers-adulto'),
        ('toppers-cumpleanos', 'Toppers-cumpleanos'),
        ('toppers-feliz-dia', 'Toppers-feliz-dia'),  
        ('toppers-aniversario', 'Toppers-aniversario'),
        ('toppers-grados', 'Toppers-grados'),
        ('toppers-comunion', 'Toppers-comunion'),
        ('toppers-numeros', 'Toppers-numeros'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=255, choices=CHOICES, default='others')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    