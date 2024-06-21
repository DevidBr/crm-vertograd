from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from clients.models import Client, ContactPerson
from clients.forms import AddClientManagerForm, ContactPersonFormset, ContactPersonForm


@login_required(login_url="login:main")
def clients_main(request):
    """
    Возвращает список всех клиентов, у которых manager.id == id пользователя, отправляющего запрос.
    В случае, если пользователь является staff, возвращает список всех клиентов.
    """
    if not request.user.is_staff:
        clients = Client.objects.filter(manager__id=request.user.id)
    else:
        clients = Client.objects.all()
    return render(request, "clients/clients_list.html", {"clients": clients})


@login_required(login_url="login:main")
def add_client(request):
    """
    При методе GET:
    Возвращает форму добавления объекта Client и одного, привязанного к нему ContactPerson
    При методе POST:
    Проверяет валидность формы и сохраняет объект Client и, ссылающийся на него объект ContactPerson,
    так же в поле "manager" сохраняется объект request.user (тот пользователь, который и сохраняет Client объект)
    """
    if request.method == 'POST':
        form = AddClientManagerForm(request.POST, prefix='client')
        formset = ContactPersonFormset(request.POST, prefix='contact_person')
        if form.is_valid() and formset.is_valid():
            client = form.save()
            client.manager = request.user
            client.save()
            for contact_form in formset:
                contact_person = contact_form.save(commit=False)
                contact_person.organization = client
                contact_person.save()
            return redirect('clients:clients_main')
    else:
        form = AddClientManagerForm(prefix='client')
        formset = ContactPersonFormset(prefix='contact_person')
    return render(request, 'clients/add_client.html', {'form': form, 'formset': formset})


@login_required(login_url="login:main")
def client_detail(request, client_id):
    """
    Принимает client.id от пользователя. Проверяет, является ли запрашивающий пользователь тем, кто сохранен в поле
    "manager", в случае прохождения проверки возвращает страницу с детальной информацией о клиенте, в ином случае,
    перенаправляет пользователя на страницу access_denied.
    Если пользователь staff, то возвращает детальную информацию, независимо от того, кто указан в поле "manager" у
    клиента.
    """
    client = Client.objects.get(id=client_id)
    if client.manager.id == request.user.id or request.user.is_staff:
        return render(request, 'clients/client_detail.html', {"client": client})
    else:
        return redirect("dashboard:access_denied")


@login_required(login_url="login:main")
def client_add_contact(request, client_id):
    organization = Client.objects.get(id=client_id)
    if request.method == "POST":
        form = ContactPersonForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect(reverse("clients:client_detail", args=[client_id]))
    else:
        form = ContactPersonForm(initial={"organization": organization})
        return render(request, "clients/add_contact.html", {"form": form,
                                                            "organization": organization})


@login_required(login_url="login:main")
def contact_person_detail(request, contact_person_id):
    contact_person = ContactPerson.objects.get(id=contact_person_id)
    if contact_person.organization.manager.id == request.user.id or request.user.is_staff:
        return render(request, "clients/contact_person_detail.html", {"contact": contact_person})
    else:
        return redirect("dashboard:access_denied")


@login_required(login_url="login:main")
def contact_person_change(request, contact_person_id):
    contact_person = ContactPerson.objects.get(id=contact_person_id)
    if contact_person.organization.manager.id == request.user.id or request.user.is_staff:
        if request.method == "POST":
            form = ContactPersonForm(request.POST, instance=contact_person)
            if form.is_valid():
                updated_contact_person = form.save(commit=False)
                updated_contact_person.save()
                return redirect(reverse("clients:contact_person_detail", args=[contact_person.pk]))
        else:
            form = ContactPersonForm(instance=contact_person)
        return render(request, "clients/change_contact.html", context={"contact": contact_person,
                                                                       "form": form})
    else:
        return redirect("dashboard:access_denied")

