import re

from pprint import pprint

import fastapi
import httpx


from pydantic import BaseModel

app = fastapi.FastAPI()

INSTANCE_URL = "https://qdon.space"


class WebHook(BaseModel):
    event: str
    created_at: str
    object: dict


@app.post("/hooks/{hook_id}/{hook_token}")
async def hook(hook_id: str, hook_token: str, hook_object: WebHook):

    if hook_object.event == 'status.created':
        return await handle_status_created(hook_id, hook_token, hook_object.object)
    else:
        print(f'Unprocessible event: {hook_object.event}')
        return fastapi.Response(status_code=400)


async def handle_status_created(hook_id: str, hook_token: str, status):
    pprint(status)
