# -*- coding: utf8 -*-

from errbot import BotPlugin, webhook
from bottle import abort

class WebhookSend(BotPlugin):
    """
    Err plugin to send messages to chats/users through webhooks
    """

    @webhook('/send_message/' ,form_param = 'payload')
    def send_message(self, request):
        try:
                self.log.debug("Payload: {}".format(request['to']))
        except:
                self.log.debug("Malformed request: {}".format(request))
                abort(500, "Internal Server Error")
        to = self.build_identifier(request['to'])
        text = request['text']
        self.send(to, text)
        return None
