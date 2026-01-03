from .models import Business
def get_current_business(request):
    business_id = request.session.get("business_id")
    if business_id:
        try:
            return Business.objects.get(id=business_id)
        except Business.DoesNotExist:
            request.session.pop("business_id", None)


    if request.user.is_authenticated and hasattr(request.user, "business"):
        business = request.user.business
        request.session["business_id"] = business.id
        return business

    return None