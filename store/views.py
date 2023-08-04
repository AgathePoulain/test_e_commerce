from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.formats import number_format
from store.models import Product, Cart, Item, Order
from django.contrib import messages
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Product
from store.serializers import ProductSerializer
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

    return redirect('index')


@api_view(['GET'])
def index_api(request):
    return Response({"Success": "The setup was successful"})


@api_view(['GET'])
def get_all_post(request):
    get_posts = Product.objects.all()  # This endpoint goes and gets all the posts in database
    serializer = ProductSerializer(get_posts, many=True)  # The data is converted to the correct format
    return Response(serializer.data)  # The suitable data is used by the response class


@api_view(['GET', 'POST'])
def create_post(request):
    data = request.data
    serializer = ProductSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Success": "The post was successfully created"}, status=201)
    else:
        return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def delete(request):
    post_id = request.data.get('post_id')
    try:
        post = Product.objects.get(id=post_id)
        post.delete()
        return Response({"Success": "The post was successfully deleted"}, status=200)
    except Product.DoesNotExist:
        return Response({"Error": "The post does not exist"}, status=404)


@api_view(['GET'])
def get_post(request):
    post_id = request.data.get('post_id')
    try:
        post = Product.objects.get(id=post_id)
        serializer = ProductSerializer(post)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({"Error": "The post does not exist"}, status=404)


@api_view(['PUT'])
def update_post(request):
    post_id = request.data.get('post_id')
    get_new_name = request.data.get('new_name')
    get_new_price = request.data.get('new_price')
    get_new_stock = request.data.get('new_stock')
    get_new_description = request.data.get('new_description')
    get_new_thumbnail = request.data.get('new_thumbnail')
    try:
        post = Product.objects.get(id=post_id)
        if get_new_name:
            post.title = get_new_name
        if get_new_price:
            post.price = get_new_price
        if get_new_stock:
            post.stock = get_new_stock
        if get_new_description:
            post.description = get_new_description
        if get_new_description:
            post.thumbnail = get_new_thumbnail
        post.save()
        return Response({"Success": "The product was successfully updated"}, status=200)
    except Product.DoesNotExist:
        return Response({"Error": "The product does not exist"}, status=404)
