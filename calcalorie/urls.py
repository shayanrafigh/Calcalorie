from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from food_calorie import views

router= DefaultRouter()
#router.register(r'food/detail', views.FoodDetailView, basename="food-detail")
router.register(r'cards', views.CardView, basename="card")
router.register(r'nutrients', views.NutrientView, basename="nutrient")
router.register(r'foods', views.FoodDetailView, basename="food")
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/schema/',SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/docs/',SpectacularSwaggerView.as_view(url_name='schema')),
    path("__debug__/", include("debug_toolbar.urls")),
    
]
