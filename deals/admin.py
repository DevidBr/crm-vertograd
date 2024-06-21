from django.contrib import admin
from deals.models import Deal, CommentForDeal, PriceRequest, PlantForPriceRequest, CommercialOffer, ContractRequest, \
    Contract


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'service', 'status']
    list_editable = ['status']
    list_display_links = ['id']
    pass


@admin.register(CommentForDeal)
class CommentForDealAdmin(admin.ModelAdmin):
    pass


@admin.register(PriceRequest)
class PriceRequestAdmin(admin.ModelAdmin):
    pass


@admin.register(PlantForPriceRequest)
class PlantForPriceRequestAdmin(admin.ModelAdmin):
    pass


@admin.register(CommercialOffer)
class CommercialOfferAdmin(admin.ModelAdmin):
    pass


@admin.register(ContractRequest)
class ContractRequestAdmin(admin.ModelAdmin):
    pass


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    pass