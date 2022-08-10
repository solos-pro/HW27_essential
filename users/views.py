import json

from django.core.paginator import Paginator
from django.db.models import Count, Avg
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from djangoProject import settings
from advertisement.models import Advertisement
from users.models import User, Location
from users.serializers import LocationsSerializer, UsersSerializer, UserSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, RetrieveAPIView


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer

# @method_decorator(csrf_exempt, name='dispatch')
# class UserListView(ListView):
#     model = User
#
#     def get(self, request, *args, **kwargs):
#         super().get(request, *args, **kwargs)
#
#         # self.object_list = self.object_list.order_by("username")
#         self.object_list = self.object_list.annotate(ads_count=Count('username')).order_by("username")
#
#         paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
#         page_number = request.GET.get("page")
#         page_obj = paginator.get_page(page_number)
#
#         advertisements = []
#
#         for user in page_obj:
#             advertisements.append(
#                 {
#                     "id": user.id,
#                     "first_name": user.first_name,
#                     "last_name": user.last_name,
#                     "username": user.username,
#                     "age": user.age,
#                     "role": user.role,
#                     "location": list(Location.objects.all().filter(user=user.id).values_list("name", flat=True)),
#                     "ads_count": user.ads_count,
#                 }
#             )
#
#         response = {
#             "items": advertisements,
#             "num_pages": paginator.num_pages,
#             "total": paginator.count,
#         }
#         return JsonResponse(response, status=200, safe=False)


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
	# lookup_field = 'slug_field'

# @method_decorator(csrf_exempt, name="dispatch")
# class UserDetailView(DetailView):
#     model = User
#
#     def get(self, request, *args, **kwargs):
#         user = self.get_object()
#         return JsonResponse(
#             {
#                 "id": user.id,
#                 "name": user.username,
#                 "first_name": user.first_name,
#                 "last_name": user.last_name,
#                 "age": user.age,
#                 "role": user.role,
#                 # "location": list(User.objects.all().filter(user=user.id).values_list("location_name", flat=True)),
#             }, status=200, safe=False)


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
                "age": user.age,
                "role": user.role,
                # "location": list(User.objects.all().filter(user=user.id).values_list("location_name", flat=True)),
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
                "age": user.age,
                "role": user.role,
                # "location": list(User.objects.all().filter(user=user.id).values_list("location_name", flat=True)),
            }, status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "deleted"}, status=200)


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

# ---------------------------------------------------------------------------------


@method_decorator(csrf_exempt, name='dispatch')
class LocationView(ListView):
    model = Location

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        # self.object_list = self.object_list.annotate(ads_count=Count('username')).order_by("username")
        self.object_list = self.object_list.all()

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        list(map(lambda x: setattr(x, "name", x.name), page_obj))

        response = {
            "items": LocationsSerializer(page_obj, many=True).data,
            "num_pages": paginator.num_pages,
            "total": paginator.count,
        }
        return JsonResponse(response, status=200, safe=False)


class LocationsViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationsSerializer

