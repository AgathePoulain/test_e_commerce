from django.db import models
from django.urls import reverse

from shop.settings import AUTH_USER_MODEL

"""
Réflexion sur le projet, les éléments requis et leurs types : 

Product
- Nom (texte)
- Prix (integer)
- Quantité en stock (integer)
- Description (chainte de caractères)
- Image

"""


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    description = models.TextField(blank=True)  # Pouvoir ajouter la description plus tard
    thumbnail = models.ImageField(upload_to="products", blank=True, null=True)

    # Ou sont les images associées à ce modèle ?

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product", kwargs={"pk": self.pk})
    # Récupérer à partir du nom de l'url et des infos passées à l'url, l'adresse qui nous amène à la page du produit


"""
ARTICLE : 
- user -->  relié à un autre modèle
- produit --> relié à un autre modèle --> ORM (Object Relational Mapping)
- quantité --> integer
- commandé ou non --> booléen

"""


class Item(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Si user supprime son compte, on supprime en cascade tous les articles qu'il a pu réunir
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    price = models.FloatField(default=0.0)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    def get_price(self):
        return self.quantity * self.product.price

    def plus_quantity(self):
        if self.quantity > 0:
            self.quantity += 1
            self.product.stock -= 1
            self.product.save()
            self.save()

    def minus_quantity(self):
        if self.quantity > 0:
            self.quantity -= 1
            self.product.stock += 1
            self.product.save()
            self.save()


"""
PANIER : 
- user -->  relié à un autre modèle
- articles --> relié à un autre modèle --> ORM (Object Relational Mapping)
- commandé ou non --> booléen
- date de la commande 

"""


class Cart(models.Model):  # Modèle qui regroupe les commandes en cours
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)  # un seul panier par user
    items = models.ManyToManyField(Item)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    def delete_item(self, pk):
        try:
            item_to_delete = self.items.get(item_pk=pk)
            item_to_delete.delete()
        except Item.DoesNotExist:
            pass

    # Avoir les infos des articles commandés même une fois supprimés du panier


class Order(models.Model):  # Modèle qui regroupe les commandes validées
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Item)
    ordered = models.BooleanField(default=True)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    def validate_order(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            from django.utils import timezone
            order.ordered_date = timezone.now()
            order.save()
        self.orders.clear()
        super().delete(*args, **kwargs)
