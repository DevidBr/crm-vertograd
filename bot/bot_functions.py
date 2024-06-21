import os
from dotenv import load_dotenv
from bot.main_bot import bot


load_dotenv()


def bot_deal_has_been_added(deal, manager):
    bot.send_message(chat_id=os.getenv("ADMIN_API"), parse_mode="html", text=f"""
Была создана сделка № <b>{deal.pk}</b>,

<b>Услуга:</b> {deal.service};
<b>Клиент:</b> {deal.organization.name};
<b>Менеджер:</b> {manager}
""")


def bot_send_request_price(manager, service, client):
    bot.send_message(chat_id=os.getenv("ADMIN_API"), parse_mode="html", text=f"""
Получена заявка на оценку стоимости от {manager};
<b>Услуга:</b> {service};
<b>Заказчик:</b> {client}.
""")


def bot_created_commercial_offer(manager, deal, commercial_offer):
    bot.send_message(chat_id=os.getenv("ADMIN_API"), parse_mode="html", text=f"""
Было создано КП № <b>{commercial_offer.number}</b>,

<b>Сделка:</b> 
- Услуга: {deal.service};
- Стоимость: {deal.price};
- Себестоимость: {deal.cost_price};
- Предварительная прибыль: {deal.price - deal.cost_price}

<b>Клиент:</b> {deal.organization.name}
<b>Менеджер:</b> {manager}
""")


def bot_send_request_contract(manager, deal):
    bot.send_message(chat_id=os.getenv("ADMIN_API"), parse_mode="html", text=f"""
Получен запрос договора,

<b>Сделка:</b>
- Услуга: {deal.service}; 
- Стоимость: {deal.price};
- Себестоимость: {deal.cost_price};
- Предварительная прибыль: {deal.price - deal.cost_price}

<b>Клиент:</b> {deal.organization.name}
<b>Менеджер:</b> {manager}
""")


def bot_price_request_has_been_completed(deal, chat_id):
    bot.send_message(chat_id=chat_id, parse_mode="html", text=f"""
Оценка стоимости для клиента {deal.organization.name} завершена,

<b>Сделка:</b>
- Услуга: {deal.service}; 
- Стоимость: {deal.price};
- Себестоимость: {deal.cost_price};
- Предварительная прибыль: {deal.price - deal.cost_price}

<b>Клиент:</b> {deal.organization.name}
""")


def contract_has_been_created(contract_number, deal_pk, client, chat_id):
    bot.send_message(chat_id=chat_id, parse_mode="html", text=f"""
Создан договор №{contract_number} для клиента {client}.
Можете взять его в карточке сделки №{deal_pk}.
""")


