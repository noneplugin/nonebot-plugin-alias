# nonebot-plugin-alias

为 [nonebot2](https://github.com/nonebot/nonebot2) 的指令创建别名

### 使用

**以下命令需要加[命令前缀](https://v2.nonebot.dev/docs/api/config#Config-command_start) (默认为`/`)，可自行设置为空**

- `alias {name}={command}` 添加别名
- `alias {name}` 查看别名
- `unalias {name}` 删除别名

> [!WARNING]
>
> 别名仅在当前私聊/群聊下对当前用户有效
>
> 且不会持久化保存（机器人重启后别名失效）


### 示例

<div align="left">
  <img src="https://s2.loli.net/2024/09/06/DpTZCdkK3jL9yRi.png" width="400" />
</div>
