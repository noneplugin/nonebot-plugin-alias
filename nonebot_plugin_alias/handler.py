from nonebot.adapters.cqhttp import Bot, Event, MessageEvent, GroupMessageEvent
from nonebot.message import event_preprocessor
from nonebot.typing import T_State

from .parser import parse_msg


@event_preprocessor
async def handle(bot: Bot, event: Event, state: T_State):
    if not isinstance(event, MessageEvent):
        return
    msgs = event.get_message()
    if len(msgs) < 1 or msgs[0].type != 'text':
        return
    msg = str(msgs[0]).lstrip()
    if not msg:
        return

    try:
        msg = parse_msg(msg, get_id(event))
        event.message[0].data['text'] = msg
    except:
        return


def get_id(event: MessageEvent) -> str:
    if isinstance(event, GroupMessageEvent):
        return 'group_' + str(event.group_id)
    else:
        return 'private_' + str(event.user_id)
