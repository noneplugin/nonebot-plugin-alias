from copy import deepcopy
from typing import NamedTuple

from nonebot import on_command, require
from nonebot.adapters import Bot, Event, Message
from nonebot.matcher import Matcher
from nonebot.message import handle_event
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

require("nonebot_plugin_alconna")

from nonebot_plugin_alconna import Alconna, Args, KeyWordVar, MultiVar, on_alconna

__plugin_meta__ = PluginMetadata(
    name="命令别名",
    description="为机器人指令创建别名",
    usage=(
        "添加别名：alias {name}={command}\n"
        "查看别名：alias {name}\n"
        "删除别名：unalias {name}"
    ),
    type="application",
    homepage="https://github.com/noneplugin/nonebot-plugin-alias",
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={
        "example": "alias 喷水='echo 呼风唤雨'\nunalias 喷水",
    },
)


class Alias(NamedTuple):
    name: str
    command: str
    matcher: type[Matcher]


_aliases: dict[str, dict[str, Alias]] = {}

alias_matcher = on_alconna(
    Alconna(
        "alias",
        Args["names", MultiVar(str, "*")][
            "aliases", MultiVar(KeyWordVar(str, "="), "*")
        ],
    ),
    block=True,
    priority=11,
    use_cmd_start=True,
)
unalias_matcher = on_alconna(
    Alconna("unalias", Args["names", MultiVar(str, "*")]),
    block=True,
    priority=11,
    use_cmd_start=True,
)


@alias_matcher.handle()
async def _(
    event: Event, matcher: Matcher, names: tuple[str, ...], aliases: dict[str, str]
):
    session_id = event.get_session_id()
    responses = []

    if not names and not aliases:
        for name, _alias in _aliases.get(session_id, {}).items():
            responses.append(f"{name}='{_alias.command}'")

    for name in names:
        _alias = _aliases.get(session_id, {}).get(name)
        if _alias:
            responses.append(f"{name}='{_alias.command}'")
        else:
            responses.append(f"不存在的别名：{name}")

    for name, command in aliases.items():
        if session_id not in _aliases:
            _aliases[session_id] = {}
        if _alias := _aliases[session_id].get(name):
            _alias.matcher.destroy()
        _aliases[session_id][name] = Alias(
            name, command, create_alias_matcher(session_id, name, command)
        )
        responses.append(f"成功添加别名：{name}='{command}'")

    if responses:
        await matcher.send("\n".join(responses))


@unalias_matcher.handle()
async def _(event: Event, matcher: Matcher, names: tuple[str, ...]):
    session_id = event.get_session_id()
    responses = []

    for name in names:
        if name in _aliases.get(session_id, {}):
            _aliases[session_id][name].matcher.destroy()
            _aliases[session_id].pop(name)
            responses.append(f"成功删除别名：{name}")
        else:
            responses.append(f"不存在的别名：{name}")

    if responses:
        await matcher.send("\n".join(responses))


def create_alias_matcher(session_id: str, name: str, command: str) -> type[Matcher]:
    def _rule(event: Event) -> bool:
        return event.get_session_id() == session_id

    _matcher = on_command(name, block=False, rule=_rule)

    @_matcher.handle()
    async def _(bot: Bot, event: Event, msg: Message = CommandArg()):
        def get_message():
            new_message = msg.__class__(command)
            for new_segment in reversed(new_message):
                msg.insert(0, new_segment)
            return msg

        fake_event = deepcopy(event)
        fake_event.get_message = get_message
        await handle_event(bot, fake_event)

    return _matcher
