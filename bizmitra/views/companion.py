# bizmitra/views/companion.py

from django.shortcuts import render
from accounts.utils import get_current_business

def companion_view(request):
    business = get_current_business(request)
    if not business:
        return render(request, "bizmitra/companion.html")

    return render(
        request,
        "bizmitra/companion.html",
        {
            "business": business,
        }
    )
