import pandas as pandas
from users.models import User, Location
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
FILE1: str = os.path.join(BASE_DIR, 'new_location.csv')
FILE2: str = os.path.join(BASE_DIR, 'new_categories.csv')
FILE3: str = os.path.join(BASE_DIR, 'new_user.csv')
FILE4: str = os.path.join(BASE_DIR, 'new_ads.csv')


@method_decorator(csrf_exempt, name='dispatch')
class InitLocations(View):
    def get(self, request):

        data_location = pandas.read_csv(FILE1, sep=",").to_dict()
        i = 0

        while max(data_location['id'].keys()) >= i:
            Location.objects.update_or_create(
                name=data_location["name"][i],
                lat=data_location["lat"][i],
                lng=data_location["lng"][i],
            )
            i += 1

        return JsonResponse("data_location is added", safe=False, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class InitCategories(View):
    def get(self, request):

        data_categories = pandas.read_csv(FILE2, sep=",").to_dict()
        i = 0

        while max(data_categories['id'].keys()) >= i:
            Category.objects.update_or_create(
                name=data_categories["name"][i],
            )
            i += 1

        return JsonResponse("data_categories is added", safe=False, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class InitUsers(View):
    def get(self, request):

        data_user = pandas.read_csv(FILE3, sep=",").to_dict()
        i = 0

        while max(data_user['id'].keys()) >= i:
            User.objects.update_or_create(
                first_name=data_user["first_name"][i],
                last_name=data_user["last_name"][i],
                username=data_user["username"][i],
                password=data_user["password"][i],
                role=data_user["role"][i],
                age=data_user["age"][i],
                locations_id=data_user["location_id"][i],
            )
            i += 1

        return JsonResponse("data_user is added", safe=False, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class InitAdvertisement(View):
    def get(self, request):

        data_ads = pandas.read_csv(FILE4, sep=",").to_dict()
        i = 0

        while max(data_ads['Id'].keys()) >= i:
            Advertisement.objects.update_or_create(
                name=data_ads["name"][i],
                author_id=data_ads["author_id"][i],
                price=data_ads["price"][i],
                description=data_ads["description"][i],
                is_published=data_ads["is_published"][i],
                image=data_ads["image"][i],
                category_id=data_ads["category_id"][i],
            )
            i += 1

        return JsonResponse("data_ads is added", safe=False, status=200)


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
                    "author_id": ad.author_id,
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
                "author_id": ad.author_id,
                "author": list(User.objects.all().filter(id=ad.author_id).values_list("first_name", flat=True)),
                "price": ad.price,
                "description": ad.description,
                "category_id": ad.category_id,
                "category": list(Category.objects.all().filter(id=ad.category_id).values_list("name", flat=True)),
                "image": ad.image.url if ad.image else None,
                "is_published": ad.is_published,
            }, status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Advertisement
    fields = ["name", "author_id", "price", "description", "category_id", "image", "is_published"]

    def post(self, request, *args, **kwargs):
        ads_data = json.loads(request.body)

        author_id = get_object_or_404(User, pk=ads_data["author_id"])
        category = get_object_or_404(Category, pk=ads_data["category_id"])

        ads = Advertisement.objects.create(
            name=ads_data["name"],
            author_id=ads_data["author_id"],
            price=ads_data["price"],
            description=ads_data["description"],
            is_published=ads_data["is_published"],
            image=ads_data["image"],
            category_id=ads_data["category_id"],
        )


        return JsonResponse(
            {
                "id": ads.id,
                "name": ads.name,
                "author_id": ads.author_id,
                "price": ads.price,
                "description": ads.description,
                "category": ads.category_id,
                "image": ads.image.url if ads.image else None,
                "is_published": ads.is_published,
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Advertisement
    fields = ["name", "author", "price", "description", "category", "image", "is_published"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ads_data = json.loads(request.body)

        ads = self.object
        ads.name = ads_data["name"]
        ads.author_id = int(ads_data["author_id"])
        ads.price = ads_data["price"]
        ads.description = ads_data["description"]
        ads.is_published = ads_data["is_published"]
        ads.image = ads_data["image"]
        ads.category_id = int(ads_data["category_id"])
        ads.save()

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


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Advertisement
    success_url = "delete/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "deleted"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class ImageUpdateView(UpdateView):
    model = Advertisement
    fields = ["image"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES("image")
        self.object.save()

        return JsonResponse({
            "id":  self.object.id,
            "name":  self.object.name,
            "author_id":  self.object.author_id,
            "author":  list(map(str, self.object.author_id.all())),
            "price":  self.object.price,
            "description":  self.object.description,
            "is_published":  self.object.is_published,
            "category_id":  self.object.category,
            "image": self.object.image.url if self.object.image else None,
        }, status=200, safe=False)


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
        cat_data = json.loads(request.body)

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
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "deleted"}, status=200)