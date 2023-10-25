import re

from Domain.product.models import Product, ProductImage
from Domain.tag.models import Tag


def extracts_params(serializers):
    # recherche tous les mots qui commencent par un hash "#" dans le content
    tags = re.findall(r'#w+', serializers.validated_data['content'])
    # Supprime le caractère "#" de chaque tag
    tags = [tag[1:] for tag in tags]

    # on recupère toutes les images depuis la requête
    images = serializers.validated_data.pop("images")

    return tags, images


# Service qui permet d'ajouter la logique à notre Vue
def create_product(serializers, user):
    tags, images = extracts_params(serializers)
    product = serializers.save(
        owner=user,
        is_draft=serializers.validated_data['draft'],

    )

    for tag in tags:
        t, created = Tag.objects.get_or_create(name=tag.name)
        product.tags.add(t)

    for image in images:
        if image == images[0]:
            ProductImage.objects.get_or_create(image=image, product=product, default=True)
        ProductImage.objects.get_or_create(image=image, product=product)


def update(serializer, images):
    pass
    # TODO: Ici on passe la logique à passer.
