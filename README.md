# slack-compilebot
Like [/u/compilebot](https://github.com/renfredxh/compilebot), but for Slack.

## The Basics
All you have to do is mention CompileBot in a thread, or send it a direct
message, along with a language and source code:

> @compilebot python
>
>     print("Hello World!")
>

CompileBot will then process your message, execute it remotely, and then
respond with the output:

> Output:
>
>     Hello World!
>

Code blocks are done with three backtics (```) in Slack:

> \```  
> code here  
> \```

### Supplying Input
You can also give an input block that the program will use as Stdin:

> @compilebot python 3
>
>     n = int(input())
>     while n != 42:
>         print(n)
>         n = int(input())
>
> Input:
>
>     1
>     2
>     10
>     42
>     11

Make sure the word "input" is written before the code block followed by a colon.
Also make sure the line with "input" is not included in a code block.
CompileBot will take the block and supply it as standard input to the program:

> Output:
>
>     1
>     2
>     10

### Options
You can supply additional options in your comment that will signal CompileBot
to display additional information. You can place these options after the
programming language on a new line and before the code block.

> @compilebot Ruby  
> time memory
>
>     x = 1
>     50000.times { x *= 10 }
>     puts x / 10 ** 50000
Reply:

> Output:
>
>     1
>
> Memory Usage: 75776 bytes  
> Execution Time: 0.48 seconds

## How it works
CompileBot runs off the [slackbot](https://github.com/lins05/slackbot) API, and
uses the [Sphere Engine](https://github.com/sphere-engine/python-client) API to
execute the code.

Note that Sphere Engine no longer is giving out free forever accounts, so
unless you already have a free account and an API token, you will need to make
a trial account.

Inspired by [compilebot](https://github.com/renfredxh/compilebot) for Reddit.

## Contributing
Even if you don't want to contribute to the compilebot source, we need people
for testing and improving documentation.

If you would like to contribute new features, or fix bugs or contribute
anything else to the compilebot module, you can follow the instructions
below to get a local instance of compilebot set up on your system.

## Installation
### Docker
Running on Docker is the simplest way to setup the bot.
You will need a Slack bot token and a
[Sphere Engine API](https://sphere-engine.com/signup) token.

Run the container with `docker-run` or `docker-compose`:

```bash
docker run --name=slack-compilebot \
    --restart=always \
    -e SE_API_TOKEN=token \
    -e SLACK_BOT_ID=UXXXXXXXX \
    -e SLACK_API_TOKEN=xoxb-XXXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXX \
    rycieos/slack-compilebot
```

```yaml
version: '2.3'
services:
  slack-compilebot:
    image: rycieos/slack-compilebot
    restart: always
    environment:
      - SE_API_TOKEN=token
      - SLACK_BOT_ID=UXXXXXXXX
      - SLACK_API_TOKEN=xoxb-XXXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXX
```

#### Env options:
* `DEBUG`: Default `False`. If True, print debugging messages in the logs.
* `SE_API_TOKEN`: The Sphere Engine API token to use for authentication.
* `SE_API_ENDPOINT`: The URL endpoint. The default is probably good.
* `SLACK_BOT_ID`: The Slack bot ID to respond to, in `UXXXXXXXX` format. It's easy to get from the webapp by "Inspect Element"ing the `@bot` username.
* `SE_API_TOKEN`: The Slack token to authenticate with. Can be generated at the [old style bot](https://slack.com/apps/A0F7YS25R-bots) page.
* `ERRORS_TO`: The slack username (not user ID) of the user to report bot errors to. Could also be a channel name (not channel ID). This will not be compile errors, but actual errors with the bot. Optional.

### Local
Requires Python 3.4+

```bash
git clone git@github.com:Rycieos/slack-compilebot.git
cd slack-compilebot
```

Setup a virtual env and download dependencies

```bash
virtualenv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

Copy default settings and set them. You will need a Slack bot token and a
[Sphere Engine API](https://sphere-engine.com/signup) token.

```bash
cp slackbot_settings.py.dist slackbot_settings.py
#edit slackbot_settings.py
```

Finally, run it:

```bash
python run.py
```

## Supported Languages
CompileBot supports any language that is supported by
[ideone](http://ideone.com/). Chances are CompileBot can process any language
you would want to use. However, if the language you are looking for isn't
available, you can contact Ideone/Sphere Engine to add a new one, and
CompileBot will automatically support it.

Some languages need an entry point, like `int main()` in C. All languages use
the standard for the language. For Java, the `main()` method needs to be in the
public class `Main`. For C#, the `Main()` method needs to be in the public
class `Test`.

