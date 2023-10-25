from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from Domain.brand.models import Brand
from Domain.category.models import EndCategory, SubCategory
from Domain.account.models import User


class Size(models.Model):
    size = models.CharField(max_length=255)
    subCategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.size


class Product(models.Model):

    PRODUCT_STATES = (
        ('NEVER_USE', 'NEVER_USE'),
        ('VERY_GOOD', 'VERY_GOOD'),
        ('GOOD', 'GOOD'),
    )

    PRODUCT_SIZES = (
        ('XXL', 'XXL'),
        ('XL', 'XL'),
        ('L', 'L'),
        ('M', 'M'),
    )

    RESERVE_DAYS = 3

    title = models.CharField(max_length=255)
    price = models.PositiveIntegerField(null=False)
    product_slug = models.SlugField(max_length=255, allow_unicode=False, null=False)
    content = models.TextField()
    active = models.BooleanField(default=True)
    brand = models.ManyToManyField(Brand)
    size = models.CharField(choices=PRODUCT_SIZES, default='XXL', max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    endCategory = models.ForeignKey(EndCategory, on_delete=models.CASCADE)
    rank = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=False)
    for_rental = models.BooleanField(default=False)  # à louer
    rental_days = models.IntegerField(null=True)  # nombre de jours de location.
    is_reserved = models.BooleanField(default=False)  # reserve
    reserved_end = models.DateTimeField(null=True)  # date de fin de la reservation.
    change = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    is_draft = models.BooleanField(default=True)
    state = models.CharField(choices=PRODUCT_STATES, default='NEVER_USE', null=False, max_length=25)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.product_slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"


class ProductImage(models.Model):
    image = models.ImageField(upload_to="assets/uploads/products", default="", null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
