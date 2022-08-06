from django.urls import path
from rest_framework import routers
from users.views import \
    UserListView, UserDetailView, UserCreateView, UserUpdateView, UserDeleteView, UserAdsView, \
    LocationView, LocationsViewSet

router = routers.SimpleRouter()
router.register('location_set', LocationsViewSet)


urlpatterns = [
    path('', UserListView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
    path('create/', UserCreateView.as_view()),
    path('<int:pk>/update/', UserUpdateView.as_view()),
    path('<int:pk>/delete/', UserDeleteView.as_view()),
    path('<int:pk>/image_up/', UserAdsView.as_view()),
    path('locations/', LocationView.as_view())
]

urlpatterns += router.urls
