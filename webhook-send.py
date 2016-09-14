# -*- coding: utf8 -*-

from errbot import BotPlugin, webhook

class WebhookSend(BotPlugin):
    """
    Err plugin to send messages to chats/users through webhooks
    """

    @webhook
    def send_message(self, request):
        self.log.debug("Received: {}".format(request))
        return None
