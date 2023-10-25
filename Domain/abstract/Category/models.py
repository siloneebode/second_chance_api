from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404


class AbstractCategoryManager(models.Manager):

    def get_object_by_slug(self, slug):
        try:
            category = self.get(slug=slug)
            return category
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404

    def get_object_by_2_param(self, category_slug, slug):
        try:
            category = self.get_object_by_slug(category_slug)
            sub_category = self.get(category=category, slug=slug)
            return sub_category
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404

    def get_object_by_3_param(self, category_slug, subcategory_slug, slug):
        try:
            category = self.get_object_by_slug(category_slug)
            sub_category = self.get_object_by_2_param(category_slug, subcategory_slug)
            end_category = self.get(sub_category=sub_category, slug=slug)
            return end_category
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404


class AbstractCategoryModel(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = AbstractCategoryManager()

    class Meta:
        abstract = True
