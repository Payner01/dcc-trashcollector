from django.urls import path


from . import views

# TODO: Determine what distinct pages are required for the user stories, add a path for each in urlpatterns

app_name = "employees"
urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.create, name="create"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('confirm_pickup/<int:item_id>/', views.confirm_pickup, name="confirm_pickup"),
    path('search_daily_pickups/<str:weekday>/', views.search_daily_pickups, name="search_daily_pickups")

]