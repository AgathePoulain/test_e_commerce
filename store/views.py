from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from store.models import Product, Cart, Order


def index(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', context={"products":products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug) # Retourne le modèle s'il existe dans la bdd sinon renvoie erreur
    return render(request, 'store/detail.html', context={"product":product})

def add_to_cart(request, slug):
    user = request.user # Récupérer user
    product = get_object_or_404(Product, slug=slug) # Récupérer produit s'il existe

    # Récupérer le panier s'il existe et le créer s'il n'existe pas
    cart, _ = Cart.objects.get_or_create(user=user)
    # _ : pour dire qu'on n'utilise pas la seconde variable

    # Récupérer l'ordre
    order, created = Order.objects.get_or_create(user=user, ordered=False, product=product)
    if created: # objet n'existait pas encore dans le panier
        cart.orders.add(order)
        cart.save()
    else : # objet existait déjà dans le panier, on incrémente sa quantité
        order.quantity += 1
        order.save()
    return redirect(reverse("product", kwargs={"slug":slug}))

def cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, 'store/cart.html', context={"orders":cart.orders.all()})

def delete_cart(request):
    if cart:= request.user.cart: # SYNTHAXE !!
        cart.orders.all().delete()
        cart.delete()
    return redirect('index')