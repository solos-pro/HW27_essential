from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView
from advertisement.models import Advertisement, Characteristics


class AdDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(200, {"status": "ok"})


class AdsView(View):
    def get(self, request):
        ads = Advertisement.objects.all()

        response = []
        for ad in ads:
            response.append(
                {
                    "id": ad.id,
                    "name": ad.name,
                    "author": ad.author,
                    "price": ad.price,
                    "description": ad.description,
                    "address": ad.address,
                    "is_published": ad.is_published,
                }
            )
        return JsonResponse(response, status=200, safe=False)


class CatDetailView(DetailView):
    model = Characteristics

    def get(self, request, *args, **kwargs):
        cat = self.get_object()
        return JsonResponse(
            {
                "id": cat.id,
                "name": cat.name,
            }, status=200, safe=False
        )


class CatView(View):
    def get(self, request):

        cats = Characteristics.objects.all()

        response = []
        for cat in cats:
            response.append(
                {
                    "id": cat.id,
                    "name": cat.name,
                }
            )
        return JsonResponse(response, status=200, safe=False)