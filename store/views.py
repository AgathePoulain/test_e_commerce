from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.formats import number_format
from store.models import Product, Cart, Item, Order
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse


def index(request):
    products = Product.objects.all()
    return render(request, 'store/index2.html', context={"products": products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)  # Retourne le modèle s'il existe dans la bdd sinon renvoie erreur
    return render(request, 'store/detail.html', context={"product": product})


def add_to_cart(request, pk):  # Ajouter un article au panier
    user = request.user  # Récupérer user
    product = get_object_or_404(Product, pk=pk)  # Récupérer produit s'il existe

    # Récupérer le panier s'il existe et le créer s'il n'existe pas
    panier, _ = Cart.objects.get_or_create(user=user)
    # _ : Pour dire qu'on n'utilise pas la seconde variable

    if product.stock > 0:  # Vérifier qu'il y a bien des produits en stock
        item, created = Item.objects.get_or_create(user=user, product=product, defaults={"quantity": 0})
        item.quantity += 1
        item.save()
        panier.items.add(item)
        panier.save()

        messages.success(request, f"L'article {product.name} a été ajouté au panier.")
        product.stock -= 1
        product.save()
    else:
        messages.warning(request, f"L'article {product.name} est actuellement indisponible.")
    return redirect(reverse("product", kwargs={"pk": pk}))


def plus_quantity(request, pk):
    user = request.user  # Récupérer user
    item = get_object_or_404(Item, user=user, pk=pk)
    item.plus_quantity()
    return redirect('cart')


def minus_quantity(request, pk):
    user = request.user  # Récupérer user
    item = get_object_or_404(Item, user=user, pk=pk)
    item.minus_quantity()
    return redirect('cart')


def cart(request):  # Afficher le panier
    user = request.user
    panier = get_object_or_404(Cart, user=user)
    total_amount = 0.0

    for item in panier.items.all():
        price = item.get_price()
        total_amount += price

    formatted_total_amount = formatter(total_amount)
    return render(request, 'store/cart.html',
                  context={"items": panier.items.all(), "total_amount": formatted_total_amount})


def formatter(amount):
    formatted_amount = number_format(amount, decimal_pos=1, use_l10n=True)
    parts = formatted_amount.split(",")
    if len(parts[0]) >= 4:
        parts[0] = " ".join([parts[0][:-3], parts[0][-3:]])
    return f"{','.join(parts)}"


def delete_item(request, pk):
    user = request.user
    item = get_object_or_404(Item, user=user, pk=pk)
    product = item.product
    product.stock += item.quantity  # Ajouter la quantité du produit supprimé au stock dans le magasin
    product.save()
    item.delete()
    return redirect('cart')


def validate_cart(request):
    """
    Principe de fonctionnement de la vue validate_cart :
    1 : Récupérer le panier de l'utilisateur actuel.
    2 : Créer un nouvel objet Order avec l'utilisateur actuel.
    3 : Ajouter tous les articles du panier à l'objet Order.
    4 : Marquer chaque article du panier comme étant commandé (ordered=True).
    5 : Définir la date de commande pour chaque article.
    6 : Vider le panier après la validation de la commande.

    """
    # 1
    user = request.user
    panier = get_object_or_404(Cart, user=user)

    if panier.items.exists():
        # 2
        order = Order.objects.create(user=user, ordered=True, ordered_date=timezone.now())

        # 3
        for item in panier.items.all():
            order.orders.add(item)

        # 4 + 5
        order.orders.update(ordered=True, ordered_date=timezone.now())

        # 6
        # panier.items.clear()
        for item in panier.items.all():
            item.delete()

        messages.success(request, "Votre commande a été validée avec succès.")
    else:
        messages.warning(request, "Votre panier est vide.")

    return redirect('index')