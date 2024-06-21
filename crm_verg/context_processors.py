from deals.forms import AddDealForm, PriceRequestForm, PlantForPriceRequestFormset
from deals.models import PriceRequest, ContractRequest


def get_change_add_deal_form(request):
    context = {"change_add_deal_form": AddDealForm}
    return context


# TODO: Убрать этот процессор
def get_add_price_request_forms(request):
    context = {
        # "price_request_form": PriceRequestForm,
        # "plants_formset": PlantForPriceRequestFormset
    }
    return context


def price_request_counter(request):
    context = {"price_request_counter": PriceRequest.objects.filter(status="1").count()}
    return context


def contract_request_counter(request):
    context = {"contract_request_counter": ContractRequest.objects.filter(status="1").count()}
    return context