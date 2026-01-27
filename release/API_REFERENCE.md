# LL_XTCAT Bot API 参考文档

本文档供快速了解框架 API，用于开发插件。

---

## 目录

1. [快速开始](#快速开始)
2. [插件结构](#插件结构)
3. [事件装饰器](#事件装饰器)
4. [生命周期钩子](#生命周期钩子)
5. [API 列表](#api-列表)
6. [示例插件](#示例插件)
7. [注意事项](#注意事项)

---

## 快速开始

```python
from core import Plugin, on_message, on_notice, on_request, MessageEvent

class MyPlugin(Plugin):
    name = "插件名称"
    description = "插件描述"
    version = "1.0.0"
    author = "作者"

    @on_message(message_type="group", keywords=["关键词"])
    async def handler(self, event: MessageEvent):
        await self.bot.api.send_group_msg(event.group_id, "回复内容")
```

---

## 插件结构

每个插件是 `plugins/` 下的一个目录，包含 `__init__.py`：

```
plugins/
└── my_plugin/
    ├── __init__.py    # 插件主文件（必需）
    ├── data/          # 数据目录（通过 self.data_dir 访问）
    └── ui/            # UI 目录（可选）
        └── index.html # 配置界面
```

### 插件 UI 配置界面

插件可提供 `ui/index.html` 作为配置界面，通过「打开UI」按钮在浏览器中打开。

**Plugin API 服务器接口：** 框架内置 HTTP API 服务器（默认 `http://127.0.0.1:3890`），提供以下接口：

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/plugin/{name}/data/{file}` | 读取插件数据文件 |
| POST | `/api/plugin/{name}/data/{file}` | 保存插件数据文件（JSON body） |
| DELETE | `/api/plugin/{name}/data/{file}` | 删除插件数据文件 |
| GET | `/api/plugin/{name}/data` | 列出插件 data 目录下所有文件 |
| GET | `/ui/plugin/{name}/{path}` | 访问插件 UI 静态文件 |
| GET | `/get_group_list` | 获取机器人群列表（代理 OneBot API） |

**JavaScript 示例：**

```javascript
// 从 URL 获取插件名和 API 基础地址
const pluginName = window.location.pathname.match(/^\/ui\/plugin\/([^\/]+)/)[1];
const apiBase = window.location.origin;

// 读取数据
const res = await fetch(`${apiBase}/api/plugin/${pluginName}/data/config.json`);
const data = await res.json();

// 保存数据
await fetch(`${apiBase}/api/plugin/${pluginName}/data/config.json`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
});

// 删除数据
await fetch(`${apiBase}/api/plugin/${pluginName}/data/config.json`, {
    method: 'DELETE'
});

// 列出所有数据文件
const listRes = await fetch(`${apiBase}/api/plugin/${pluginName}/data`);
const { files } = await listRes.json();  // files: ["config.json", "users.json", ...]

// 获取群列表
const groupRes = await fetch(`${apiBase}/get_group_list`);
const { data: groupList } = await groupRes.json();  // groupList: [{group_id, group_name}, ...]
```

**插件代码中读取数据：**

```python
import json

class MyPlugin(Plugin):
    async def on_load(self):
        config_file = self.data_dir / "config.json"
        if config_file.exists():
            self.config = json.loads(config_file.read_text(encoding='utf-8'))
```

---

## 事件装饰器

### @on_message - 消息事件

```python
@on_message(
    message_type="group",     # "private" 或 "group"
    keywords=["你好"],        # 包含任一关键词触发
    startswith="/cmd",        # 以指定前缀开头
    endswith="结尾",          # 以指定后缀结尾
    command="help"            # 命令（自动加 / 前缀）
)
async def handler(self, event: MessageEvent):
    # event.user_id - 发送者 QQ
    # event.group_id - 群号（群消息）
    # event.raw_message - 原始消息文本
    # event.message_id - 消息 ID
    # event.sender - 发送者信息
    pass
```

### @on_notice - 通知事件

```python
@on_notice(notice_type="group_increase")  # 群成员增加
async def handler(self, event: NoticeEvent):
    pass

# notice_type 可选值:
# group_increase - 群成员增加
# group_decrease - 群成员减少
# group_ban - 群禁言
# group_admin - 群管理员变动
# friend_add - 好友添加
# poke - 戳一戳
```

### @on_request - 请求事件

```python
@on_request(request_type="friend")  # "friend" 或 "group"
async def handler(self, event: RequestEvent):
    # event.flag - 请求标识（用于处理请求）
    pass
```

---

## 生命周期钩子

```python
class MyPlugin(Plugin):
    async def on_load(self):
        """插件加载时"""
        pass

    async def on_unload(self):
        """插件卸载时"""
        pass

    async def on_enable(self):
        """插件启用时"""
        pass

    async def on_disable(self):
        """插件禁用时"""
        pass
```

---

## API 列表

所有 API 通过 `self.bot.api` 调用，均为异步方法。

### 消息相关

| 方法 | 说明 | 参数 |
|------|------|------|
| `send_private_msg(user_id, message)` | 发送私聊消息 | user_id: QQ号, message: 消息内容 |
| `send_group_msg(group_id, message)` | 发送群消息 | group_id: 群号, message: 消息内容 |
| `delete_msg(message_id)` | 撤回消息 | message_id: 消息ID |
| `get_msg(message_id)` | 获取消息详情 | message_id: 消息ID |
| `mark_msg_as_read(message_id)` | 标记消息已读 | message_id: 消息ID |
| `get_forward_msg(message_id)` | 获取转发消息详情 | message_id: 转发消息ID |
| `send_group_forward_msg(group_id, messages)` | 发送群合并转发 | messages: 转发节点列表 |
| `send_private_forward_msg(user_id, messages)` | 发送私聊合并转发 | messages: 转发节点列表 |
| `get_group_msg_history(group_id, message_seq, count)` | 获取群历史消息 | message_seq: 起始序号, count: 数量 |
| `get_friend_msg_history(user_id, message_seq, count)` | 获取好友历史消息 | 同上 |
| `set_msg_emoji_like(message_id, emoji_id)` | 表情回应消息 | emoji_id: 表情ID |
| `delete_msg_emoji_like(message_id, emoji_id)` | 删除表情回应 | 同上 |

### 用户相关

| 方法 | 说明 | 参数 |
|------|------|------|
| `get_login_info()` | 获取登录号信息 | 无 |
| `get_stranger_info(user_id)` | 获取陌生人信息 | user_id: QQ号 |
| `get_friend_list()` | 获取好友列表 | 无 |
| `get_friends_with_category()` | 获取好友分组列表 | 无 |
| `send_like(user_id, times)` | 点赞 | times: 次数(默认1) |
| `friend_poke(user_id)` | 好友戳一戳 | user_id: QQ号 |
| `set_friend_remark(user_id, remark)` | 设置好友备注 | remark: 备注名 |
| `delete_friend(user_id)` | 删除好友 | user_id: QQ号 |
| `set_qq_avatar(file)` | 设置QQ头像 | file: 图片路径 |
| `get_avatar(user_id, group_id, size)` | 获取头像 | size: 尺寸(默认640) |

### 群信息相关

| 方法 | 说明 | 参数 |
|------|------|------|
| `get_group_info(group_id)` | 获取群信息 | group_id: 群号 |
| `get_group_list()` | 获取群列表 | 无 |
| `get_group_member_info(group_id, user_id)` | 获取群成员信息 | - |
| `get_group_member_list(group_id)` | 获取群成员列表 | group_id: 群号 |
| `get_group_honor_info(group_id, type)` | 获取群荣誉信息 | type: "all"等 |
| `get_group_system_msg()` | 获取群系统消息 | 无 |
| `get_group_at_all_remain(group_id)` | 获取@全体剩余次数 | group_id: 群号 |
| `get_group_shut_list(group_id)` | 获取群禁言列表 | group_id: 群号 |

### 群管理相关

| 方法 | 说明 | 参数 |
|------|------|------|
| `set_group_kick(group_id, user_id, reject_add_request)` | 踢出群成员 | reject_add_request: 是否拒绝再加群 |
| `set_group_kick_batch(group_id, user_ids, reject_add_request)` | 批量踢出 | user_ids: QQ号列表 |
| `set_group_ban(group_id, user_id, duration)` | 禁言 | duration: 秒数(0=解禁) |
| `set_group_whole_ban(group_id, enable)` | 全体禁言 | enable: True/False |
| `set_group_admin(group_id, user_id, enable)` | 设置管理员 | enable: True/False |
| `set_group_card(group_id, user_id, card)` | 设置群名片 | card: 名片内容 |
| `set_group_name(group_id, group_name)` | 设置群名 | group_name: 新群名 |
| `set_group_leave(group_id, is_dismiss)` | 退出群组 | is_dismiss: 是否解散 |
| `set_group_special_title(group_id, user_id, special_title)` | 设置群头衔 | special_title: 头衔 |
| `set_group_remark(group_id, remark)` | 设置群备注 | remark: 备注 |
| `group_poke(group_id, user_id)` | 群内戳一戳 | - |
| `send_group_sign(group_id)` | 群打卡 | group_id: 群号 |

### 群公告相关

| 方法 | 说明 | 参数 |
|------|------|------|
| `send_group_notice(group_id, content, image)` | 发送群公告 | image: 可选图片 |
| `get_group_notice(group_id)` | 获取群公告 | group_id: 群号 |
| `delete_group_notice(group_id, notice_id)` | 删除群公告 | notice_id: 公告ID |

### 精华消息相关

| 方法 | 说明 | 参数 |
|------|------|------|
| `get_essence_msg_list(group_id)` | 获取群精华消息 | group_id: 群号 |
| `set_essence_msg(message_id)` | 设置精华消息 | message_id: 消息ID |
| `delete_essence_msg(message_id)` | 删除精华消息 | message_id: 消息ID |

### 请求处理相关

| 方法 | 说明 | 参数 |
|------|------|------|
| `set_friend_add_request(flag, approve, remark)` | 处理好友请求 | flag: 请求标识, approve: 是否同意 |
| `set_group_add_request(flag, sub_type, approve, reason)` | 处理加群请求 | sub_type: "add"/"invite" |

### 文件相关

| 方法 | 说明 | 参数 |
|------|------|------|
| `get_file(file, download)` | 获取文件详情 | file: 文件名, download: 是否下载 |
| `get_image(file)` | 获取图片详情 | file: 图片文件名 |
| `get_record(file, out_format)` | 获取语音详情 | out_format: 输出格式(mp3等) |
| `download_file(url, base64, name, headers)` | 下载文件到缓存 | url或base64二选一 |

### 群文件相关

| 方法 | 说明 | 参数 |
|------|------|------|
| `upload_group_file(group_id, file, name, folder_id)` | 上传群文件 | file: 文件路径 |
| `upload_private_file(user_id, file, name)` | 上传私聊文件 | file: 文件路径 |
| `get_group_root_files(group_id)` | 获取群根目录文件 | group_id: 群号 |
| `get_group_files_by_folder(group_id, folder_id)` | 获取子目录文件 | folder_id: 文件夹ID |
| `get_group_file_url(group_id, file_id)` | 获取群文件链接 | file_id: 文件ID |
| `get_group_file_system_info(group_id)` | 获取群文件系统信息 | group_id: 群号 |
| `delete_group_file(group_id, file_id)` | 删除群文件 | file_id: 文件ID |
| `create_group_file_folder(group_id, folder_name)` | 创建群文件夹 | folder_name: 文件夹名 |
| `delete_group_folder(group_id, folder_id)` | 删除群文件夹 | folder_id: 文件夹ID |
| `rename_group_folder(group_id, folder_id, new_folder_name)` | 重命名文件夹 | - |

### 系统相关

| 方法 | 说明 | 参数 |
|------|------|------|
| `get_version_info()` | 获取版本信息 | 无 |
| `get_status()` | 获取Bot状态 | 无 |
| `clean_cache()` | 清理缓存 | 无 |
| `set_restart(delay)` | 重启OneBot | delay: 延迟秒数 |
| `set_online_status(status, ext_status, battery_status)` | 设置在线状态 | status: 见下表 |
| `get_cookies(domain)` | 获取Cookies | domain: 域名 |
| `ocr_image(image)` | 图片OCR | image: 图片路径/URL/base64 |

**在线状态值:**
- 10: 在线
- 30: 离开
- 40: 隐身
- 50: 忙碌
- 60: Q我吧
- 70: 请勿打扰

### 通用 API 调用

```python
# 调用文档中未封装的 API
result = await self.bot.api.call_api("action_name", param1=value1, param2=value2)
```

---

## 示例插件

### 复读机

```python
from core import Plugin, on_message, MessageEvent

class EchoPlugin(Plugin):
    name = "复读机"
    version = "1.0.0"

    @on_message(message_type="group", startswith="复读 ")
    async def echo(self, event: MessageEvent):
        text = event.raw_message[3:].strip()
        if text:
            await self.bot.api.send_group_msg(event.group_id, text)
```

### 入群欢迎

```python
from core import Plugin, on_notice, NoticeEvent

class WelcomePlugin(Plugin):
    name = "入群欢迎"
    version = "1.0.0"

    @on_notice(notice_type="group_increase")
    async def welcome(self, event: NoticeEvent):
        msg = f"欢迎 [CQ:at,qq={event.user_id}] 加入本群！"
        await self.bot.api.send_group_msg(event.group_id, msg)
```

### 自动同意好友请求

```python
from core import Plugin, on_request, RequestEvent

class AutoApprovePlugin(Plugin):
    name = "自动同意"
    version = "1.0.0"

    @on_request(request_type="friend")
    async def approve(self, event: RequestEvent):
        await self.bot.api.set_friend_add_request(event.flag, approve=True)
```

### 群管理示例

```python
from core import Plugin, on_message, MessageEvent

class AdminPlugin(Plugin):
    name = "群管理"
    version = "1.0.0"

    @on_message(message_type="group", command="ban")
    async def ban_user(self, event: MessageEvent):
        # 命令格式: /ban @用户
        for seg in event.message:
            if seg.get("type") == "at":
                target_id = int(seg["data"]["qq"])
                await self.bot.api.set_group_ban(
                    event.group_id,
                    target_id,
                    duration=600  # 10分钟
                )
                await self.bot.api.send_group_msg(
                    event.group_id,
                    f"已禁言 {target_id}"
                )
                break
```

### 合并转发消息

```python
from core import Plugin, on_message, MessageEvent

class ForwardPlugin(Plugin):
    name = "转发示例"
    version = "1.0.0"

    @on_message(message_type="group", command="forward")
    async def send_forward(self, event: MessageEvent):
        messages = [
            {
                "type": "node",
                "data": {
                    "uin": 10001,
                    "name": "系统消息",
                    "content": [{"type": "text", "data": {"text": "第一条消息"}}]
                }
            },
            {
                "type": "node",
                "data": {
                    "uin": 10001,
                    "name": "系统消息",
                    "content": [{"type": "text", "data": {"text": "第二条消息"}}]
                }
            }
        ]
        await self.bot.api.send_group_forward_msg(event.group_id, messages)
```

---

## 注意事项

1. 所有处理器必须是 `async def` 异步函数
2. 插件目录名以 `_` 开头会被忽略
3. 不要在插件中直接操作 UI（不同线程）
4. 使用 `event.raw_data` 调试事件过滤问题
5. 通过 `self.data_dir` 获取插件专属数据目录
