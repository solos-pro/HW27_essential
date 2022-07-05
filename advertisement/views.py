from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView
from advertisement.models import Advertisement, Category
import json


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

    def post(self, request):
        ad_data = json.loads(request.body)

        ad = Advertisement.objects.create(
            name = ad_data["name"],
            author = ad_data["author"],
            price = ad_data["price"],
            description = ad_data["description"],
            address = ad_data["address"],
            is_published = ad_data["is_published"],
        )


        return JsonResponse(
            {
                "id": ad.pk,
                "name": ad.name,
                "author": ad.author,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published,
            }
        )


class CatDetailView(DetailView):
    model = Category

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

        cats = Category.objects.all()

        response = []
        for cat in cats:
            response.append(
                {
                    "id": cat.id,
                    "name": cat.name,
                }
            )
        return JsonResponse(response, status=200, safe=False)

    def post(self, request):
        category_data = json.loads(request.body)

        category = Category.objects.create(
            name=category_data["name"],
        )

        return JsonResponse(
            {
                "id": category.id,
                "name": category.name,
            }, status=200, safe=False
        )