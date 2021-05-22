import re
from nonebot.adapters.cqhttp import Bot, Event, MessageEvent
from nonebot.message import event_preprocessor
from nonebot.typing import T_State

from .alias_list import aliases


@event_preprocessor
async def handle(bot: Bot, event: Event, state: T_State):
    if not isinstance(event, MessageEvent):
        return
    msgs = event.get_message()
    if len(msgs) > 0 and msgs[0].type == 'text':
        alias_all = aliases.get_alias_all()
        msg = str(msgs[0]).lstrip()
        for name in sorted(alias_all, reverse=True):
            if re.match(f'{name}', msg):
                msg = re.sub(f'{name}', f'{alias_all[name]}', msg, count=1)
                event.message[0].data['text'] = msg
                return
