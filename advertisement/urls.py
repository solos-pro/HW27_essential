from django.urls import path
from advertisement.views import AdsView, AdDetailView, AdCreateView, AdUpdateView, AdDeleteView

urlpatterns = [
    path('', AdsView.as_view()),
    path('<int:pk>/', AdsView.as_view()),
    path('<int:pk>/', AdDetailView.as_view()),
    path('create/', AdCreateView.as_view()),
    path('<int:pk>/', AdUpdateView.as_view()),
    path('<int:pk>/', AdDeleteView.as_view()),
]
