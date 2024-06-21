from django.urls import path
from deals.views import deals_list, add_deal, deal_detail, deal_change_service, RequestPrice, PriceRequestDetailView, \
    commercial_offer_save, commercial_offer_has_been_sent_to_the_client, ContractRequestView, PriceRequestListView, \
    ContractRequestsListView, ContractRequestDetailAndCreateContractView

app_name = "deals"

urlpatterns = [
    path("list/", deals_list, name="deals_list"),
    path("add/<int:client_id>", add_deal, name="add_deal"),
    path("detail/<int:deal_id>", deal_detail, name="deal_detail"),
    path("change_deal/<int:deal_id>", deal_change_service, name="deal_change_service"),
    # path("change_deal/request_price/add_plant", add_plant_form, name="add_plant_form"),
    path("change_deal/<int:deal_pk>/request_price/", RequestPrice.as_view(), name="request_price"),
    path("price_requests/<int:price_request_pk>/", PriceRequestDetailView.as_view(), name="price_request_detail"),
    path("deal_save_commercial_offer/<int:deal_id>/", commercial_offer_save, name="commercial_offer_save"),
    path("commercial_offer_has_been_sent_to_the_client/<int:deal_id>/", commercial_offer_has_been_sent_to_the_client,
         name="commercial_offer_has_been_sent_to_the_client"),
    path("detail/<int:deal_id>/contract_request", ContractRequestView.as_view(), name="contract_request"),
    path("price_request_list/", PriceRequestListView.as_view(), name="price_request_list"),
    path("contract_request_list/", ContractRequestsListView.as_view(), name="contract_request_list"),
    path("contract_request_detail/<int:contract_request_pk>/", ContractRequestDetailAndCreateContractView.as_view(),
         name="contract_request_detail")
]
