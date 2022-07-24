import json

from django.core.paginator import Paginator
from django.db.models import Count, Avg
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView

from djangoProject import settings
from users.models import User


@method_decorator(csrf_exempt, name='dispatch')
class UserView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by("username")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        advertisements = []

        for user in page_obj:
            advertisements.append(
                {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "role": list(map(str, user.groups.all())),
                    "age": list(User.objects.all().filter(user=user.id).values_list("age", flat=True)),
                    "location": list(User.objects.all().filter(user=user.id).values_list("location_name", flat=True)),
                }
            )

        response = {
            "items": advertisements,
            "num_pages": paginator.num_pages,
            "total": paginator.count,
        }
        return JsonResponse(response, status=200, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return JsonResponse(
            {
                "id": user.id,
                "name": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": list(map(str, user.groups.all())),
                "age": list(User.objects.all().filter(user=user.id).values_list("age", flat=True)),
                "location": list(User.objects.all().filter(user=user.id).values_list("location_name", flat=True)),
            }, status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ["username", "first_name", "last_name"]

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        user = User.objects.create(
            username=user_data["username"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
        )

        return JsonResponse(
            {
                "id": user.id,
                "name": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": list(map(str, user.groups.all())),
                "age": list(User.objects.all().filter(user=user.id).values_list("age", flat=True)),
                "location": list(User.objects.all().filter(user=user.id).values_list("location_name", flat=True)),
            }, status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ["username", "first_name", "last_name"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)

        user = self.object
        user.username = user_data["username"]
        user.first_name = user_data["first_name"]
        user.last_name = user_data["last_name"]

        user.save()

        return JsonResponse(
            {
                "id": user.id,
                "name": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": list(map(str, user.groups.all())),
                "age": list(User.objects.all().filter(user=user.id).values_list("age", flat=True)),
                "location": list(User.objects.all().filter(user=user.id).values_list("location_name", flat=True)),
            }, status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = "delete/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "OK"}, status=200)


class UserAdsView(View):
    def get(self, request):
        user_qs = User.objects.annotate(ads=Count('advertisement'))

        paginator = Paginator(user_qs, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        users = []

        for user in page_obj:
            users.append(
                {
                    "id": user.id,
                    "name": user.username,
                    "total_ads": user.ads,
                }
            )

        response = {
            "items": users,
            "num_pages": paginator.num_pages,
            "total": paginator.count,
            "avg": user_qs.aggregate(avg=Avg("ads"))["avg"],
        }

        return JsonResponse(response, safe=False)

