from .models import Business

def get_current_business(request):
    business_id = request.session.get("business_id")
    if not business_id:
        return None
    return Business.objects.filter(id=business_id).first()
