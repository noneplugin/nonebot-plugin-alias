from nonebot import on_shell_command
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.rule import ArgumentParser
from nonebot.typing import T_State

from .handler import *

__usage__ = '为指令设置别名\nUsage:\n  alias [别名]=[指令名称]\n  unalias [别名]'
__version__ = '0.1.0'
__plugin_name__ = 'alias'


alias_parser = ArgumentParser()
alias_parser.add_argument('-p', '--print', action='store_true')
alias_parser.add_argument('names', nargs='*')

alias = on_shell_command('alias', parser=alias_parser, priority=10)

unalias_parser = ArgumentParser()
unalias_parser.add_argument('-a', '--all', action='store_true')
unalias_parser.add_argument('names', nargs='*')

unalias = on_shell_command('unalias', parser=unalias_parser, priority=10)


@alias.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    args = state['args']
    if args.print:
        message = ''
        alias_all = aliases.get_alias_all()
        for name in sorted(alias_all):
            message += f"{name}='{alias_all[name]}'\n"
        message = message.strip()
        if message:
            await alias.finish(message)
        else:
            await alias.finish('尚未添加任何别名')

    message = ''
    names = args.names
    for name in names:
        if '=' in name:
            name, command = name.split('=', 1)
            if name and command and aliases.add_alias(name, command):
                message += f"成功添加别名：{name}='{command}'\n"
        else:
            command = aliases.get_alias(name)
            if command:
                message += f"{name}='{command}'\n"
            else:
                message += f"不存在的别名：{name}\n"

    message = message.strip()
    if message:
        await alias.send(message)


@unalias.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    args = state['args']
    if args.all:
        if aliases.del_alias_all():
            await unalias.finish('成功删除所有别名')

    message = ''
    names = args.names
    for name in names:
        if aliases.get_alias(name):
            if aliases.del_alias(name):
                message += f"成功删除别名：{name}\n"
        else:
            message += f"不存在的别名：{name}\n"

    message = message.strip()
    if message:
        await unalias.send(message)
