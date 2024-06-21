from django import forms
from django.forms import inlineformset_factory, formset_factory, modelformset_factory
from deals.models import Deal, CommentForDeal, PriceRequest, PlantForPriceRequest, CommercialOffer, ContractRequest, \
    Contract




class AddDealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ["service", "cost_price", "price",
                  "description", "organization", "manager",
                  "status"]

        widgets = {
            "service": forms.Select(attrs={
                "class": "form-select",
                "style": "width: 30%",
            }),
            "cost_price": forms.NumberInput(attrs={
                "class": "form-control",
                "style": "width: 30%"
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-control",
                "style": "width: 30%"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": 'Общее описание сделки. Например:\n'
                               '"Планирую продать озеленение интерьера с последующим'
                               ' сервисным уходом. Известно, что раньше услугу заказывали у'
                               ' дяди Лёши, но что-то не устроило..." и т.д.',
                "style": "width: 60%",
                "rows": 6
            }),
            "organization": forms.HiddenInput,
            "manager": forms.HiddenInput,
            "status": forms.HiddenInput
        }


class AddCommentForDealForm(forms.ModelForm):
    class Meta:
        model = CommentForDeal
        fields = ["deal", "text", "author"]
        widgets = {
            "deal": forms.HiddenInput,
            "author": forms.HiddenInput,
            "text": forms.Textarea(attrs={
                "class": "form-control",
                "style": "background-color: rgb(225 229 219) !important;"
            })
        }


# Формы для создания запроса стоимости для сделки.
class PlantForPriceRequestForm(forms.ModelForm):
    class Meta:
        model = PlantForPriceRequest
        fields = ['name', 'photo', 'quantity', 'height']

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Введите адрес объекта"
            }),
            "photo": forms.FileInput(attrs={
                "class": "form-control",
            }),
            "quantity": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Количество"
            }),
            "height": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Высота растения в см."
            }),
        }


        labels = {
            "photo": "Фото растения, если есть."
        }


PlantForPriceRequestFormset = formset_factory(
    form=PlantForPriceRequestForm,
    extra=1,
    can_delete=False
)


class PriceRequestForm(forms.ModelForm):
    class Meta:
        model = PriceRequest
        fields = ['address', 'comment_from_manager', 'deal']
        widgets = {
            "address": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Введите адрес объекта"
            }),
            "comment_from_manager": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Дополнительные комментарии к заявке, если они есть."
            }),
            "deal": forms.HiddenInput()
        }


class ConfirmRequestPriceForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ["cost_price", "price"]

        widgets = {
            "cost_price": forms.NumberInput(attrs={
                "class": "form-control",
                "required": "true"
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-control",
                "required": "true"
            }),
        }


class AddCommercialOfferForm(forms.ModelForm):
    class Meta:
        model = CommercialOffer
        fields = ["number", "date", "image", "counter_number", "creator"]
        widgets = {
            "number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "№ исх.",
                "readonly": "true"
            }),
            "date": forms.DateInput(attrs={
                "class": "form-control",
                "required": "true"
            }),
            "image": forms.FileInput(attrs={
                "class": "form-control",
                "required": "true"
            }),
            "counter_number": forms.HiddenInput(),
            "creator": forms.HiddenInput(),
        }


class ContractRequestForm(forms.ModelForm):
    class Meta:
        model = ContractRequest
        fields = ["deal", "creator", "description"]

        widgets = {
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Опишите, о чем договорились с клинтом на данный момент?\n"
                               "Порядок оплаты / сроки / какие-то еще пожелания..."
            }),
            "deal": forms.HiddenInput(),
            "creator": forms.HiddenInput()
        }


class ContractCreateForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ["deal", "contract_number", "contract_date", "contract_text"]

        widgets = {
            "deal": forms.HiddenInput(),
            "contract_number": forms.TextInput(attrs={
                "class": "form-control",
                "required": True
            }),
            "contract_date": forms.DateInput(attrs={
                "class": "form-control",
                "required": True,
                "placeholder": "Нажми для выбора даты",
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "left"
            }),
            "contract_text": forms.FileInput(attrs={
                "class": "form-control",
                "required": True,
            }),
        }

        labels = {
            "contract_text": "Файл с текстом договора (DOC, DOCX и т.д.)"
        }
