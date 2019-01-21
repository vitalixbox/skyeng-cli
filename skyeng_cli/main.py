import sys
import logging
from pprint import pprint

import click

from skyeng_cli.skyeng import SkyengApiAuth, SkyengApi


logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


@click.group()
@click.option('--debug', '-d', is_flag=True, default=False)
@click.option('--username', '-u')
@click.option('--password', '-p')
@click.option('--token', '-t')
@click.pass_context
def cli(ctx, debug, username, password, token):
    if debug:
        logger.setLevel(logging.DEBUG)

    if token:
        ctx.obj['auth'] = SkyengApiAuth.from_token_global(token_global=token)
    elif username and password:
        ctx.obj['auth'] = SkyengApiAuth.from_userpass(
            username=username, password=password
        )
    else:
        raise click.ClickException(
            'Auth options must be set. --token or --username + --password'
        )

    ctx.obj['api'] = SkyengApi(ctx.obj['auth'])


@cli.command('get-token')
@click.pass_context
def get_token(ctx):
    print(ctx.obj['auth'].auth().token_global)


@cli.command()
@click.pass_context
def wordsets(ctx):
    profile = ctx.obj['api'].get_profile()
    wordsets = ctx.obj['api'].get_wordsets(profile['id'])
    pprint(wordsets)


@cli.command()
@click.pass_context
def words(ctx):
    profile = ctx.obj['api'].get_profile()
    wordsets = ctx.obj['api'].get_wordsets(profile['id'])
    words = {}
    
    for ws in wordsets:
        _words = ctx.obj['api'].get_words(profile['id'], ws['id'])
        for word in _words:
            words[word['meaningId']] = word
            words[word['meaningId']]['wordset'] = ws

    meanings = ctx.obj['api'].get_meanings(words.keys())
    for meaning in meanings:
        words[meaning['id']]['meaning'] = meaning

    pprint(words)


def entry_point():
    cli(obj={})


if __name__ == '__main__':
    entry_point()
