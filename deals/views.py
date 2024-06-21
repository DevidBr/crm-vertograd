from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import View
from django.utils import timezone
from django.contrib import messages

from bot.bot_functions import bot_send_request_price, bot_created_commercial_offer, bot_send_request_contract, \
    bot_price_request_has_been_completed, contract_has_been_created, bot_deal_has_been_added
from clients.models import Client
from deals.forms import AddDealForm, AddCommentForDealForm, PriceRequestForm, PlantForPriceRequestFormset, \
    ConfirmRequestPriceForm, AddCommercialOfferForm, ContractRequestForm, ContractCreateForm
from deals.models import Deal, PlantForPriceRequest, PriceRequest, CommercialOffer, ContractRequest, Contract
from services.models import Service


STATUS_CHOICES = [
    ("1", "Новая сделка."),
    ("2", "Выявлена потребность"),
    ("3", "Формируется наше предложение"),
    ("4", "Предложение сформировано, разрабатываем КП"),
    ("5", "КП направлено на рассмотрение заказчику"),
    ("6", "Согласование условий"),
    ("7", "КП согласовано, подготавливаем договор"),
    ("8", "Согласование договора обеими сторонами"),
    ("9", "Договор направлен на подпись"),
    ("10", "Договор подписан"),
    ("11", "Счет направлен заказчику. Контроль оплаты."),
    ("12", "Счет оплачен, передано в работу"),
    ("13", "В работе"),
    ("14", "Сделка завершена успешно. Акты подписаны."),
    ("15", "Сделка завершена без успеха"),
    ("16", "Архив")
]


# name = deals:deals_list
@login_required(login_url="login:main")
def deals_list(request):
    deals = []
    if not request.user.is_staff:
        my_clients = Client.objects.filter(manager__id=request.user.id)
    else:
        my_clients = Client.objects.all()
    for client in my_clients:
        for deal in client.deals.all().exclude(status__in=["14", "15", "16"]):
            deals.append(deal)
    deals_count = len(deals)
    return render(request, 'deals/deals_list.html', {
        "deals": deals,
        "deals_count": deals_count
    })


@method_decorator(login_required(login_url="/"), "dispatch")
class RequestPrice(View):
    """
    class RequestPrice обернут в декоратор method_decorator, проверяющий, залогинен ли пользователь?
    Описывает методы get и post. Представляет форму для создания объекта "Запрос стоимости" и формсет для
    создания объектов "Растение для запроса стоимости", имеющих FK к объекту "Запрос стоимости".
    """

    # Описываем переменные с формой для "Запроса стоимости" и форм-сетом для "Растения для запроса"
    price_request_form = PriceRequestForm
    plants_formset = PlantForPriceRequestFormset

    def get(self, request, deal_pk):
        """
        Принимает request и deal_pk.
        Рендерит форму price_request_form и формсет plants_formset
        """

        # Определяем сделку, к которой привяжем запрос стоимости
        deal = get_object_or_404(Deal, pk=deal_pk)

        # Проверка статуса сделки. Если сделка не в статусе 2, то редирект обратно на карту сделки, чтобы
        # не было доступа делать запрос стоимости с какого-либо другого статуса.
        if deal.status != "2":
            return redirect(reverse("deals:deal_detail", args=[deal.pk]))

        # Описываем контекст для рендера формы и форм-сета
        context = {
            "deal": deal,
            "price_request_form": self.price_request_form(initial={
                "deal": deal
            }),
            "plants_formset": self.plants_formset
        }
        # Возвращаем рендер с контекстом
        return render(request, "deals/request_price.html", context=context)

    def post(self, request, deal_pk):
        """
        Принимает request, содержащий заполненную форму и форм-сет.
        Возвращает JsonResponse для ajax, описанный в js скрипте.
        """

        # Определяем форму для "Запроса стоимости" и передаем в нее данные из request.POST, полученные туда из ajax
        price_request_form = self.price_request_form(request.POST)

        # Определяем форм-сет для "Растений для запроса стоимости" и передаем в него данные
        # из request.POST и request.FILES, полученные из ajax
        plants_formset = self.plants_formset(request.POST, request.FILES)

        # Если форма и форм-сет валидны
        if price_request_form.is_valid() and plants_formset.is_valid():
            # то создаем объект "Запрос стоимости"
            new_price_request = price_request_form.save(commit=False)
            # сохраняем ссылку на сделку
            deal = new_price_request.deal
            # сохраняем объект "Запрос стоимости"
            new_price_request.save()

            # Перебираем формы в форм-сете
            for plant_form in plants_formset:
                # Если перебираемая форма валидна, то
                if plant_form.is_valid():
                    # Определяем plant_data, записывая в него cleaned_data словарь
                    plant_data = plant_form.cleaned_data
                    # Определяем plant_file, "забирая" значение 'photo' из cleaned_data словаря plant_data
                    plant_file = plant_data.get('photo')

                    # Создаем новый объект "Растение для запроса стоимости", забирая значения из plant_data
                    new_plant_for_request_price = PlantForPriceRequest(
                        name=plant_data.get("name"),
                        quantity=plant_data.get("quantity"),
                        height=plant_data.get("height"),
                        photo=None,
                        price_request=new_price_request
                    )
                    # Если в plant_file что-то есть (если пользователь загрузил в форму фотографию), то
                    if plant_file:
                        # Сохраняем это фото в поле photo объекта "Растение для запроса стоимости"
                        new_plant_for_request_price.photo.save(plant_file.name, plant_file)
                    # Окончательно сохраняем объект "Растение для запроса стоимости"
                    # TODO: приделать бота, отправляющего сообщение на manager.telegram_id
                    new_plant_for_request_price.save()

            # Меняем статус сделки на "3"
            deal.status = "3"
            # Сохраняем сделку
            deal.save()

            # Определяем url для дальнейшего перенаправления в ajax
            redirect_to_deal_detail_url = (
                request.build_absolute_uri(reverse("deals:deal_detail", args=[deal.pk])))

            # отправка сообщения в телеграм боте. Функция описана в модуле bot_functions.py
            bot_send_request_price(manager=f"{self.request.user.last_name} {self.request.user.first_name}",
                                   service=deal.service,
                                   client=deal.organization.name)

            # Возвращаем JsonResponse с url для window.location.href в скрипте.
            return JsonResponse(data={"success": "Все ок", "redirect_url": redirect_to_deal_detail_url}, status="200")


@login_required(login_url="login:main")
def deal_change_service(request, deal_id):
    deal = Deal.objects.get(id=deal_id)
    if request.method == "POST":
        new_service_id = request.POST.get('service')
        if new_service_id:
            new_service = Service.objects.get(id=new_service_id)
            deal.service = new_service
            deal.status = "2"
            deal.save()
            return JsonResponse(data={"success": "Услуга успешно добавлена", "status": 200})
        else:
            return JsonResponse(data={"success": "Услуга не выбрана. Выберите услугу.", "status": 400})


@login_required(login_url="login:main")
def deal_detail(request, deal_id, deal_update_form=None):
    deal = Deal.objects.get(id=deal_id)
    deal_status = int(deal.status)
    next_deal_status = deal_status + 1
    next_deal_status_value = dict(STATUS_CHOICES).get(f"{next_deal_status}")
    if deal.manager.id == request.user.id or request.user.is_staff:
        if request.method == "POST":
            add_comment_form = AddCommentForDealForm(request.POST)
            if add_comment_form.is_valid():
                add_comment_form.save()
                return redirect(reverse("deals:deal_detail", args=[deal_id]))
        add_comment_form = AddCommentForDealForm(initial={
            "deal": deal_id,
            "author": request.user.id
        })

        if deal.status == "4":
            actual_date = timezone.now()
            actual_month_and_year = f"/{actual_date.strftime('%m')}{actual_date.strftime('%y')}"
            last_commercial_offer = CommercialOffer.objects.filter(creator=request.user).last()
            if last_commercial_offer:
                last_counter_number = last_commercial_offer.counter_number
                actual_counter_number = last_counter_number + 1
            else:
                actual_counter_number = 1

            add_commercial_offer_form = AddCommercialOfferForm(initial={
                "date": timezone.now(),
                "number": f"{request.user.pk}-{actual_counter_number}{actual_month_and_year}",
                "counter_number": actual_counter_number,
                "creator": request.user.pk
            })
            return render(request, template_name="deals/deal_detail.html",
                          context={"deal": deal,
                                   "add_comment_form": add_comment_form,
                                   "add_commercial_offer_form": add_commercial_offer_form,
                                   "actual_month_and_year": actual_month_and_year})
        else:
            return render(request, template_name="deals/deal_detail.html",
                          context={"deal": deal,
                                   "add_comment_form": add_comment_form,
                                   "next_status": next_deal_status_value})
    else:
        return redirect("dashboard:access_denied")


@login_required(login_url="login:main")
def add_deal(request, client_id):
    client = Client.objects.get(id=client_id)
    if client.manager.id != request.user.id and not request.user.is_staff:
        return redirect("dashboard:access_denied")
    if request.method == "POST":
        form = AddDealForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            if ((cleaned_data['manager'].id == request.user.id
                 and cleaned_data['organization'].id == client.id)
                    or cleaned_data['manager'].is_staff):
                new_deal = form.save(commit=False)
                # Проверяем, была ли выбрана услуга сразу при создании сделки, или нет?

                # Если услуга не выбрана и в объекте deal.service = None, то присваивается статус
                # 1 (Новая сделка. Необходимо выбрать услугу.)
                if new_deal.service is None:
                    new_deal.status = "1"

                # Если выбрана какая-то услуга, то статус сделки = 2 (Выявлена потребность. Необходимо запросить стоимость у руководителя.)
                else:
                    new_deal.status = "2"
                new_deal.save()
                bot_deal_has_been_added(deal=new_deal, manager=f"{request.user.last_name} {request.user.first_name}")
                return redirect(reverse("deals:deal_detail", args=[new_deal.pk]))
            else:
                return redirect("dashboard:access_denied")

    else:
        form = AddDealForm(initial={"organization": client_id,
                                    "manager": request.user,
                                    "status": "1"})
    return render(request, template_name="deals/add_deal.html", context={"client": client,
                                                                         "form": form})


@method_decorator(login_required(login_url="/"), "dispatch")
class PriceRequestListView(View):
    def get(self, request, filter=None):
        if not request.user.is_staff:
            return redirect(to="dashboard:access_denied")
        else:
            if not filter:
                price_requests = PriceRequest.objects.all()
                return render(request, template_name="deals/for_directors/price_request_list.html",
                              context={"price_requests": price_requests})


@method_decorator(login_required(login_url="/"), "dispatch")
class PriceRequestDetailView(View):
    def get(self, request, price_request_pk):
        price_request = PriceRequest.objects.get(pk=price_request_pk)
        if request.user.is_staff:
            deal = Deal.objects.get(pk=price_request.deal.pk)
            confirm_price_form = ConfirmRequestPriceForm()
            return render(request,
                          template_name='deals/price_request_detail.html',
                          context={'price_request': price_request,
                                   'confirm_price_form': confirm_price_form})
        else:
            return render(request,
                          template_name='deals/price_request_detail.html',
                          context={'price_request': price_request})

    def post(self, request, price_request_pk):
        if not request.user.is_staff:
            return redirect(to="dashboard:access_denied")
        else:
            deal_for_upgrade = Deal.objects.get(price_request__pk=price_request_pk)
            confirm_price_form = ConfirmRequestPriceForm(request.POST)
            price_request = deal_for_upgrade.price_request
            if confirm_price_form.is_valid():
                cost_price = confirm_price_form.cleaned_data.get('cost_price')
                price = confirm_price_form.cleaned_data.get('price')
                deal_for_upgrade.cost_price = cost_price
                deal_for_upgrade.price = price
                deal_for_upgrade.status = "4"
                deal_for_upgrade.save()
                price_request.status = 2
                price_request.save()
                bot_price_request_has_been_completed(deal=deal_for_upgrade,
                                                     chat_id=deal_for_upgrade.manager.profile.telegram_chat_id)
                return self.get(request, price_request_pk)


@require_POST
def commercial_offer_save(request, deal_id):
    deal = Deal.objects.get(pk=deal_id)
    add_commercial_offer_form = AddCommercialOfferForm(request.POST, request.FILES)
    if add_commercial_offer_form.is_valid():
        new_commercial_offer = add_commercial_offer_form.save(commit=False)
        new_commercial_offer.deal = deal
        new_commercial_offer.save()
        deal.status = "5"
        deal.save()
        bot_created_commercial_offer(manager=request.user.last_name,
                                     deal=deal,
                                     commercial_offer=new_commercial_offer)
        return redirect(reverse("deals:deal_detail", args=[deal_id]))
    else:
        print("Форма не была валидна")
        return redirect(reverse("deals:deal_detail", args=[deal_id]))


@login_required(login_url="login:main")
@require_POST
def commercial_offer_has_been_sent_to_the_client(request, deal_id):
    deal = get_object_or_404(Deal, pk=deal_id)
    deal.status = "6"
    deal.save()
    return redirect(reverse("deals:deal_detail", args=[deal_id]))


@method_decorator(login_required(login_url="/"), "dispatch")
class ContractRequestView(View):
    def get(self, request, deal_id):
        deal = Deal.objects.get(pk=deal_id)
        contract_request_form = ContractRequestForm(initial={
            "deal": deal.pk,
            "creator": request.user.pk
        })
        return render(request, template_name="deals/contract_request.html",
                      context={"deal": deal,
                               "contract_request_form": contract_request_form
                               })

    def post(self, request, deal_id):
        deal = Deal.objects.get(pk=deal_id)
        contract_request_form = ContractRequestForm(request.POST)
        if contract_request_form.is_valid():
            contract_request_form.save()
            deal.status = "7"
            deal.save()
            bot_send_request_contract(manager=request.user.last_name, deal=deal)
            return redirect(reverse("deals:deal_detail", args=[deal_id]))
        return redirect(reverse("deals:deal_detail", args=[deal_id]))


@method_decorator(login_required(login_url="/"), "dispatch")
class ContractRequestsListView(View):
    def get(self, request, filter=None):
        if not request.user.is_staff:
            return redirect(to="dashboard:access_denied")
        else:
            if not filter:
                contract_requests = ContractRequest.objects.all()
                return render(request, template_name="deals/for_directors/contract_request_list.html",
                              context={"contract_requests": contract_requests})


@method_decorator(login_required(login_url="/"), "dispatch")
class ContractRequestDetailAndCreateContractView(View):
    def get(self, request, contract_request_pk):
        if not request.user.is_staff:
            return redirect(to="dashboard:access_denied")
        else:
            actual_date = timezone.now()
            actual_year = actual_date.strftime("%y")
            actual_month = actual_date.strftime("%m")
            last_contract_pk = Contract.objects.all().last().pk
            contract_request = ContractRequest.objects.get(pk=contract_request_pk)
            contract_create_form = ContractCreateForm(initial={
                "deal": contract_request.deal,
                "contract_number": f"{actual_year}{actual_month}/{last_contract_pk+1}"
            })
            return render(request,
                          template_name="deals/for_directors/contract_request_detail.html",
                          context={"contract_request": contract_request,
                                   "contract_create_form": contract_create_form})

    def post(self, request, contract_request_pk):
        if not request.user.is_staff:
            return redirect(to="dashboard:access_denied")
        else:
            contract_request = ContractRequest.objects.get(pk=contract_request_pk)
            contract_create_form = ContractCreateForm(request.POST, request.FILES)
            if contract_create_form.is_valid():
                new_contract = contract_create_form.save(commit=False)
                print("Сохраняем договор без коммита")
                print(f"{new_contract=}")

                print("Меняем статус у договора на 1")
                new_contract.status = "1"
                # Удаляем запрос на основе которого делали договор.
                contract_request.delete()
                print("Удалили запрос договора")
                # Меняем статус сделки, связанной с договором
                print("Извлекаем сделку, чтобы ей тоже поменять статус")
                updated_deal = new_contract.deal
                print(f"{updated_deal=}")
                updated_deal.status = "8"
                print(f"{updated_deal.status=}")
                updated_deal.save()
                print("Сохраняем новый договор")
                new_contract.save()
                contract_has_been_created(
                    contract_number=new_contract.contract_number,
                    deal_pk=updated_deal.pk,
                    client=updated_deal.organization.name,
                    chat_id=updated_deal.manager.profile.telegram_chat_id,
                )
                return redirect(reverse("deals:contract_request_list"))