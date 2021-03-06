import re

chat_message = re.compile(r":\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")


class TwitchTags:
    def __init__(self, raw_tags):
        self.tags = parse_raw_tags(raw_tags)

    def __getitem__(self, tag):
        if tag in self.tags:
            return self.tags[tag]
        return None


class TwitchChatMessage:
    def __init__(self, raw_tags, raw_message, username):
        self.message = raw_message.strip()
        self.tags = TwitchTags(raw_tags)
        if self.tags['display-name']:
            self.username = self.tags['display-name']
        else:
            self.username = username

    def is_sub_message(self):
        return 'founder' in self.tags['badges'] or 'subscriber' in self.tags['badges']

    def is_mod_message(self):
        return self.tags['mod'] == 1 or 'broadcaster' in self.tags['badges']


def parse_raw_response(response):
    user_info = chat_message.search(response)
    raw_tags, raw_message, username = '', '', ''
    if user_info:
        user_info = user_info.group(0)
        username = re.search(r"\w+", user_info).group(0)
        raw_tags, raw_message = tuple(chat_message.split(response))

    return TwitchChatMessage(raw_tags, raw_message, username)


def parse_raw_tags(raw_tags):
    if raw_tags:
        raw_tags_info = raw_tags.split(';')
        for raw_tag in raw_tags_info:
            raw_tag = raw_tag.split('=')
        return {tag[0]: tag[1] for tag in raw_tags_info}
    return {}


# Some useful twitch irc commands
def mess(sock, message, channel):
    sock.send("PRIVMSG #{} :{}\r\n".format(channel, message).encode("UTF-8"))


def ban(sock, user, channel):
    mess(sock, ".ban {}".format(user), channel)


def timeout(sock, user, channel, seconds=500):
    mess(sock, ".timeout {}".format(user, seconds), channel)
