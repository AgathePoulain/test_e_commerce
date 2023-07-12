#  -------- CREER UN SITE E COMMERCE --------

# ----- 1 : ENVIRONNEMENT DE TRAVAIL -----
# pip install django
# django-admin startproject shop .

# ======================================== GESTION DES PRODUITS =====================================================================

# ----- 2 : CREATION DES MODELES -----
# python manage.py startapp store --> Ajouter à shop --> settings.py


# ----- 3 : PLANIFICATION DES MODELES -----
# application store --> models.py -->
"""
Réflexion sur le projet, les éléments requis et leurs types :

Product
- Nom (texte)
- Prix (integer)
- Quantité en stock (integer)
- Description (chainte de caractères)
- Image

"""

# ----- 4 : CREATION DU MODELE PRODUCT -----
# application store --> models.py -->
# class Product(models.Model):
#     name = models.CharField(max_length=128)
#     price = models.FloatField(default=0.0)
#     stock = models.IntegerField(default=0)
#     description = models.TextField(blank=True) # Pouvoir ajouter la description plus tard
#     thumbnail = models.ImageField(upload_to="products", blank=True, null=True) # Ou sont les images associées à ce modèle ?

#     def __str__(self):
#         return self.name


# ----- 5 : CREER ET APPLIQUER LES MIGRATIONS -----
# Terminal -->
# pip install pillow
# pip freeze > requirements.txt
# python manage.py makemigrations
# Les migrations permettent de répertorier tous les changements apportés à notre bdd

# python manage.py migrate
# Utiliser TablePlus pour tester la base de données


# ----- 6 : ENREGISTRER LES MODELES DANS L ADMIN -----
# Ajouter visuelement des modèles dans notre bdd
# Enregistrer les modèles --> admin.py --> admin.site.register(Product)
# Terminal --> python manage.py runserver
# python manage.py createsuperuser


# ----- 7 : CREER LE TEMPLATE DE BASE -----
# Créer dossier templates --> fichier html
# settings.py -->
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [BASE_DIR/"templates"],
#         'APP_DIRS': True,}
# On va étendre le template à tout le site


# ----- 8 : CREER PAGE ACCEUIL -----
# On crée un fichier index.html dans store
# On va étendre le modèle de base.html à index.html et ainsi éviter de toujours tout recopier dans le code html

# base.html -->
# <body>
# {% block content %}
# {% end block %}
# </body>

# index.html -->
# {% extends 'base.html' %}
# {% block content %}
# <h1>La boutique de la Grange Ariégeoise</h1>
# {% end block %}

# ----- 9 : CREER LE CHEMIN POUR LA PAGE D ACCEUIL -----
# store.views.py --> def index(request):
#     return render(request, 'store/index.html')

# shop.urls.py -->    path('', index, name='index'),


# ----- 10 : AFFICHER TOUS LES PRODUITS -----
# views.py
# from store.models import Product
# def index(request):
#     products = Product.objects.all()
#     return render(request, 'store/index.html', context={"products":products})

# index.html -->
# {% for product in products %}
#     <h2>{{product.name}}</h2>
#     <img src="{{product.thumbnail.url}}" alt="{{product.name}}" style = "max-width: 300px;">
# {% endfor %}

# Dans urls.py --> Pour traiter les images et les afficher correctement --> concaténation urlpatterns + static
# from shop import settings
# urlpatterns = [
#     path('', index, name='index'),
#     path('admin/', admin.site.urls),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Dans settings.py --> Pour que la concaténation sur urls.py fonctionne
# MEDIA_URL = "/media/"
# MEDIA_ROOT = BASE_DIR/"media"


# ----- 11 : AFFICHER PAGE DETAIL UN PRODUIT -----
# models.py --> slug = models.SlugField(max_length=128)
# urls.py --> path('product/<str:slug>', product_detail, name='product'),

# views.py -->
# def product_detail(request, slug):
#     product = get_object_or_404(Product, slug=slug) # Retourne le modèle s'il existe dans la bdd sinon renvoie erreur
#     return HttpResponse(f"{product.name} {product.price}€")

# Puis faire -->
# def product_detail(request, slug):
#     product = get_object_or_404(Product, slug=slug) # Retourne le modèle s'il existe dans la bdd sinon renvoie erreur
#     return render(request, 'store/detail.html', context={"product":product})

# ----- 12 : LIER PAGE ACCEUIL ET PRODUITS -----
# base.html -->
# <a href="{% url 'index' %}">
#     <h1>La boutique de la Grange Ariégeoise</h1>
# </a>
# Ainsi en cliquant sur "La boutique" on revient sur le lien url de index (qui est ici la page d'acceuil)

# index.html --> <a href="{% url 'product' slug=product.slug %}"><h2>{{product.name}}</h2></a>

# models.py --> accéder à la page de l'instance, bouton voir sur le site sur la page admin pour chaque article
# def get_absolute_url(self):
#    return reverse("product", kwargs={"slug": self.slug})
# Récupérer à partir du nom de l'url et des infos passées à l'url, l'adresse qui nous amène à la page du produit

# index.html --> <a href="{{ product.get_absolute_url }}"><h2>{{product.name}}</h2></a>


# ======================================== GESTION DES UTILISATEURS =====================================================================

# ----- 13 : CREER MODELE UTILISATEUR -----
# Créer une application et la déclarer dans settings.py
# terminal --> python manage.py startapp accounts
# models.py --> création classe
# AbstractUser et AbstractBaseUser (rien dedans sauf gestion du mot de passe et authentification, pas d'autres champs générés)
# Ici on utilise AbstractUser pour ses fonctionnalités déjà existantes

# from django.contrib.auth.models import AbstractUser
# class Shopper(AbstractUser):
#     pass

# settings.py --> AUTH_USER_MODEL = "accounts.Shopper"
# Supprimer l'ancienne bd.sqlite3
# terminal --> python manage.py makemigrations
# python manage.py migrate
# python manage.py createsuperuser


# ----- 14 : FORMULAIRE INSCRIPTION UTILISATEUR -----
# accounts --> templates --> accounts --> signup.html
# label --> afficher du texte
# input --> récupérer des données

# accounts.views.py --> def signup(request):
#     return render(request, 'accounts/signup.html')

# urls.py --> path('signup/', signup, name='signup'),

# base.html --> Pour afficher inscription si user pas connecté
# {% if not user.is_authenticated %}
# <a href="{% url 'signup' %}">Inscription</a>
# {% endif %}


# ----- 15 : RECUPERER LES INFOS DU FORMULAIRE -----
# accounts.views.py -->
# Récupérer la classe utilisateur
# User = get_user_model()
# def signup(request):
#     if request.method == "POST":
#         # Traiter le formulaire
#         username = request.POST.get("username") # Récupérer les clés du dictionnaire = "name" dans input
#         password = request.POST.get("password")
#         user = User.objects.create_user(username=username, password=password) # Créer l'utilisateur
#         login(request, user) # Connecter l'utilisateur au site
#         return redirect('index') # rediriger vers la vue d'acceuil
#
#     return render(request, 'accounts/signup.html')


# ----- 16 : AFFICHER UTILISATEUR CONNECTE ET DECONNEXION -----
# accounts --> admin.py --> admin.site.register(Shopper) Afficher les utilisateurs dans la partie admin de mon site
# signup.html -->
# {% if user.is_authenticated %}
#     Bienvenue {{ user.username }}
#     <a href="{% url 'logout' %}">Déconnexion</a>
#
# {% else %}
# <a href="{% url 'signup' %}">Inscription</a>
# {% endif %}

# views.py -->
# def logout_user(request):
#     logout(request)
#     return redirect ('index')

# urls.py --> path('logout/', logout_user, name='logout'),

# Très facile de déconnecter l'user


# ----- 17 : CREER LA VUE DE CONNEXTION -----
# accounts --> login.html --> créer le template de connexion
# accounts --> views.py --> créer la vue login_user pour connecter l'user et le rediriger vers la page d'acceuil
# def login_user(request):
#     if request.method == 'POST':
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(username=username, password=password) # Vérifier que les infos données sont les bonnes et bien dans la bdd
#         if user: # Connecter l'user et rediriger vers la page d'acceuil
#             login(request, user)
#             return redirect('index')
#     return render (request, 'accounts/login.html')

# base.html --> <a href="{% url 'login' %}">Connexion</a>

# urls.py --> path('login/', login_user, name='login'),


# ======================================== GESTION DU PANIER =====================================================================

# ----- 18 : PLANIFIER LES MODELES -----
"""
ARTICLE : 
- user -->  relié à un autre modèle
- produit --> relié à un autre modèle --> ORM (Object Relational Mapping)
- quantité --> integer
- commandé ou non --> booléen

"""

"""
PANIER : 
- user -->  relié à un autre modèle
- articles --> relié à un autre modèle --> ORM (Object Relational Mapping)
- commandé ou non --> booléen
- date de la commande 

"""

# ----- 19 : CREER LE MODELE ORDRER -----
# strore --> models.py -->
# class Order(models.Model):
#     user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE) # Si user supprime son compte, on supprime en cascade tous les articles qu'il a pu réunir
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     ordered = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f"{self.product.name} ({self.quantity})"

# store --> admin.py --> admin.site.register(Order)
# Créer les migrations dans le terminal --> python manage.py makemigrations --> python manage.py migrate


# ----- 20 : CREER LE MODELE CART -----
# models.py -->
# class Cart(models.Model):
#     user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE) # un seul panier par user
#     orders = models.ManyToManyField(Order)
#     ordered = models.BooleanField(default=False)
#     ordered_date = models.DateTimeField(blank=True, null=True)
#
#     def __str__(self):
#         return self.user.username

# store --> admin.py --> admin.site.register(Cart)
# Créer les migrations dans le terminal --> python manage.py makemigrations --> python manage.py migrate (appliquer les migrations dans la bdd)


# ----- 21 : AJOUTER UN ARTICLE DANS LE PANIER -----
# Ajouter un bouton -->
# shop --> urls.py --> path('product/<str:slug/add_to_cart>', add_to_cart, name='add_to_cart'),
# store --> views.py -->
# def add_to_cart(request, slug):
#     user = request.user # Récupérer user
#     product = get_object_or_404(Product, slug=slug) # Récupérer produit s'il existe
#
#     # Récupérer le panier s'il existe et le créer s'il n'existe pas
#     cart, _ = Cart.objects.get_or_create(user=user)
#     # _ : pour dire qu'on n'utilise pas la seconde variable
#
#     # Récupérer l'ordre
#     order, created = Order.objects.get_or_create(user=user, product=product)
#     if created: # objet n'existait pas encore dans le panier
#         cart.orders.add(order)
#         cart.save()
#     else : # objet existait déjà dans le panier, on incrémente sa quantité
#         order.quantity += 1
#         order.save()
#     return redirect(reverse("product", kwargs={"slug":slug}))

# store --> detail.html -->
# {% if user.is_authenticated %}
        # <p><a href="{% url 'add-to-cart' product.slug %}">Ajouter au panier</a></p>
    # {% endif %}


# ----- 22 : AFFICHER LE PANIER -----
# urls.py --> path('cart/', cart, name='cart'),
# views.py -->
# def cart(request):
#     cart = get_object_or_404(Cart, user=request.user)
#     return render(request, 'store/cart.html', context={"orders":cart.orders.all()


# ----- 23 : AJOUTER UN LIEN VERS LE PANIER -----
# base.html -->
# {% if user.cart %}
# <a href="{% url 'cart' %}">Voir le panier ({{ user.cart.orders.count }})</a>
# {% endif %}


# ----- 23 : SUPPRIMER LE PANIER AU COMPLET -----
# urls.py --> path('cart/delete/', delete_cart, name='delete-cart'),

# views.py -->
# def delete_cart(request):
#     if cart:= request.user.cart: # SYNTHAXE !!
#         cart.orders.all().delete()
#         cart.delete()
#     return redirect('index')

# cart.html --> <a href="{% url 'delete-cart' %}">Vider le panier</a>


# ----- 24 : MODIFIER MODELE ORDER ET CART -----
# Comment modifier des modèles existants lorsqu'ils ont élé mal pensés ?
# Déplacer des champs du modele cart panier dans le modèle order
# python manage.py makemigrations
# python manage.py migrate
# On peut déplacer des champs dans les modèles tant qu'on fait les migrations derrière ensuite


# ----- 25 : MODIFIER SUPPRESSION DU PANIER -----
# Proposer un historique des articles commandés, même ceux supprimés
# Passer par le modèle et non plus par une vue
# models.py -->
#     def delete (self, *args, **kwargs):
#         for order in self.orders.all():
#             order.ordered = True
#             order.ordered_date = timezone.now()
#             order.save()
#
#         self.orders.clear()
#         super().delete(*args, **kwargs)


# ----- 26 : PACKAGE STRIPE POUR PAIEMENT -----











