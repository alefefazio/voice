# coding: utf-8
import os
import json
from django.http.response import HttpResponse, JsonResponse
from django.contrib import auth
from commons.django_model_utils import get_or_none
from commons.django_views_utils import ajax_login_required
from core.service import log_svc, todo_svc
from django.views.decorators.csrf import csrf_exempt
from slackclient import SlackClient
# Your app's Slack bot user token
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN', 'bot_token')
SLACK_VERIFICATION_TOKEN = os.getenv('SLACK_VERIFICATION_TOKEN', 'verification_token')

# Slack client for Web API requests
slack_client = SlackClient(SLACK_BOT_TOKEN)

def dapau(request):
    raise Exception('break on purpose')


@csrf_exempt
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    user_dict = None
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            log_svc.log_login(request.user)
            user_dict = _user2dict(user)
    return JsonResponse(user_dict, safe=False)


def logout(request):
    if request.user.is_authenticated():
        log_svc.log_logout(request.user)
    auth.logout(request)
    return HttpResponse('{}', content_type='application/json')


def whoami(request):
    i_am = {
        'user': _user2dict(request.user),
        'authenticated': True,
    } if request.user.is_authenticated() else {'authenticated': False}
    return JsonResponse(i_am)


@ajax_login_required
def add_todo(request):
    todo = todo_svc.add_todo(request.POST['new_task'])
    return JsonResponse(todo)


@ajax_login_required
def list_todos(request):
    todos = todo_svc.list_todos()
    return JsonResponse({'todos': todos})


def _user2dict(user):
    d = {
        'id': user.id,
        'name': user.get_full_name(),
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'permissions': {
            'ADMIN': user.is_superuser,
            'STAFF': user.is_staff,
        }
    }
    return d


def verify_slack_token(request_token):
    if SLACK_VERIFICATION_TOKEN != request_token:
        print("Error: invalid verification token!")
        print("Received {} but was expecting {}".format(request_token, SLACK_VERIFICATION_TOKEN))
        return HttpResponse("Request contains invalid Slack verification token", 403)
@csrf_exempt
def message_options(request):
    if request.method == 'POST':
        # Parse the request payload
        form_json = json.loads(request.POST["payload"])

        # Verify that the request came from Slack
        verify_slack_token(form_json["token"])

        # Dictionary of menu options which will be sent as JSON
        menu_options = {
            "options": [
                {
                    "text": "Cappuccino",
                    "value": "cappuccino"
                },
                {
                    "text": "Latte",
                    "value": "latte"
                }
            ]
        }

        return HttpResponse(json.dumps(menu_options), content_type='application/json')
@csrf_exempt
def message_actions(request):
    if request.method == 'POST':
        # Parse the request payload
        form_json = json.loads(request.POST["payload"])

        # Verify that the request came from Slack
        verify_slack_token(form_json["token"])

        # Check to see what the user's selection was and update the message accordingly
        selection = form_json["actions"][0]["selected_options"][0]["value"]

        if selection == "cappuccino":
            message_text = "cappuccino"
        else:
            message_text = "latte"

        response = slack_client.api_call(
        "chat.update",
        channel=form_json["channel"]["id"],
        ts=form_json["message_ts"],
        text="One {}, right coming up! :coffee:".format(message_text),
        attachments=[] # empty `attachments` to clear the existing massage attachments
        )

        # Send an HTTP 200 response with empty body so Slack knows we're done here
        return HttpResponse(json.dumps(response), content_type='application/json', status=200)
# A Dictionary of message attachment options
attachments_json = [
    {
        "fallback": "Upgrade your Slack client to use messages like these.",
        "color": "#3AA3E3",
        "attachment_type": "default",
        "callback_id": "menu_options_2319",
        "actions": [
            {
                "name": "sentimentos",
                "text": "escolhe só um...",
                "type": "select",
                "data_source": "external"
            }
        ]
    }
]

# Send a message with the above attachment, asking the user if they want coffee
def send_message():
    slack_client.api_call(
    "chat.postMessage",
    channel="CAJ9A1LBA",
    text = "O que fazer",
    attachments=attachments_json
    )

send_message()
