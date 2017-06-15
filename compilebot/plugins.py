from slackbot.bot import listen_to
from slackbot.bot import respond_to
from slackbot import settings
from sphere_engine import CompilersClientV3
import re
import time

@respond_to(r'.*', re.IGNORECASE)
@listen_to(r'(?:^|\s|[\W]+)<@{}>'.format(settings.BOT_ID), re.IGNORECASE)
def respond(message):
    bot = CompileBot(message)
    try:
        bot.resolve_language()
        if settings.DEBUG:
            print('resolved lang: ' + bot.lang)
    except ValueError:
        message.reply('Language {} not found or supported'.format(bot.lang))
        return

    bot.compile()
    bot.reply()

class CompileBot:
    def __init__(self, message):
        self.message = message
        if settings.DEBUG:
            print('message: ' + self.message.body['text'])

        c_pattern = (
            r'\s*(?:<@.*?>)?\s*(?P<lang>.*)\s*\n\s*'
            r'(?P<args>.*)?\s*\n?\s*'
            r'```(?P<src>(.*\n?)*?)```'
            r'(?:\n\s*((?i)Input|Stdin):?\s*\n\s*)?'
            r'(?:```(?P<in>(.*\n?)*)```)?'
        )
        m = re.search(c_pattern, message.body['text'])
        if m:
            self.lang = m.group('lang')
            self.options = m.group('args').lower() or ''
            self.source = m.group('src')
            self.input = m.group('in') or ''
        else:
            message.reply("I couldn't understand you")
            return

        if settings.DEBUG:
            print('lang: ' + self.lang)
            print('args: ' + self.options)
            print('source: ' + self.source)
            print('input: ' + self.input)

        self.client = CompilersClientV3(settings.SE_API_TOKEN,
            settings.SE_API_ENDPOINT)

    def resolve_language(self):
        lang = self.lang.lower()
        for l in self.client.compilers()['items']:
            if (l['name'].lower() == lang or l['short'].lower() == lang
                    or l['ver'].lower() == lang):
                self.lang = l['id']
                return
        raise ValueError()

    def compile(self):
        r = self.client.submissions.create(self.source, self.lang, self.input)
        while self.client.submissions.get(r['id'])['status'] != 0:
            time.sleep(1)
        result = self.client.submissions.get(r['id'], False, False, True, True, True)

        if settings.DEBUG:
            print(result)

        self.status = result['result']
        self.stderr = result['stderr']
        self.stdout = result['output']
        self.memory = result['memory']
        self.time = result['time']
        self.cmpinfo = result['cmpinfo'] or ''

    def reply(self):
        reply = ''
        if self.status != 15:
            reply += 'There was an error processing your code:\n'
        if self.status == 11:
            reply += 'Compilation error\n'
        elif self.status == 12:
            reply += 'Runtime error\n'
        elif self.status == 13:
            reply += 'Time limit exceeded\n'
        elif self.status == 17:
            reply += 'Memory limit exceeded\n'
        elif self.status == 19:
            reply += 'Illegal system call\n'
        elif self.status == 20:
            reply += 'Internal error\n'

        if (self.status != 15 and self.cmpinfo != ''):
            reply += 'Compilation Output:\n```{}```\n'.format(self.cmpinfo)

        if self.stdout != '':
            reply += 'Output:\n```{}```'.format(self.stdout)
        if self.stderr != '':
            reply += 'Stderr:\n```{}```'.format(self.stderr)
        if 'memory' in self.options:
            reply += '\nMemory Usage: {} bytes\n'.format(self.memory)
        if 'time' in self.options:
            reply += '\nExecution Time: {} seconds\n'.format(self.time)
        self.message.reply(reply)

