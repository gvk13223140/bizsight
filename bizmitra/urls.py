from django.urls import path
from bizmitra.views import (
    companion_home,
    dashboard_view,
    guided_chat_view,
    alerts_view,
)

app_name = "bizmitra"


urlpatterns = [
    path("", companion_home, name="home"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("chat/", guided_chat_view, name="chat"),
    path("alerts/", alerts_view, name="alerts"),
]