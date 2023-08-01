from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate

# Récupérer la classe utilisateur
User = get_user_model()
def signup(request):
    if request.method == "POST":
        # Traiter le formulaire
        username = request.POST.get("username") # Récupérer les clés du dictionnaire = "name" dans input
        password = request.POST.get("password")
        user = User.objects.create_user(username=username, password=password) # Créer l'utilisateur
        login(request, user) # Connecter l'utilisateur au site
        return redirect('index') # rediriger vers la vue d'acceuil

    return render(request, 'accounts/signup.html')


def login_user(request):
    if request.method == 'POST':
        # Connecter l'user
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password) # Vérifier que les infos données sont les bonnes et bien dans la bdd

        if user: # Connecter l'user et rediriger vers la page d'acceuil
            login(request, user)
            return redirect('index')

    return render (request, 'accounts/login.html')

def logout_user(request):
    logout(request)
    return redirect('index')

def signin (request):
    return render(request, 'accounts/se_connecter.html')