from rest_framework.routers import DefaultRouter
from store.viewset import ProductViewset

router = DefaultRouter()
router.register('viewset', ProductViewset,  basename='product-a')

print(router.urls)
urlpatterns = router.urls
