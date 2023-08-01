# ------ FORMATION BOOTSTRAP ------

# Utilité : Pour le frontend, permet d'associer HTML et CSS pour une mise en page plus facile sur pycharm.

# ------ 1 :  CREATION FICHIER HTML ------
# --> Include the <meta name="viewport"> tag as well for proper responsive behaviour in mobile devices.

# ------ 2 : AJOUTER CSS ET JS DE BOOTSTRAP ------
# --> <head> : <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
# --> <body> : <script>src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz" crossorigin="anonymous"></script>

# DECLARER DES STYLES CSS EN HTML
# ---> On peut écrire le style css directement dans le fichier html en insérant la balise <style></style> dans le <head>
# ---> On peut également préciser un style particulier en déclarant un élément en html
# Exemple : <h2 class="texte3" style = "margin-top: 40px">{{order.product.name}}</h2>

# ------ 3 : UTILISER UN TEMPLATE DE BOOSTRAP ------
# 1 : Importer le code css et le code html
# 2 : html --> faire la bonne référene au fichier css avec {% load static %}
# 3 : html --> ajouter le link dans le head et le script dans le body