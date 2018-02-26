from django.views import generic
from django.db import transaction
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import SuspiciousOperation
from constance import config
from .models import Crontab
import slack


class HomeView(generic.ListView):
    model = Crontab
    context_object_name = 'crontabs'
    template_name = 'home.html'


class UsageView(generic.TemplateView):
    template_name = 'usage.html'


class NewCrontabView(generic.CreateView):
    model = Crontab
    fields = ('channel_name', 'gerrit_query', 'crontab')
    template_name = 'crontab_form.html'
    success_url = '/'


@transaction.atomic
def slack_oauth(request):
    get_state = request.GET.get('state')
    session_state = request.session.get('oauth_state')
    if get_state is None or session_state is None or get_state != session_state:
        raise SuspiciousOperation('Invalid state. You have been logged and will be caught.')

    error = request.GET.get('error')
    if error == 'access_denied':
        messages.error(request, 'Access denied - Request cancelled')
        return redirect('/')
    elif error is not None:
        messages.error(request, 'Unknown error - try again')
        return redirect('/')

    slack_app = slack.App(config.SLACK_CLIENT_ID, config.SLACK_CLIENT_SECRET, config.SLACK_REDIRECT_URI)
    res = slack_app.request_oauth_token(request.GET['code'])
    print(res)

    if not res['ok']:
        messages.error(request, 'Permission has been granted, but OAuth token request has failed')
        return redirect('/')

    # These are database operations through the constance app
    config.ACCESS_TOKEN = res['access_token']
    config.SCOPE = res['scope']
    config.USER_ID = res['user_id']
    config.TEAM_NAME = res['team_name']
    config.TEAM_ID = res['team_id']
    config.BOT_USER_ID = res['bot']['bot_user_id']
    config.BOT_ACCESS_TOKEN = res['bot']['bot_access_token']

    messages.success(request, 'Succesfully installed Slackbot.')
    return redirect('/')