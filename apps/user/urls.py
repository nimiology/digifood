from django.urls import path

from apps.user.views import UserSearch, GetUser

app_name = 'user'
urlpatterns = [
    path('', UserSearch.as_view(), name='search'),
    path('<username>/', GetUser.as_view(), name='get'),

]