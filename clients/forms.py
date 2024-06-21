from django import forms
from django.forms import inlineformset_factory

from clients.models import Client, ContactPerson


class ContactPersonForm(forms.ModelForm):
    class Meta:
        model = ContactPerson
        fields = ["name", "job_title", "telephone",
                  "whatsapp", "telegram", "email", "organization"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "ФИО",
                "style": "width: 50%"}),
            "job_title": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "должность",
                "style": "width: 50%"}),
            "telephone": forms.TextInput(attrs={
                "class": "",
                "placeholder": "номер телефона",
                "style": "width: 50%; height: 40px; border: none"}),
            "whatsapp": forms.TextInput(attrs={
                "class": "",
                "placeholder": "whatsapp",
                "style": "width: 50%; height: 40px; border: none"}),
            "telegram": forms.TextInput(attrs={
                "class": "",
                "placeholder": "telegram",
                "style": "width: 50%; height: 40px; border: none"}),
            "email": forms.EmailInput(attrs={
                "class": "",
                "placeholder": "email",
                "style": "width: 50%; height: 40px; border: none"}),
            "organization": forms.HiddenInput()
        }


ContactPersonFormset = inlineformset_factory(
    parent_model=Client,
    model=ContactPerson,
    form=ContactPersonForm,
    extra=1,
    can_delete=False)


class AddClientManagerForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["type", "type_of_activity", "name",
                  "inn", "city", "address",
                  "telephone", "email"]
        labels = {
            "type": "Тип клиента (организация/ИП/самозанятый/частное лицо)",
            "type_of_activity": "Описание компании",
            "name": "Наименование клиента",
        }
        widgets = {
            'type': forms.Select(attrs=
                                 {'class': 'form-select',
                                  "style": "width: 30%"}),
            'type_of_activity': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                "placeholder": "Краткое описание клиента.\n"
                               "Например: 'Ресторан на юге Москвы' "
                               "или 'Частный дом с садом' и т.д.",
                "style": "width: 80%"}),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                "placeholder": "Название организации или ФИО, если это просто частное лицо.",
                "style": "width: 80%"}),
            'inn': forms.TextInput(attrs={
                'class': 'form-control',
                "placeholder": "ИНН Компании.",
                "style": "width: 30%"}),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                "placeholder": "Город, в котором находится клиент.",
                "style": "width: 50%"}),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                "placeholder": "Улица, дом, где находится клиент.",
                "style": "width: 50%"}),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                "placeholder": "Основной телефон организации. Если это частное лицо, то его телефон.",
                "style": "width: 50%"}),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email организации. Если это частное лицо, то его email.',
                "style": "width: 50%"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.contact_person_formset = ContactPersonFormset(instance=self.instance)

    def save(self, commit=True):
        instance = super().save(commit=commit)
        self.contact_person_formset.save()
        return instance
