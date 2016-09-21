# -*- coding: utf8 -*-

from errbot import BotPlugin, webhook, re_botcmd
from bottle import abort

class WebhookSend(BotPlugin):
    """
    Err plugin to send messages to chats/users through webhooks
    """

    def activate(self):

        super(WebhookSend, self).activate()
        self.start_poller(60, self.mute_callback)
        if not 'muted' in self.keys():
            self.log.info("Initializing 'muted' storage")
            self['muted'] = {}

    @webhook('/send_message/' ,form_param = 'payload')
    def send_message(self, request):
        try:
                self.log.debug("Payload: {}".format(request['to']))
        except:
                self.log.debug("Malformed request: {}".format(request))
                abort(500, "Internal Server Error")
        muted = self['muted']
        if request['to'] not in muted.keys():
            to = self.build_identifier(request['to'])
            text = request['text']
            self.send(to, text)
            return None
        else:
            self.log.info("User {} muted, no action".format(request['to']))
            return None

    @re_botcmd(pattern=r"((fuck|back)off|mute)\s*([0-9]+)?")
    def mute_messages(self, msg, match):
        timeout = 15
        if match.group(3):
            timeout = match.group(3)

        user = msg.frm.nick
        self.log.info("Muting messages to {} for {} minutes".format(user, timeout))
        muted = self['muted']
        muted[user] = int(timeout)
        self['muted'] = muted
        yield("I will not send messages to {} for {} minutes".format(user, timeout))

    def mute_callback(self):
        muted = self['muted']
        for u in muted:
            muted[u] -= 1
            if muted[u] <= 0:
                del muted[u]
        self['muted'] = muted
