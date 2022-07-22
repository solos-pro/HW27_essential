import pandas as pandas
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from advertisement.models import Advertisement, Category
import json
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FILE1: str = os.path.join(BASE_DIR, 'ads.csv')
FILE2: str = os.path.join(BASE_DIR, 'categories.csv')


@method_decorator(csrf_exempt, name='dispatch')
class InitDB(View):
    def get(self, request):

        data_ads = pandas.read_csv(FILE1, sep=",").to_dict()
        i = 0

        while max(data_ads['Id'].keys()) >= i:
            Advertisement.objects.create(
                name=data_ads["name"][i],
                author=data_ads["author"][i],
                price=data_ads["price"][i],
                description=data_ads["description"][i],
                address=data_ads["address"][i],
                is_published=data_ads["is_published"][i],
                image=data_ads["image"][i],
            )
            i += 1

        data_categories = pandas.read_csv(FILE2, sep=",").to_dict()
        i = 0

        while max(data_categories['id'].keys()) >= i:
            Category.objects.create(
                name=data_categories["name"][i],
            )
            i += 1

        return JsonResponse("data from ads.csv & categories.csv is added", safe=False, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(200, {"status": "ok"})


@method_decorator(csrf_exempt, name='dispatch')
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
                    "image": ad.image.url if ad.image else None
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


@method_decorator(csrf_exempt, name="dispatch")
class AdDetailView(DetailView):
    model = Advertisement

    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        return JsonResponse(
            {
                "id": ad.id,
                "name": ad.name,
                "author": ad.author,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published,
            }, status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
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


@method_decorator(csrf_exempt, name='dispatch')
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