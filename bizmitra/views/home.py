from django.shortcuts import render
from accounts.utils import get_current_business

def companion_home(request):
    business = get_current_business(request)
    return render(
        request,
        "bizmitra/home.html",
        {"business": business}
    )
