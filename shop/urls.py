from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from store.views import index, product_detail, add_to_cart, cart, delete_item, plus_quantity, minus_quantity, \
    validate_cart, get_all_post, create_post, delete, get_post, update_post, index_api
from accounts.views import signup, logout_user, login_user, signin

from shop import settings

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('logout/', logout_user, name='logout'),
    path('login/', login_user, name='login'),
    path('cart/', cart, name='cart'),
    path('cart/validate/', validate_cart, name='validate_cart'),
    path('cart/delete/<int:pk>/', delete_item, name='delete_item'),
    path('product/<int:pk>', product_detail, name='product'),
    path('product/<int:pk>/add-to-cart/', add_to_cart, name='add-to-cart'),
    path('cart/plus_quantity/<int:pk>/', plus_quantity, name='plus_quantity'),
    path('cart/minus_quantity/<int:pk>/', minus_quantity, name='minus_quantity'),
    path('api/', index_api),
    path('api/get_all_post/', get_all_post),
    path('api/create_post/', create_post),
    path('api/delete/', delete),
    path('api/get_post/', get_post),
    path('api/update_post/', update_post),



    #  path('', include('api.urls'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
