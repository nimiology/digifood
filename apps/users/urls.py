from django.urls import path

from apps.users.views import UserSearch, GetUser

app_name = 'users'
urlpatterns = [
    path('', UserSearch.as_view(), name='search'),
    path('<username>/', GetUser.as_view(), name='get'),

]