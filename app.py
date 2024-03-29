import re

from datetime import datetime

import fastapi
import httpx
from lxml import html
from pydantic import BaseModel


app = fastapi.FastAPI()


# Blurhash, size
blocklist_images = [
    ('UTQcblVY%gIU8w8_%Mxu%2Rjayt7.8?bMxRj', '1009x200'),  # Discord URL
    ('UCSs4}tS_4aIx]ofM{WE?cV?D$tSD$WY%NjE', '1080x1080'),  # Spam image with url
    ('UkKBv%k8Oas:t1f9V[ae|;afoJofs;bYovjZ', '200x200'),  # Spam image with url (2)
]

MENTIONS_RE = re.compile(r'^(\s*(@[\w_.-]+))*$')
SPAM_URL = 'https://discord.gg/ctkpaarr'


class WebHook(BaseModel):
    event: str
    created_at: str
    object: dict


def is_mention_only(content: str):
    doc = html.fromstring(content)
    for elem in doc.cssselect('.u-url.mention'):
        elem.drop_tree()

    text = doc.text_content().strip()
    return MENTIONS_RE.text(text)


@app.post("/hooks/{instance}/{token}")
async def hook(instance: str, token: str, hook_object: WebHook):

    if hook_object.event == 'status.created':
        return await handle_status_created(instance, token, hook_object.object)
    else:
        print(f'Unprocessible event: {hook_object.event}')
        return fastapi.Response(status_code=400)


async def handle_status_created(instance: str, token: str, status):
    account = status['account']
    acct = account['acct']
    display_name = account['display_name']
    acc_created_at = account['created_at']
    acc_created_at = datetime.strptime(acc_created_at, '%Y-%m-%dT%H:%M:%S.%fZ')
    visibility = status['visibility']
    reblog = status.get('reblog', None)
    mentions = status.get('mentions', [])
    language = status['language']
    content = status['content']

    username = acct.split('@')[0] if ('@' in acct) else acct
    print(f'acct: {acct}, username: {username}')

    url = status['url']

    if reblog is not None:
        return

    if visibility != 'public':
        print(f'{url} is not public')
        return
    if language not in ['ja', None]:
        print(f'{url} is not japanese')
        return
    # if display_name:
    #     return

    if acc_created_at < datetime(2024, 2, 14):
        print(f'{url} is from old account')
        return

    if len(username) != 10:
        print(f'{url} is from non-10letter account')
        return

    # Temporary aggressive
    print(f'!!! {url}')
    return do_it(account, instance, token)

    if SPAM_URL in content:
        print('Got! Spam URL')
        return do_it(account, instance, token)

    if is_mention_only(content):
        return do_it(account, instance, token)

    # XXX: Disabled for now because some users are posting with some text
    # if not is_mention_only(content):
    #     return

    media_attachments = status.get('media_attachments', [])
    if len(media_attachments) != 1:
        return

    media = media_attachments[0]
    blurhash = media.get('blurhash', None)
    size = media.get('meta', {}).get('original', {}).get('size', None)
    if (blurhash, size) in blocklist_images:
        return do_it(account, instance, token)


async def do_it(account, instance, token):
    print(f'Spam found: {account["acct"]}')
    async with httpx.AsyncClient() as client:
        res = await client.post(
            f'https://{instance}/api/v1/admin/accounts/{account["id"]}/action',
            headers={
                'Authorization': f'Bearer {token}',
            },
            json={
                'type': 'suspend',
                'text': '2024-02 kuroneko spam',
            }
        )
        print(res.status_code)
        if res.is_success:
            print(res.text)
