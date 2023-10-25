from Domain.abstract.Category.models import AbstractCategoryManager, AbstractCategoryModel
from django.db import models


class CategoryManager(AbstractCategoryManager):
    pass


class SubCategoryManager(AbstractCategoryManager):
    pass


class EndCategoryManager(AbstractCategoryManager):
    pass


class Category(AbstractCategoryModel):
    category_slug = models.SlugField(max_length=255, allow_unicode=False, null=True)
    objects = CategoryManager()

    def __str__(self):
        return f"{self.name}"


class SubCategory(AbstractCategoryModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category_slug = models.SlugField(max_length=255, allow_unicode=False, null=True)
    objects = SubCategoryManager()

    def __str__(self):
        return f"{self.name}"


class EndCategory(AbstractCategoryModel):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    end_category_slug = models.SlugField(max_length=255, allow_unicode=False, null=True)
    objects = EndCategoryManager()

    def __str__(self):
        return f"{self.name}"



