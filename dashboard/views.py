from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count
from clients.models import Client
from deals.models import Deal, PriceRequest


@login_required(login_url="login:main")
def home_dashboard(request):
    if request.user.is_staff:
        return render(request,
                      template_name="dashboard/home_dashboard.html")
    else:
        deals_count = 0
        for client in Client.objects.filter(manager__id=request.user.id):
            deals_count += client.active_deals_counter()
        print(deals_count)
        return render(request, "dashboard/home_dashboard.html", {"deals__count": deals_count})


@login_required(login_url="login:main")
def access_denied(request):
    return render(request, "dashboard/access_denied.html")
