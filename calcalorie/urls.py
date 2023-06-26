from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from food_calorie import views

router= DefaultRouter()
router.register(r'food', views.FoodView, basename="food")
router.register(r'food/detail', views.FoodDetailView, basename="food-detail")
router.register(r'vitamin', views.VitaminView, basename="vitamin")
router.register(r'mineral', views.MineralView, basename="mineral")
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/schema/',SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/docs/',SpectacularSwaggerView.as_view(url_name='schema')),
    
]
