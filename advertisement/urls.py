from django.urls import path
from advertisement.views import \
    InitLocations, InitCategories, InitUsers, InitAdvertisement, \
    AdsView, AdDetailView, AdCreateView, AdUpdateView, AdDeleteView,\
    CatListView, CatDetailView, CatCreateView, CatUpdateView, CatDeleteView

urlpatterns = [
    path('init/location/', InitLocations.as_view()),
    path('init/categories/', InitCategories.as_view()),
    path('init/users/', InitUsers.as_view()),
    path('init/ads/', InitAdvertisement.as_view()),

    path('ad/', AdsView.as_view()),
    path('ad/<int:pk>/', AdsView.as_view()),
    path('ad/<int:pk>/', AdDetailView.as_view()),
    path('ad/create/', AdCreateView.as_view()),
    path('ad/<int:pk>/update/', AdUpdateView.as_view()),
    path('ad/<int:pk>/delete/', AdDeleteView.as_view()),

    path('cat/', CatListView.as_view()),
    path('cat/<int:pk>/', CatDetailView.as_view()),
    path('cat/create/', CatCreateView.as_view()),
    path('cat/<int:pk>/update/', CatUpdateView.as_view()),
    path('cat/<int:pk>/delete/', CatDeleteView.as_view()),
]
