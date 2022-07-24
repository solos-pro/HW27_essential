import pandas as pandas
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from advertisement.models import Advertisement, Category
import json
import os

from djangoProject import settings

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
class AdsView(ListView):
    model = Advertisement

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by("price")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        advertisements = []
        for ad in page_obj:
            advertisements.append(
                {
                    "id": ad.id,
                    "name": ad.name,
                    "author": ad.author_id,
                }
            )

        response = {
            "items": advertisements,
            "num_pages": paginator.num_pages,
            "total": paginator.count,
        }
        return JsonResponse(response, status=200, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class AdDetailView(DetailView):
    model = Advertisement

    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        return JsonResponse(
            {
                "id": ad.id,
                "name": ad.name,
                "author": ad.author_id,
                "price": ad.price,
                "description": ad.description,
                "category": ad.category_id,
                "image": ad.image.url if ad.image else None,
                "is_published": ad.is_published,
            }, status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdsCreateView(CreateView):
    model = Advertisement
    fields = ["name", "author_id", "price", "description", "category_id", "image", "is_published"]

    def post(self, request, *args, **kwargs):
        ads_data = json.loads(request.body)

        ads = Advertisement.objects.create(
            name=ads_data["name"],
            author_id=ads_data["author_id"],
            price=ads_data["price"],
            description=ads_data["description"],
            is_published=ads_data["is_published"],
            # image=request.FILES["image"],
            image=ads_data["image"],
            category_id=ads_data["category_id"],
        )

        ads.author = get_object_or_404(User, pk=ads_data["author_id"])

        return JsonResponse(
            {
                "id": ads.id,
                "name": ads.name,
                "author": ads.author_id,
                "price": ads.price,
                "description": ads.description,
                "category": ads.category_id,
                "image": ads.image.url if ads.image else None,
                "is_published": ads.is_published,
            }
        )


# --------------------------------------------------------------------------------------
@method_decorator(csrf_exempt, name='dispatch')
class CatListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by("name")

        response = []
        for cat in self.object_list:
            response.append(
                {
                    "id": cat.id,
                    "name": cat.name,
                }
            )
        return JsonResponse(response, status=200, safe=False)


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
class CatCreateView(CreateView):
    model = Category
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        cat_data = json.loads(request.body)

        cat = Category.objects.create(name=cat_data["name"])

        return JsonResponse(
            {
                "id": cat.id,
                "name": cat.name,
            }, status=200, safe=False
        )


@method_decorator(csrf_exempt, name='dispatch')
class CatUpdateView(UpdateView):
    model = Category
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        cat_data = json.loads(request, *args, **kwargs)

        cat = self.object
        cat.name = cat_data["name"]
        cat.save()

        return JsonResponse(
            {
                "id": cat.id,
                "name": cat.name,
            }, status=200, safe=False
        )


@method_decorator(csrf_exempt, name='dispatch')
class CatDeleteView(DeleteView):
    model = Category
    success_url = "delete/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "OK"}, status=200)