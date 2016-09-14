# err-webhook-send
Err chatbot plugin to send messages to chats through webhooks

## Installation and usage

To use this plugin you'll need to configure and activate [Webserver](http://errbot.io/en/latest/user_guide/plugin_development/webhooks.html) plugin first:

```
!plugin config Webserver {'HOST': '0.0.0.0', 'PORT': 3141 }
```

This will configure Errbot to listen to requests on all interfaces on port `3141`.

Install the plugin:

```
!repos install https://github.com/br0ziliy/err-webhook-send.git
```

Plugin exposes `/send_message` endpoint, which expects POST request with
`Content-Type: application/x-www-form-urlencoded` header set, and `payload` form
field, which contains following JSON: `{'to': 'username', 'text': 'message to send' }`.

`to` should contain a text representation of message recipient (this value will
be used with [build_identifier()](http://errbot.io/en/latest/errbot.botplugin.html#errbot.botplugin.BotPlugin.build_identifier) call).
Plugin does not check if a user or channel exist upon sending a message, it's up
to you to supply a valid channel/username.
For information about valid identifiers for various backends see [Identifiers](#identifiers) section below.

`text` should contain the message you'd like to send. Markdown formatting is
supported.

Example usage:

```
curl -m 5 --data-urlencode payload='{"to": "vk",  "text": "Hi there\!"}' http://${ERRBOT_IP}:3141/send_message
```

Above command will send `Hi there!` to user `vk`.

## Identifiers

List of valid identifiers for various backends:

- [IRC](http://errbot.io/en/latest/_modules/errbot/backends/irc.html#IRCBackend.build_identifier)

```
#channel
user
```

- [Slack](http://errbot.io/en/latest/errbot.backends.slack.html?highlight=build_identifier#errbot.backends.slack.SlackBackend.extract_identifiers_from_string)

```
<#C12345>
<@U12345>
<@U12345|user>
@user
#channel/user
#channel
```

- [Telegram](http://errbot.io/en/latest/_modules/errbot/backends/telegram_messenger.html#TelegramBackend.build_identifier)

Any positive integer. Telegram usernames not supported.

- [XMPP](http://errbot.io/en/latest/_modules/errbot/backends/xmpp.html#XMPPBackend.build_identifier)

Any [XEP-0030](http://xmpp.org/extensions/xep-0030.html#info)-compatible JID string.
Usually it's as simple as `user@my.jabber.host.com` or
`chatroom@my.jabber.host.com`

- HipChat

Same as XMPP

- Campfire [UNTESTED]

User name as seen in the Campfire chat room.

- Skype [UNTESTED]

A Skype ID.

- Tox [UNTESTED]

A Tox hash.
