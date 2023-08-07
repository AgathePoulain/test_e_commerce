"""
            BUILD AN API WITH DJANGO REST FRAMEWORK

0 - INTRODUCTION -
Application Programming Interface : defines how different software systems should interact
with each other by specifying the types of requests and responses that can be made as well as
the format of data being transferred

Web development context : API used to expose data and functionality from a web application
to other systems (mobile apps, other websites, IOT devices)

Example du restaurant : le client passe commande à la cuisine en passant par le serveur, qui
traite la demande pur une solution appropriée

API is capable of accepting and collecting different requests, and based of those requests,
it returns different and appropriate responses


1 - PROJECT SETUP -
Dans terminal :
mkdir dossier
cd dossier
pip install django
pip install djangorestframework
django-admin startproject shop
cd shop
python manage.py startapp store
python manage.py startapp api
--> shop --> settings.py --> ajouter 'api' et 'rest_framework' à installed app
         --> urls.py --> from django.urls import path, include --> path('', include('api.urls'))
--> api --> créer urls.py


2 - CREATING FIRST ENDPOINT -
API endpoint : API are capable of receiving different types of requests, and those requests depend on what endpoints are available
Different requests can be made thanks to different endpoints

api --> views.py -->
from rest_framework.decorators import api_view
from rest_framework.response import Response

--> when you create a view, you must specify wether it is for a post or a get request
@api_view(['GET'])
def index(request):
    return Response({"Success":"The setup was successful"})

    --> urls.py -->
path('api/', index)


3 - INSTALLING POSTMAN -


4 - TEST API WITH REQUEST -
terminal --> pip install requests (installer la bibliothèque pour faire des requêtes dans notre environnement)
api --> test.py -->
import requests
request = requests.get('http://127.0.0.1:8000/api/')
print(request.json())

--> run tests --> return '{'Success': 'The setup was successful'}
It is one way of interacting with our API, we have to write a code to make request to each endpoint that we create


5 - TEST API POSTMAN -
--> From now on, we are only going to use postman to test our API


6 - CREATING MODELS -
We need to be able to store data inside our database
--> api --> models.py [Créer le modèle Post]

class Post(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    description = models.TextField(blank=True)  # Pouvoir ajouter la description plus tard

    def __str__(self):
        return self.name


7 - REGISTER MODELS IN ADMIN -
--> admin.py --> admin.site.register(models.Post) [Enregister le modèle]

8 - CREATING SUPERUSER -
--> Terminal -->
python manage.py createsuperuser
python manage.py makemigrations
python manage.py migrate


9 - CREATING POSTS FROM ADMIN -


10 - GET ALL POST FROM ADMIN -
--> views.py -->
from api.models import Post
@api_view(['GET'])
def get_all_post(request):
    get_posts = Post.objects.all()
    return Response(get_posts) --> l'objet get_posts est trop complexe pour que Response puisse le renvoyer
    Il faut que les data injectées dans Response soient serializées


11 - CREATING SERIALIZERS -
Serializers serve as a middleman between the actual query sets and the response class
They take in the query set and converts it into a data type or format that the response class can handle

--> api --> serializers.py
class PostSerializer(ModelSerializer):
    class Meta:
        model = Post  # Specify the model we try to serialize
        fields = '__all__'  # Specify the fields from this model which will be included in the process : here we want
        # to work with all the fields of the Post model

--> views.py
@api_view(['GET'])
def get_all_post(request):
    get_posts = Post.objects.all()  # This endpoint goes and gets all the posts in database
    serializer = PostSerializer(get_posts)  # The data is converted to the correct format
    return Response(serializer.data)  # The suitable data is used by the response class

--> Problem : Got AttributeError when attempting to get a value for field `name` on serializer `PostSerializer`.
The serializer field might be named incorrectly and not match any attribute or key on the `QuerySet` instance.
Original exception text was: 'QuerySet' object has no attribute 'name'.

--> Solution --> views.py
serializer = PostSerializer(get_posts, many=True)
To tell django that what we are trying to pass in a query set is a list of objects
and not just one item


12 - POST CREATE API ENDPOINT -
How to create a post from the user interface and not from django admin interface ?
--> Need to create another endpoint

--> api --> views.py
@api_view(['GET', 'POST'])
def create_post(request):
    data = request.data
    serializer = PostSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Success": "The post was successfully created"}, status=201)
    else:
        return Response(serializer.errors, status=400)


13 - DELETE POST API ENDPOINT -
def delete(request):
    post_id = request.data.get('post_id')
    try:
        post = Post.objects.get(id=post_id)
        post.delete()
        return Response({"Success": "The post was successfully deleted"}, status=200)
    except Post.DoesNotExist:
        return Response({"Error": "The post does not exist"}, status=404)


14 - GET POST API ENDPOINT -
@api_view(['GET'])
def get_post(request):
    post_id = request.data.get('post_id')
    try:
        post = Post.objects.get(id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    except Post.DoesNotExist:
        return Response({"Error": "The post does not exist"}, status=404)


15 - UPDATE POST API ENDPOINT -
@api_view(['PUT'])
def update_post(request):
    post_id = request.data.get('post_id')
    get_new_name = request.data.get('new_name')
    get_new_price = request.data.get('new_price')
    get_new_stock = request.data.get('new_stock')
    get_new_description = request.data.get('new_description')
    try:
        post = Post.objects.get(id=post_id)
        if get_new_name:
            post.title = get_new_name
        if get_new_price:
            post.price = get_new_price
        if get_new_stock:
            post.stock = get_new_stock
        if get_new_description:
            post.description = get_new_description
        post.save()
        return Response({"Success": "The post was successfully updated"}, status=200)
    except Post.DoesNotExist:
        return Response({"Error": "The post does not exist"}, status=404)


16 - VIEWSET ET ROUTEURS --
Video : https://www.youtube.com/watch?v=AbonUu2QbLA&list=PLJuTqSmOxhNuN1iyCCx3pvkImo7JZpHHc&index=23

Viewset : un ensemble de vue qui fait toutes les autres vues en une

--> Créer viewset.py dans store
from store.models import Product
from store.serializers import ProductSerializer
from rest_framework import viewsets


class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


-->  Créer routeurs.py dans shop
from rest_framework.routers import DefaultRouter
from store.viewset import ProductViewset

router = DefaultRouter()
router.register('viewset', ProductViewset, basename='product-a')

'viewset' : C'est le préfixe URL qui sera utilisé pour les URL générées.
Par exemple, les URL pour récupérer une liste de produits, créer un produit, mettre à jour un produit, etc., auront ce préfixe suivi
par des segments spécifiques pour chaque opération.

ProductViewset: C'est la classe de vue qui gérera les opérations sur les produits. Elle doit être une sous-classe de viewsets.ModelViewSet
de Django REST framework. Cette classe ViewSet détermine comment les opérations CRUD sont gérées et quel sérialiseur est utilisé pour la conversion
entre les objets Python et les données JSON.

basename='product-a': Cela définit le nom de base pour la vue. Il est utilisé pour identifier cette vue dans les URL générées.
Par exemple, lors de la génération d'une URL pour la récupération d'un produit spécifique, le nom de base est combiné avec l'identifiant
du produit pour former une URL comme /viewset/1/.


urlpatterns = router.urls













"""