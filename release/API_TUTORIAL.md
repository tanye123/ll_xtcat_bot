# LL_XTCAT Bot API 完整教程

本文档详细介绍了 LL_XTCAT Bot 框架中所有可用的 API 方法，每个 API 都配有详细的代码示例和逐行注释，方便学习和使用。

## 目录

1. [基础知识](#基础知识)
2. [消息相关 API](#消息相关-api)
3. [群管理相关 API](#群管理相关-api)
4. [信息获取相关 API](#信息获取相关-api)
5. [请求处理相关 API](#请求处理相关-api)
6. [用户操作相关 API](#用户操作相关-api)
7. [群管理扩展 API](#群管理扩展-api)
8. [群公告相关 API](#群公告相关-api)
9. [精华消息相关 API](#精华消息相关-api)
10. [消息扩展 API](#消息扩展-api)
11. [文件相关 API](#文件相关-api)
12. [群文件相关 API](#群文件相关-api)
13. [系统相关 API](#系统相关-api)
14. [其他 API](#其他-api)

---

## 基础知识

### API 调用方式

在插件中，所有 API 都通过 `self.bot.api` 对象调用。所有方法都是异步的，需要使用 `await` 关键字。

```python
# 基础调用格式
# self.bot.api 是 API 客户端实例
# 所有方法都是 async 的，必须用 await 调用
result = await self.bot.api.方法名(参数)
```

### 通用 API 调用

如果需要调用文档中未封装的 API，可以使用通用方法：

```python
# call_api 是通用的 API 调用方法
# 参数1: action - API 动作名称（字符串）
# 参数2: **params - API 所需的参数（关键字参数）
result = await self.bot.api.call_api("action_name", param1=value1, param2=value2)
```

---

## 消息相关 API

### 1. send_private_msg - 发送私聊消息

向指定用户发送私聊消息。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "私聊示例"

    @on_message(message_type="private", keywords=["你好"])
    async def handle_hello(self, event: MessageEvent):
        # send_private_msg: 发送私聊消息
        # 参数说明:
        #   user_id: int - 目标用户的 QQ 号（必填）
        #   message: str 或 List[Dict] - 消息内容，可以是纯文本或消息段列表（必填）
        #   auto_escape: bool - 是否将消息内容作为纯文本发送，默认 False（可选）
        # 返回值: Dict，包含 message_id 等信息

        result = await self.bot.api.send_private_msg(
            user_id=event.user_id,      # 发送给消息发送者
            message="你好！这是私聊回复"  # 消息内容
        )

        # result 示例: {"message_id": 123456}
        print(f"消息发送成功，消息ID: {result.get('message_id')}")
```

**使用场景举例：**
```python
# 场景1: 发送纯文本消息
await self.bot.api.send_private_msg(
    user_id=123456789,
    message="这是一条纯文本消息"
)

# 场景2: 发送带表情的消息（使用消息段）
await self.bot.api.send_private_msg(
    user_id=123456789,
    message=[
        {"type": "text", "data": {"text": "你好 "}},      # 文本消息段
        {"type": "face", "data": {"id": "1"}}             # QQ 表情消息段
    ]
)

# 场景3: 发送图片消息
await self.bot.api.send_private_msg(
    user_id=123456789,
    message=[
        {"type": "image", "data": {"file": "https://example.com/image.jpg"}}
    ]
)
```

---

### 2. send_group_msg - 发送群消息

向指定群聊发送消息。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "群消息示例"

    @on_message(message_type="group", keywords=["打卡"])
    async def handle_checkin(self, event: MessageEvent):
        # send_group_msg: 发送群消息
        # 参数说明:
        #   group_id: int - 目标群号（必填）
        #   message: str 或 List[Dict] - 消息内容（必填）
        #   auto_escape: bool - 是否作为纯文本发送，默认 False（可选）
        # 返回值: Dict，包含 message_id 等信息

        result = await self.bot.api.send_group_msg(
            group_id=event.group_id,    # 发送到当前群
            message="打卡成功！"          # 消息内容
        )

        print(f"群消息发送成功，消息ID: {result.get('message_id')}")
```

**使用场景举例：**
```python
# 场景1: 发送 @某人 的消息
await self.bot.api.send_group_msg(
    group_id=123456789,
    message=[
        {"type": "at", "data": {"qq": "987654321"}},  # @指定用户
        {"type": "text", "data": {"text": " 你好！"}}  # 文本内容
    ]
)

# 场景2: 发送 @全体成员 的消息
await self.bot.api.send_group_msg(
    group_id=123456789,
    message=[
        {"type": "at", "data": {"qq": "all"}},        # @全体成员
        {"type": "text", "data": {"text": " 重要通知！"}}
    ]
)

# 场景3: 发送回复消息
await self.bot.api.send_group_msg(
    group_id=123456789,
    message=[
        {"type": "reply", "data": {"id": "原消息ID"}},  # 回复指定消息
        {"type": "text", "data": {"text": "这是回复内容"}}
    ]
)
```

---

### 3. send_msg - 发送消息（通用）

通用消息发送方法，可以根据类型发送私聊或群聊消息。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "通用消息示例"

    async def send_to_user_or_group(self, event: MessageEvent):
        # send_msg: 通用消息发送方法
        # 参数说明:
        #   message_type: str - 消息类型，"private" 或 "group"（必填）
        #   user_id: int - 用户 QQ 号，私聊时必填（可选）
        #   group_id: int - 群号，群聊时必填（可选）
        #   message: str 或 List[Dict] - 消息内容（必填）
        #   auto_escape: bool - 是否作为纯文本发送（可选）
        # 返回值: Dict，包含 message_id 等信息

        # 根据消息来源自动回复
        if event.message_type == "private":
            # 私聊消息，回复私聊
            await self.bot.api.send_msg(
                message_type="private",
                user_id=event.user_id,
                message="收到你的私聊消息"
            )
        else:
            # 群消息，回复群聊
            await self.bot.api.send_msg(
                message_type="group",
                group_id=event.group_id,
                message="收到群消息"
            )
```

---

### 4. delete_msg - 撤回消息

撤回一条消息（需要有相应权限）。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "撤回示例"

    @on_message(message_type="group", keywords=["撤回测试"])
    async def handle_delete(self, event: MessageEvent):
        # 先发送一条消息
        result = await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message="这条消息将在3秒后撤回"
        )

        # 获取发送的消息ID
        message_id = result.get("message_id")

        # 等待3秒
        import asyncio
        await asyncio.sleep(3)

        # delete_msg: 撤回消息
        # 参数说明:
        #   message_id: int - 要撤回的消息ID（必填）
        # 返回值: Dict（通常为空）
        # 注意: 撤回他人消息需要管理员权限，撤回自己消息有时间限制

        await self.bot.api.delete_msg(message_id=message_id)
        print(f"消息 {message_id} 已撤回")
```

---

### 5. get_msg - 获取消息

获取指定消息的详细信息。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "获取消息示例"

    @on_message(message_type="group", command="查消息")
    async def handle_get_msg(self, event: MessageEvent):
        # get_msg: 获取消息详情
        # 参数说明:
        #   message_id: int - 消息ID（必填）
        # 返回值: Dict，包含消息的详细信息
        #   - message_id: 消息ID
        #   - real_id: 真实消息ID
        #   - sender: 发送者信息
        #   - time: 发送时间戳
        #   - message: 消息内容
        #   - raw_message: 原始消息文本

        # 获取当前消息的详情
        msg_info = await self.bot.api.get_msg(message_id=event.message_id)

        # 打印消息信息
        print(f"消息ID: {msg_info.get('message_id')}")
        print(f"发送者: {msg_info.get('sender', {}).get('nickname')}")
        print(f"发送时间: {msg_info.get('time')}")
        print(f"消息内容: {msg_info.get('raw_message')}")

---

## 群管理相关 API

### 1. set_group_kick - 踢出群成员

将指定成员踢出群聊。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "踢人示例"

    @on_message(message_type="group", command="踢人")
    async def handle_kick(self, event: MessageEvent):
        # set_group_kick: 踢出群成员
        # 参数说明:
        #   group_id: int - 群号（必填）
        #   user_id: int - 要踢出的用户 QQ 号（必填）
        #   reject_add_request: bool - 是否拒绝此人再次加群，默认 False（可选）
        # 返回值: Dict（通常为空）
        # 注意: 需要管理员或群主权限

        target_user = 123456789  # 要踢出的用户QQ号

        await self.bot.api.set_group_kick(
            group_id=event.group_id,        # 当前群
            user_id=target_user,            # 目标用户
            reject_add_request=False        # 不拒绝再次加群
        )

        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message=f"已将用户 {target_user} 踢出群聊"
        )
```

**使用场景举例：**
```python
# 场景1: 踢出并拒绝再次加群
await self.bot.api.set_group_kick(
    group_id=123456789,
    user_id=987654321,
    reject_add_request=True  # 拒绝此人再次加群
)

# 场景2: 从 @消息 中获取要踢的人
@on_message(message_type="group", command="踢")
async def kick_at_user(self, event: MessageEvent):
    # 从消息中解析被 @ 的用户
    for seg in event.message:
        if seg.get("type") == "at":
            target_qq = int(seg["data"]["qq"])
            await self.bot.api.set_group_kick(
                group_id=event.group_id,
                user_id=target_qq
            )
            break
```

---

### 2. set_group_ban - 禁言群成员

禁言指定群成员。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "禁言示例"

    @on_message(message_type="group", command="禁言")
    async def handle_ban(self, event: MessageEvent):
        # set_group_ban: 禁言群成员
        # 参数说明:
        #   group_id: int - 群号（必填）
        #   user_id: int - 要禁言的用户 QQ 号（必填）
        #   duration: int - 禁言时长（秒），0 表示解除禁言，默认 30*60=1800秒（可选）
        # 返回值: Dict（通常为空）
        # 注意: 需要管理员或群主权限

        target_user = 123456789

        # 禁言 10 分钟
        await self.bot.api.set_group_ban(
            group_id=event.group_id,
            user_id=target_user,
            duration=10 * 60  # 10分钟 = 600秒
        )

        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message=f"已禁言用户 {target_user} 10分钟"
        )
```

**使用场景举例：**
```python
# 场景1: 禁言 1 小时
await self.bot.api.set_group_ban(
    group_id=123456789,
    user_id=987654321,
    duration=3600  # 1小时 = 3600秒
)

# 场景2: 解除禁言
await self.bot.api.set_group_ban(
    group_id=123456789,
    user_id=987654321,
    duration=0  # 0秒 = 解除禁言
)

# 场景3: 禁言 1 天
await self.bot.api.set_group_ban(
    group_id=123456789,
    user_id=987654321,
    duration=86400  # 1天 = 86400秒
)
```

---

### 3. set_group_whole_ban - 全体禁言

开启或关闭全体禁言。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "全体禁言示例"

    @on_message(message_type="group", command="全体禁言")
    async def handle_whole_ban(self, event: MessageEvent):
        # set_group_whole_ban: 全体禁言
        # 参数说明:
        #   group_id: int - 群号（必填）
        #   enable: bool - True 开启全体禁言，False 关闭，默认 True（可选）
        # 返回值: Dict（通常为空）
        # 注意: 需要管理员或群主权限

        # 开启全体禁言
        await self.bot.api.set_group_whole_ban(
            group_id=event.group_id,
            enable=True  # 开启
        )

        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message="已开启全体禁言"
        )

    @on_message(message_type="group", command="解除全体禁言")
    async def handle_whole_unban(self, event: MessageEvent):
        # 关闭全体禁言
        await self.bot.api.set_group_whole_ban(
            group_id=event.group_id,
            enable=False  # 关闭
        )

        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message="已解除全体禁言"
        )
```

---

### 4. set_group_admin - 设置群管理员

设置或取消群管理员。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "管理员设置示例"

    @on_message(message_type="group", command="设管理")
    async def handle_set_admin(self, event: MessageEvent):
        # set_group_admin: 设置群管理员
        # 参数说明:
        #   group_id: int - 群号（必填）
        #   user_id: int - 目标用户 QQ 号（必填）
        #   enable: bool - True 设为管理员，False 取消管理员，默认 True（可选）
        # 返回值: Dict（通常为空）
        # 注意: 只有群主才能设置管理员

        target_user = 123456789

        # 设置为管理员
        await self.bot.api.set_group_admin(
            group_id=event.group_id,
            user_id=target_user,
            enable=True  # 设为管理员
        )

        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message=f"已将 {target_user} 设为管理员"
        )

    @on_message(message_type="group", command="取消管理")
    async def handle_unset_admin(self, event: MessageEvent):
        target_user = 123456789

        # 取消管理员
        await self.bot.api.set_group_admin(
            group_id=event.group_id,
            user_id=target_user,
            enable=False  # 取消管理员
        )
```

---

### 5. set_group_card - 设置群名片

设置群成员的群名片（群昵称）。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "群名片示例"

    @on_message(message_type="group", command="改名片")
    async def handle_set_card(self, event: MessageEvent):
        # set_group_card: 设置群名片
        # 参数说明:
        #   group_id: int - 群号（必填）
        #   user_id: int - 目标用户 QQ 号（必填）
        #   card: str - 新的群名片，空字符串表示删除群名片，默认空（可选）
        # 返回值: Dict（通常为空）
        # 注意: 管理员可以修改普通成员的名片，群主可以修改所有人的名片

        # 设置自己的群名片
        await self.bot.api.set_group_card(
            group_id=event.group_id,
            user_id=event.user_id,
            card="新的群名片"
        )

        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message="群名片已修改"
        )
```

**使用场景举例：**
```python
# 场景1: 清除群名片（恢复显示QQ昵称）
await self.bot.api.set_group_card(
    group_id=123456789,
    user_id=987654321,
    card=""  # 空字符串表示清除群名片
)

# 场景2: 批量设置群名片格式
async def set_member_card_format(self, group_id, user_id, name, department):
    # 设置统一格式的群名片，如 "[部门] 姓名"
    card = f"[{department}] {name}"
    await self.bot.api.set_group_card(
        group_id=group_id,
        user_id=user_id,
        card=card
    )
```

---

### 6. set_group_name - 设置群名

修改群名称。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "群名设置示例"

    @on_message(message_type="group", command="改群名")
    async def handle_set_name(self, event: MessageEvent):
        # set_group_name: 设置群名
        # 参数说明:
        #   group_id: int - 群号（必填）
        #   group_name: str - 新的群名（必填）
        # 返回值: Dict（通常为空）
        # 注意: 需要管理员或群主权限

        new_name = "新的群名称"

        await self.bot.api.set_group_name(
            group_id=event.group_id,
            group_name=new_name
        )

        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message=f"群名已修改为: {new_name}"
        )
```

---

### 7. set_group_leave - 退出群组

让机器人退出指定群聊。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "退群示例"

    @on_message(message_type="group", command="退群")
    async def handle_leave(self, event: MessageEvent):
        # set_group_leave: 退出群组
        # 参数说明:
        #   group_id: int - 群号（必填）
        #   is_dismiss: bool - 是否解散群（仅群主可用），默认 False（可选）
        # 返回值: Dict（通常为空）
        # 警告: 此操作不可逆，请谨慎使用

        # 先发送告别消息
        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message="再见！机器人即将退出群聊"
        )

        # 退出群聊
        await self.bot.api.set_group_leave(
            group_id=event.group_id,
            is_dismiss=False  # 仅退出，不解散
        )
```

---

## 信息获取相关 API

### 1. get_login_info - 获取登录号信息

获取当前登录的 QQ 账号信息。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "登录信息示例"

    @on_message(message_type="group", command="机器人信息")
    async def handle_login_info(self, event: MessageEvent):
        # get_login_info: 获取登录号信息
        # 参数: 无
        # 返回值: Dict
        #   - user_id: int - 机器人 QQ 号
        #   - nickname: str - 机器人昵称

        info = await self.bot.api.get_login_info()

        # 获取机器人的 QQ 号和昵称
        bot_qq = info.get("user_id")      # 机器人 QQ 号
        bot_name = info.get("nickname")   # 机器人昵称

        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message=f"机器人QQ: {bot_qq}\n昵称: {bot_name}"
        )
```

---

### 2. get_stranger_info - 获取陌生人信息

获取任意 QQ 用户的公开信息。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "陌生人信息示例"

    @on_message(message_type="group", command="查用户")
    async def handle_stranger_info(self, event: MessageEvent):
        # get_stranger_info: 获取陌生人信息
        # 参数说明:
        #   user_id: int - 目标用户 QQ 号（必填）
        #   no_cache: bool - 是否不使用缓存，默认 False（可选）
        # 返回值: Dict
        #   - user_id: int - QQ 号
        #   - nickname: str - 昵称
        #   - sex: str - 性别（male/female/unknown）
        #   - age: int - 年龄

        target_qq = 123456789

        info = await self.bot.api.get_stranger_info(
            user_id=target_qq,
            no_cache=False  # 使用缓存，提高响应速度
        )

        nickname = info.get("nickname", "未知")
        sex = info.get("sex", "unknown")
        age = info.get("age", 0)

        # 性别转换为中文
        sex_map = {"male": "男", "female": "女", "unknown": "未知"}
        sex_cn = sex_map.get(sex, "未知")

        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message=f"用户信息:\nQQ: {target_qq}\n昵称: {nickname}\n性别: {sex_cn}\n年龄: {age}"
        )
```

---

### 3. get_friend_list - 获取好友列表

获取机器人的好友列表。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "好友列表示例"

    @on_message(message_type="private", command="好友列表")
    async def handle_friend_list(self, event: MessageEvent):
        # get_friend_list: 获取好友列表
        # 参数: 无
        # 返回值: List[Dict]，每个元素包含:
        #   - user_id: int - 好友 QQ 号
        #   - nickname: str - 好友昵称
        #   - remark: str - 好友备注

        friends = await self.bot.api.get_friend_list()

        # 统计好友数量
        friend_count = len(friends)

        # 获取前5个好友的信息
        friend_info = []
        for friend in friends[:5]:
            qq = friend.get("user_id")
            name = friend.get("nickname")
            remark = friend.get("remark", "")
            # 如果有备注就显示备注，否则显示昵称
            display_name = remark if remark else name
            friend_info.append(f"{qq} - {display_name}")

        msg = f"好友总数: {friend_count}\n前5位好友:\n" + "\n".join(friend_info)

        await self.bot.api.send_private_msg(
            user_id=event.user_id,
            message=msg
        )
```

---

### 4. get_group_info - 获取群信息

获取指定群的详细信息。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "群信息示例"

    @on_message(message_type="group", command="群信息")
    async def handle_group_info(self, event: MessageEvent):
        # get_group_info: 获取群信息
        # 参数说明:
        #   group_id: int - 群号（必填）
        #   no_cache: bool - 是否不使用缓存，默认 False（可选）
        # 返回值: Dict
        #   - group_id: int - 群号
        #   - group_name: str - 群名
        #   - member_count: int - 成员数
        #   - max_member_count: int - 最大成员数

        info = await self.bot.api.get_group_info(
            group_id=event.group_id,
            no_cache=True  # 获取最新信息，不使用缓存
        )

        group_name = info.get("group_name", "未知")
        member_count = info.get("member_count", 0)
        max_member = info.get("max_member_count", 0)

        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message=f"群名: {group_name}\n成员数: {member_count}/{max_member}"
        )
```

---

### 5. get_group_list - 获取群列表

获取机器人加入的所有群。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "群列表示例"

    @on_message(message_type="private", command="群列表")
    async def handle_group_list(self, event: MessageEvent):
        # get_group_list: 获取群列表
        # 参数: 无
        # 返回值: List[Dict]，每个元素包含:
        #   - group_id: int - 群号
        #   - group_name: str - 群名
        #   - member_count: int - 成员数
        #   - max_member_count: int - 最大成员数

        groups = await self.bot.api.get_group_list()

        # 统计群数量
        group_count = len(groups)

        # 构建群列表信息
        group_info = []
        for group in groups[:10]:  # 只显示前10个
            gid = group.get("group_id")
            name = group.get("group_name")
            members = group.get("member_count", 0)
            group_info.append(f"{gid} - {name} ({members}人)")

        msg = f"已加入 {group_count} 个群:\n" + "\n".join(group_info)

        await self.bot.api.send_private_msg(
            user_id=event.user_id,
            message=msg
        )
```

---

### 6. get_group_member_info - 获取群成员信息

获取指定群成员的详细信息。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "群成员信息示例"

    @on_message(message_type="group", command="我的信息")
    async def handle_member_info(self, event: MessageEvent):
        # get_group_member_info: 获取群成员信息
        # 参数说明:
        #   group_id: int - 群号（必填）
        #   user_id: int - 用户 QQ 号（必填）
        #   no_cache: bool - 是否不使用缓存，默认 False（可选）
        # 返回值: Dict
        #   - group_id: int - 群号
        #   - user_id: int - QQ 号
        #   - nickname: str - 昵称
        #   - card: str - 群名片
        #   - sex: str - 性别
        #   - age: int - 年龄
        #   - join_time: int - 入群时间戳
        #   - last_sent_time: int - 最后发言时间戳
        #   - level: str - 群等级
        #   - role: str - 角色（owner/admin/member）
        #   - title: str - 专属头衔

        info = await self.bot.api.get_group_member_info(
            group_id=event.group_id,
            user_id=event.user_id,
            no_cache=True
        )

        nickname = info.get("nickname", "未知")
        card = info.get("card", "")  # 群名片
        role = info.get("role", "member")
        title = info.get("title", "")  # 专属头衔
        level = info.get("level", "")

        # 角色转换为中文
        role_map = {"owner": "群主", "admin": "管理员", "member": "成员"}
        role_cn = role_map.get(role, "成员")

        # 显示名称优先使用群名片
        display_name = card if card else nickname

        msg = f"你的群信息:\n昵称: {display_name}\n身份: {role_cn}"
        if title:
            msg += f"\n头衔: {title}"
        if level:
            msg += f"\n等级: {level}"

        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message=msg
        )
```

---

### 7. get_group_member_list - 获取群成员列表

获取指定群的所有成员。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "群成员列表示例"

    @on_message(message_type="group", command="成员统计")
    async def handle_member_list(self, event: MessageEvent):
        # get_group_member_list: 获取群成员列表
        # 参数说明:
        #   group_id: int - 群号（必填）
        # 返回值: List[Dict]，每个元素包含群成员信息（同 get_group_member_info）

        members = await self.bot.api.get_group_member_list(
            group_id=event.group_id
        )

        # 统计各角色人数
        owner_count = 0
        admin_count = 0
        member_count = 0

        for member in members:
            role = member.get("role", "member")
            if role == "owner":
                owner_count += 1
            elif role == "admin":
                admin_count += 1
            else:
                member_count += 1

        total = len(members)

        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message=f"群成员统计:\n总人数: {total}\n群主: {owner_count}\n管理员: {admin_count}\n普通成员: {member_count}"
        )
```

**使用场景举例：**
```python
# 场景: 查找群内所有管理员
async def get_all_admins(self, group_id):
    members = await self.bot.api.get_group_member_list(group_id=group_id)
    admins = []
    for member in members:
        if member.get("role") in ["owner", "admin"]:
            admins.append({
                "user_id": member.get("user_id"),
                "nickname": member.get("nickname"),
                "role": member.get("role")
            })
    return admins
```

---

## 请求处理相关 API

### 1. set_friend_add_request - 处理加好友请求

同意或拒绝加好友请求。

```python
from core import Plugin, on_request, RequestEvent

class MyPlugin(Plugin):
    name = "好友请求处理示例"

    @on_request(request_type="friend")
    async def handle_friend_request(self, event: RequestEvent):
        # set_friend_add_request: 处理加好友请求
        # 参数说明:
        #   flag: str - 请求标识（从事件中获取）（必填）
        #   approve: bool - 是否同意，默认 True（可选）
        #   remark: str - 添加后的好友备注，仅在同意时有效（可选）
        # 返回值: Dict（通常为空）

        # 从事件中获取请求标识
        flag = event.flag
        user_id = event.user_id

        # 自动同意所有好友请求
        await self.bot.api.set_friend_add_request(
            flag=flag,           # 请求标识，必须从事件中获取
            approve=True,        # 同意请求
            remark="自动添加"     # 设置好友备注
        )

        print(f"已自动同意 {user_id} 的好友请求")
```

**使用场景举例：**
```python
# 场景1: 根据验证消息决定是否同意
@on_request(request_type="friend")
async def handle_friend_with_check(self, event: RequestEvent):
    comment = event.comment  # 获取验证消息

    # 如果验证消息包含特定关键词则同意
    if "机器人" in comment or "bot" in comment.lower():
        await self.bot.api.set_friend_add_request(
            flag=event.flag,
            approve=True,
            remark="通过验证"
        )
    else:
        # 拒绝请求
        await self.bot.api.set_friend_add_request(
            flag=event.flag,
            approve=False  # 拒绝
        )

# 场景2: 记录请求并手动处理
pending_requests = {}  # 存储待处理的请求

@on_request(request_type="friend")
async def store_friend_request(self, event: RequestEvent):
    # 存储请求信息，等待管理员处理
    pending_requests[event.user_id] = {
        "flag": event.flag,
        "comment": event.comment,
        "time": event.time
    }
```

---

### 2. set_group_add_request - 处理加群请求/邀请

同意或拒绝加群请求或邀请。

```python
from core import Plugin, on_request, RequestEvent

class MyPlugin(Plugin):
    name = "加群请求处理示例"

    @on_request(request_type="group")
    async def handle_group_request(self, event: RequestEvent):
        # set_group_add_request: 处理加群请求/邀请
        # 参数说明:
        #   flag: str - 请求标识（从事件中获取）（必填）
        #   sub_type: str - 请求子类型，"add"（加群请求）或 "invite"（邀请入群）（必填）
        #   approve: bool - 是否同意，默认 True（可选）
        #   reason: str - 拒绝理由，仅在拒绝时有效（可选）
        # 返回值: Dict（通常为空）

        flag = event.flag
        sub_type = event.sub_type  # "add" 或 "invite"
        user_id = event.user_id
        group_id = event.group_id

        if sub_type == "add":
            # 处理加群请求
            await self.bot.api.set_group_add_request(
                flag=flag,
                sub_type="add",
                approve=True  # 同意加群
            )
            print(f"已同意 {user_id} 加入群 {group_id}")

        elif sub_type == "invite":
            # 处理邀请入群
            await self.bot.api.set_group_add_request(
                flag=flag,
                sub_type="invite",
                approve=True  # 同意邀请
            )
            print(f"已同意加入群 {group_id} 的邀请")
```

**使用场景举例：**
```python
# 场景1: 拒绝加群请求并说明理由
await self.bot.api.set_group_add_request(
    flag=event.flag,
    sub_type="add",
    approve=False,
    reason="本群暂不接受新成员"  # 拒绝理由
)

# 场景2: 根据答案验证是否同意加群
@on_request(request_type="group")
async def verify_group_request(self, event: RequestEvent):
    if event.sub_type != "add":
        return

    answer = event.comment  # 获取加群答案

    # 验证答案
    correct_answer = "机器人"
    if answer == correct_answer:
        await self.bot.api.set_group_add_request(
            flag=event.flag,
            sub_type="add",
            approve=True
        )
    else:
        await self.bot.api.set_group_add_request(
            flag=event.flag,
            sub_type="add",
            approve=False,
            reason="答案错误，请重新申请"
        )
```

---

## 用户操作相关 API

### 1. send_like - 点赞

给指定用户点赞（赞名片）。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "点赞示例"

    @on_message(message_type="group", command="赞我")
    async def handle_like(self, event: MessageEvent):
        # send_like: 点赞
        # 参数说明:
        #   user_id: int - 目标用户 QQ 号（必填）
        #   times: int - 点赞次数，默认 1，每天最多 10 次（可选）
        # 返回值: Dict（通常为空）
        # 注意: 每天对同一用户最多点赞 10 次

        await self.bot.api.send_like(
            user_id=event.user_id,
            times=10  # 点赞 10 次
        )

        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message="已给你点赞 10 次！"
        )
```

---

### 2. friend_poke - 好友戳一戳

戳一戳好友（双击头像效果）。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "好友戳一戳示例"

    @on_message(message_type="private", command="戳我")
    async def handle_friend_poke(self, event: MessageEvent):
        # friend_poke: 好友戳一戳
        # 参数说明:
        #   user_id: int - 目标好友 QQ 号（必填）
        # 返回值: Dict（通常为空）
        # 注意: 只能戳好友

        await self.bot.api.friend_poke(
            user_id=event.user_id
        )

        await self.bot.api.send_private_msg(
            user_id=event.user_id,
            message="戳了你一下！"
        )
```

---

### 3. group_poke - 群戳一戳

在群里戳一戳某人。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "群戳一戳示例"

    @on_message(message_type="group", command="戳")
    async def handle_group_poke(self, event: MessageEvent):
        # group_poke: 群戳一戳
        # 参数说明:
        #   group_id: int - 群号（必填）
        #   user_id: int - 目标用户 QQ 号（必填）
        # 返回值: Dict（通常为空）

        # 从消息中解析被 @ 的用户
        target_user = None
        for seg in event.message:
            if seg.get("type") == "at":
                target_user = int(seg["data"]["qq"])
                break

        if target_user:
            await self.bot.api.group_poke(
                group_id=event.group_id,
                user_id=target_user
            )
```

---

### 4. set_friend_remark - 设置好友备注

修改好友的备注名。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "好友备注示例"

    async def set_remark_example(self, user_id: int, remark: str):
        # set_friend_remark: 设置好友备注
        # 参数说明:
        #   user_id: int - 好友 QQ 号（必填）
        #   remark: str - 新的备注名（必填）
        # 返回值: Dict（通常为空）

        await self.bot.api.set_friend_remark(
            user_id=user_id,
            remark=remark
        )

        print(f"已将 {user_id} 的备注修改为: {remark}")
```

---

### 5. delete_friend - 删除好友

删除指定好友。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "删除好友示例"

    async def delete_friend_example(self, user_id: int):
        # delete_friend: 删除好友
        # 参数说明:
        #   user_id: int - 要删除的好友 QQ 号（必填）
        # 返回值: Dict（通常为空）
        # 警告: 此操作不可逆，请谨慎使用

        await self.bot.api.delete_friend(
            user_id=user_id
        )

        print(f"已删除好友: {user_id}")
```

---

### 6. get_friends_with_category - 获取好友分组列表

获取带分组信息的好友列表。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "好友分组示例"

    @on_message(message_type="private", command="好友分组")
    async def handle_friends_category(self, event: MessageEvent):
        # get_friends_with_category: 获取好友分组列表
        # 参数: 无
        # 返回值: List[Dict]，包含分组信息和好友列表

        categories = await self.bot.api.get_friends_with_category()

        # 遍历分组
        msg_parts = []
        for category in categories:
            cat_name = category.get("categoryName", "未分组")
            friends = category.get("buddyList", [])
            msg_parts.append(f"【{cat_name}】: {len(friends)}人")

        await self.bot.api.send_private_msg(
            user_id=event.user_id,
            message="好友分组:\n" + "\n".join(msg_parts)
        )
```

---

## 群管理扩展 API

### 1. set_group_special_title - 设置群头衔

设置群成员的专属头衔。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "群头衔示例"

    @on_message(message_type="group", command="设头衔")
    async def handle_set_title(self, event: MessageEvent):
        # set_group_special_title: 设置群头衔
        # 参数说明:
        #   group_id: int - 群号（必填）
        #   user_id: int - 目标用户 QQ 号（必填）
        #   special_title: str - 头衔内容，空字符串表示删除头衔（可选）
        # 返回值: Dict（通常为空）
        # 注意: 只有群主才能设置头衔

        await self.bot.api.set_group_special_title(
            group_id=event.group_id,
            user_id=event.user_id,
            special_title="活跃成员"  # 设置头衔
        )

        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message="已为你设置头衔: 活跃成员"
        )
```

**使用场景举例：**
```python
# 场景: 清除头衔
await self.bot.api.set_group_special_title(
    group_id=123456789,
    user_id=987654321,
    special_title=""  # 空字符串表示清除头衔
)
```

---

### 2. set_group_kick_batch - 批量踢出群成员

一次性踢出多个群成员。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "批量踢人示例"

    async def batch_kick_example(self, group_id: int, user_ids: list):
        # set_group_kick_batch: 批量踢出群成员
        # 参数说明:
        #   group_id: int - 群号（必填）
        #   user_ids: List[int] - 要踢出的用户 QQ 号列表（必填）
        #   reject_add_request: bool - 是否拒绝再次加群，默认 False（可选）
        # 返回值: Dict（通常为空）
        # 注意: 需要管理员或群主权限

        await self.bot.api.set_group_kick_batch(
            group_id=group_id,
            user_ids=user_ids,  # 例如: [123456, 789012, 345678]
            reject_add_request=False
        )

        print(f"已批量踢出 {len(user_ids)} 人")
```

---

### 3. get_group_shut_list - 获取群禁言列表

获取当前被禁言的群成员列表。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "禁言列表示例"

    @on_message(message_type="group", command="禁言列表")
    async def handle_shut_list(self, event: MessageEvent):
        # get_group_shut_list: 获取群禁言列表
        # 参数说明:
        #   group_id: int - 群号（必填）
        # 返回值: List[Dict]，每个元素包含被禁言成员信息

        shut_list = await self.bot.api.get_group_shut_list(
            group_id=event.group_id
        )

        if not shut_list:
            await self.bot.api.send_group_msg(
                group_id=event.group_id,
                message="当前没有被禁言的成员"
            )
            return

        # 构建禁言列表信息
        msg_parts = []
        for member in shut_list:
            user_id = member.get("user_id")
            shut_time = member.get("shut_up_timestamp", 0)
            msg_parts.append(f"QQ: {user_id}")

        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message=f"被禁言成员 ({len(shut_list)}人):\n" + "\n".join(msg_parts)
        )
```

---

### 4. set_group_remark - 设置群备注

设置群的备注名（仅自己可见）。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "群备注示例"

    async def set_group_remark_example(self, group_id: int, remark: str):
        # set_group_remark: 设置群备注
        # 参数说明:
        #   group_id: int - 群号（必填）
        #   remark: str - 备注名（必填）
        # 返回值: Dict（通常为空）

        await self.bot.api.set_group_remark(
            group_id=group_id,
            remark=remark
        )

        print(f"已将群 {group_id} 的备注设置为: {remark}")
```

---

### 5. get_group_honor_info - 获取群荣誉信息

获取群的荣誉信息（龙王、群聊之火等）。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "群荣誉示例"

    @on_message(message_type="group", command="群荣誉")
    async def handle_honor_info(self, event: MessageEvent):
        # get_group_honor_info: 获取群荣誉信息
        # 参数说明:
        #   group_id: int - 群号（必填）
        #   type: str - 荣誉类型，可选值:
        #     "talkative" - 龙王
        #     "performer" - 群聊之火
        #     "legend" - 群聊炽焰
        #     "strong_newbie" - 冒尖小春笋
        #     "emotion" - 快乐之源
        #     "all" - 全部（默认）
        # 返回值: Dict，包含各类荣誉信息

        honor_info = await self.bot.api.get_group_honor_info(
            group_id=event.group_id,
            type="all"  # 获取全部荣誉
        )

        # 获取龙王信息
        talkative = honor_info.get("current_talkative", {})
        if talkative:
            dragon_king = talkative.get("nickname", "无")
            await self.bot.api.send_group_msg(
                group_id=event.group_id,
                message=f"当前龙王: {dragon_king}"
            )
```

---

### 6. get_group_system_msg - 获取群系统消息

获取群系统消息（加群请求等）。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "群系统消息示例"

    @on_message(message_type="private", command="群系统消息")
    async def handle_system_msg(self, event: MessageEvent):
        # get_group_system_msg: 获取群系统消息
        # 参数: 无
        # 返回值: Dict，包含:
        #   - invited_requests: 邀请入群请求列表
        #   - join_requests: 加群请求列表

        sys_msg = await self.bot.api.get_group_system_msg()

        invited = sys_msg.get("invited_requests", [])
        join = sys_msg.get("join_requests", [])

        await self.bot.api.send_private_msg(
            user_id=event.user_id,
            message=f"待处理邀请: {len(invited)} 条\n待处理加群请求: {len(join)} 条"
        )
```

---

### 7. get_group_at_all_remain - 获取群 @全体成员 剩余次数

查询今日 @全体成员 的剩余次数。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "@全体剩余次数示例"

    @on_message(message_type="group", command="@全体次数")
    async def handle_at_all_remain(self, event: MessageEvent):
        # get_group_at_all_remain: 获取群 @全体成员 剩余次数
        # 参数说明:
        #   group_id: int - 群号（必填）
        # 返回值: Dict
        #   - can_at_all: bool - 是否可以 @全体成员
        #   - remain_at_all_count_for_group: int - 群内今日剩余次数
        #   - remain_at_all_count_for_uin: int - 机器人今日剩余次数

        remain = await self.bot.api.get_group_at_all_remain(
            group_id=event.group_id
        )

        can_at = remain.get("can_at_all", False)
        group_remain = remain.get("remain_at_all_count_for_group", 0)
        bot_remain = remain.get("remain_at_all_count_for_uin", 0)

        status = "可以" if can_at else "不可以"

        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message=f"@全体成员 状态:\n当前{status}使用\n群剩余次数: {group_remain}\n机器人剩余次数: {bot_remain}"
        )
```

---

## 群公告相关 API

### 1. send_group_notice - 发送群公告

发布群公告。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "发送群公告示例"

    @on_message(message_type="group", command="发公告")
    async def handle_send_notice(self, event: MessageEvent):
        # send_group_notice: 发送群公告
        # 参数说明:
        #   group_id: int - 群号（必填）
        #   content: str - 公告内容（必填）
        #   image: str - 公告图片，支持 http://, file://, base64://（可选）
        # 返回值: Dict（通常为空）
        # 注意: 需要管理员或群主权限

        await self.bot.api.send_group_notice(
            group_id=event.group_id,
            content="这是一条测试公告\n请大家注意查看！"
        )

        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message="群公告已发布"
        )
```

**使用场景举例：**
```python
# 场景: 发送带图片的公告
await self.bot.api.send_group_notice(
    group_id=123456789,
    content="重要通知！",
    image="https://example.com/notice.jpg"  # 公告配图
)
```

---

### 2. get_group_notice - 获取群公告

获取群公告列表。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "获取群公告示例"

    @on_message(message_type="group", command="查公告")
    async def handle_get_notice(self, event: MessageEvent):
        # get_group_notice: 获取群公告
        # 参数说明:
        #   group_id: int - 群号（必填）
        # 返回值: List[Dict]，每个元素包含:
        #   - notice_id: str - 公告ID
        #   - sender_id: int - 发布者QQ号
        #   - publish_time: int - 发布时间戳
        #   - message: Dict - 公告内容

        notices = await self.bot.api.get_group_notice(
            group_id=event.group_id
        )

        if not notices:
            await self.bot.api.send_group_msg(
                group_id=event.group_id,
                message="暂无群公告"
            )
            return

        # 获取最新一条公告
        latest = notices[0]
        content = latest.get("message", {}).get("text", "无内容")

        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message=f"最新公告:\n{content}"
        )
```

---

### 3. delete_group_notice - 删除群公告

删除指定的群公告。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "删除群公告示例"

    async def delete_notice_example(self, group_id: int, notice_id: str):
        # delete_group_notice: 删除群公告
        # 参数说明:
        #   group_id: int - 群号（必填）
        #   notice_id: str - 公告ID（必填，从 get_group_notice 获取）
        # 返回值: Dict（通常为空）
        # 注意: 需要管理员或群主权限

        await self.bot.api.delete_group_notice(
            group_id=group_id,
            notice_id=notice_id
        )

        print(f"已删除公告: {notice_id}")
```

---

## 精华消息相关 API

### 1. get_essence_msg_list - 获取群精华消息

获取群的精华消息列表。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "精华消息列表示例"

    @on_message(message_type="group", command="精华消息")
    async def handle_essence_list(self, event: MessageEvent):
        # get_essence_msg_list: 获取群精华消息
        # 参数说明:
        #   group_id: int - 群号（必填）
        # 返回值: List[Dict]，每个元素包含:
        #   - sender_id: int - 发送者QQ号
        #   - sender_nick: str - 发送者昵称
        #   - sender_time: int - 发送时间戳
        #   - operator_id: int - 设精华的管理员QQ号
        #   - operator_nick: str - 管理员昵称
        #   - operator_time: int - 设精华时间戳
        #   - message_id: int - 消息ID

        essence_list = await self.bot.api.get_essence_msg_list(
            group_id=event.group_id
        )

        count = len(essence_list)

        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message=f"本群共有 {count} 条精华消息"
        )
```

---

### 2. set_essence_msg - 设置群精华消息

将消息设为精华。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "设置精华示例"

    @on_message(message_type="group", command="设精华")
    async def handle_set_essence(self, event: MessageEvent):
        # set_essence_msg: 设置群精华消息
        # 参数说明:
        #   message_id: int - 消息ID（必填）
        # 返回值: Dict（通常为空）
        # 注意: 需要管理员或群主权限

        # 如果是回复消息，获取被回复的消息ID
        reply_id = None
        for seg in event.message:
            if seg.get("type") == "reply":
                reply_id = int(seg["data"]["id"])
                break

        if reply_id:
            await self.bot.api.set_essence_msg(
                message_id=reply_id
            )

            await self.bot.api.send_group_msg(
                group_id=event.group_id,
                message="已将该消息设为精华"
            )
```

---

### 3. delete_essence_msg - 删除群精华消息

取消消息的精华状态。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "删除精华示例"

    async def delete_essence_example(self, message_id: int):
        # delete_essence_msg: 删除群精华消息
        # 参数说明:
        #   message_id: int - 消息ID（必填）
        # 返回值: Dict（通常为空）
        # 注意: 需要管理员或群主权限

        await self.bot.api.delete_essence_msg(
            message_id=message_id
        )

        print(f"已取消消息 {message_id} 的精华状态")
```

---

## 消息扩展 API

### 1. get_forward_msg - 获取转发消息详情

获取合并转发消息的详细内容。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "转发消息详情示例"

    async def get_forward_example(self, message_id: str):
        # get_forward_msg: 获取转发消息详情
        # 参数说明:
        #   message_id: str - 转发消息的ID（必填）
        # 返回值: Dict，包含转发消息的详细内容

        forward_msg = await self.bot.api.get_forward_msg(
            message_id=message_id
        )

        # forward_msg 包含转发消息的所有子消息
        messages = forward_msg.get("messages", [])
        print(f"转发消息包含 {len(messages)} 条子消息")
```

---

### 2. send_group_forward_msg - 发送群聊合并转发消息

在群里发送合并转发消息。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "群聊转发消息示例"

    @on_message(message_type="group", command="发转发")
    async def handle_send_forward(self, event: MessageEvent):
        # send_group_forward_msg: 发送群聊合并转发消息
        # 参数说明:
        #   group_id: int - 群号（必填）
        #   messages: List[Dict] - 转发消息节点列表（必填）
        # 返回值: Dict，包含 message_id 等信息

        # 构建转发消息节点
        # 每个节点代表转发消息中的一条消息
        messages = [
            {
                "type": "node",
                "data": {
                    "name": "用户A",           # 显示的发送者名称
                    "uin": "123456789",        # 显示的发送者QQ号
                    "content": "这是第一条消息"  # 消息内容
                }
            },
            {
                "type": "node",
                "data": {
                    "name": "用户B",
                    "uin": "987654321",
                    "content": "这是第二条消息"
                }
            },
            {
                "type": "node",
                "data": {
                    "name": "用户C",
                    "uin": "111222333",
                    "content": [  # 也可以使用消息段列表
                        {"type": "text", "data": {"text": "带图片的消息 "}},
                        {"type": "image", "data": {"file": "https://example.com/img.jpg"}}
                    ]
                }
            }
        ]

        await self.bot.api.send_group_forward_msg(
            group_id=event.group_id,
            messages=messages
        )
```

**使用场景举例：**
```python
# 场景: 转发已有消息（使用消息ID）
messages = [
    {
        "type": "node",
        "data": {
            "id": "123456"  # 直接使用已有消息的ID
        }
    },
    {
        "type": "node",
        "data": {
            "id": "789012"
        }
    }
]

await self.bot.api.send_group_forward_msg(
    group_id=123456789,
    messages=messages
)
```

---

### 3. send_private_forward_msg - 发送私聊合并转发消息

向好友发送合并转发消息。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "私聊转发消息示例"

    async def send_private_forward_example(self, user_id: int):
        # send_private_forward_msg: 发送私聊合并转发消息
        # 参数说明:
        #   user_id: int - 目标用户 QQ 号（必填）
        #   messages: List[Dict] - 转发消息节点列表（必填）
        # 返回值: Dict，包含 message_id 等信息

        messages = [
            {
                "type": "node",
                "data": {
                    "name": "系统通知",
                    "uin": "10000",
                    "content": "这是一条系统消息"
                }
            },
            {
                "type": "node",
                "data": {
                    "name": "管理员",
                    "uin": "123456789",
                    "content": "请查收以下信息"
                }
            }
        ]

        await self.bot.api.send_private_forward_msg(
            user_id=user_id,
            messages=messages
        )
```

---

### 4. get_group_msg_history - 获取群历史消息

获取群的历史消息记录。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "群历史消息示例"

    @on_message(message_type="group", command="历史消息")
    async def handle_msg_history(self, event: MessageEvent):
        # get_group_msg_history: 获取群历史消息
        # 参数说明:
        #   group_id: int - 群号（必填）
        #   message_seq: int - 起始消息序号，0 表示从最新开始（可选）
        #   count: int - 获取数量，默认 20（可选）
        #   reverse_order: bool - 是否倒序，默认 False（可选）
        # 返回值: Dict，包含 messages 列表

        history = await self.bot.api.get_group_msg_history(
            group_id=event.group_id,
            message_seq=0,      # 从最新消息开始
            count=10,           # 获取10条
            reverse_order=False # 正序（从旧到新）
        )

        messages = history.get("messages", [])

        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message=f"获取到 {len(messages)} 条历史消息"
        )
```

---

### 5. get_friend_msg_history - 获取好友历史消息

获取与好友的历史消息记录。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "好友历史消息示例"

    async def get_friend_history_example(self, user_id: int):
        # get_friend_msg_history: 获取好友历史消息
        # 参数说明:
        #   user_id: int - 好友 QQ 号（必填）
        #   message_seq: int - 起始消息序号，0 表示从最新开始（可选）
        #   count: int - 获取数量，默认 20（可选）
        # 返回值: Dict，包含 messages 列表

        history = await self.bot.api.get_friend_msg_history(
            user_id=user_id,
            message_seq=0,
            count=20
        )

        messages = history.get("messages", [])
        print(f"获取到 {len(messages)} 条与好友的历史消息")
```

---

### 6. mark_msg_as_read - 标记消息已读

将消息标记为已读状态。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "标记已读示例"

    async def mark_read_example(self, message_id: int):
        # mark_msg_as_read: 标记消息已读
        # 参数说明:
        #   message_id: int - 消息ID（必填）
        # 返回值: Dict（通常为空）

        await self.bot.api.mark_msg_as_read(
            message_id=message_id
        )

        print(f"消息 {message_id} 已标记为已读")
```

---

### 7. set_msg_emoji_like - 表情回应消息

对消息添加表情回应（仅群聊）。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "表情回应示例"

    @on_message(message_type="group", command="点赞消息")
    async def handle_emoji_like(self, event: MessageEvent):
        # set_msg_emoji_like: 表情回应消息
        # 参数说明:
        #   message_id: int - 消息ID（必填）
        #   emoji_id: int - 表情ID（必填）
        # 返回值: Dict（通常为空）
        # 注意: 仅支持群聊消息

        # 常用表情ID:
        # 76 - 赞
        # 63 - 玫瑰
        # 66 - 爱心
        # 124 - OK

        # 获取被回复的消息ID
        reply_id = None
        for seg in event.message:
            if seg.get("type") == "reply":
                reply_id = int(seg["data"]["id"])
                break

        if reply_id:
            await self.bot.api.set_msg_emoji_like(
                message_id=reply_id,
                emoji_id=76  # 点赞表情
            )
```

---

### 8. delete_msg_emoji_like - 删除表情回应

删除对消息的表情回应。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "删除表情回应示例"

    async def delete_emoji_like_example(self, message_id: int, emoji_id: int):
        # delete_msg_emoji_like: 删除表情回应
        # 参数说明:
        #   message_id: int - 消息ID（必填）
        #   emoji_id: int - 表情ID（必填）
        # 返回值: Dict（通常为空）

        await self.bot.api.delete_msg_emoji_like(
            message_id=message_id,
            emoji_id=emoji_id
        )

        print(f"已删除消息 {message_id} 的表情回应")
```

---

## 文件相关 API

### 1. get_file - 获取消息文件详情

获取消息中文件的详细信息。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "获取文件示例"

    async def get_file_example(self, file_id: str):
        # get_file: 获取消息文件详情
        # 参数说明:
        #   file: str - 文件ID（必填）
        #   download: bool - 是否下载文件，默认 True（可选）
        # 返回值: Dict，包含:
        #   - file: str - 文件路径
        #   - file_name: str - 文件名
        #   - file_size: int - 文件大小
        #   - base64: str - 文件的 base64 编码（如果下载）

        file_info = await self.bot.api.get_file(
            file=file_id,
            download=True  # 下载文件
        )

        file_path = file_info.get("file")
        file_name = file_info.get("file_name")
        file_size = file_info.get("file_size", 0)

        print(f"文件名: {file_name}")
        print(f"文件大小: {file_size} 字节")
        print(f"文件路径: {file_path}")
```

---

### 2. get_image - 获取消息图片详情

获取消息中图片的详细信息。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "获取图片示例"

    @on_message(message_type="group")
    async def handle_image(self, event: MessageEvent):
        # get_image: 获取消息图片详情
        # 参数说明:
        #   file: str - 图片文件ID（必填）
        # 返回值: Dict，包含:
        #   - file: str - 图片本地路径
        #   - url: str - 图片URL
        #   - size: int - 图片大小

        # 从消息中提取图片
        for seg in event.message:
            if seg.get("type") == "image":
                file_id = seg["data"].get("file")

                image_info = await self.bot.api.get_image(
                    file=file_id
                )

                url = image_info.get("url")
                size = image_info.get("size", 0)

                print(f"图片URL: {url}")
                print(f"图片大小: {size} 字节")
                break
```

---

### 3. get_record - 获取消息语音详情

获取消息中语音的详细信息。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "获取语音示例"

    async def get_record_example(self, file_id: str):
        # get_record: 获取消息语音详情
        # 参数说明:
        #   file: str - 语音文件ID（必填）
        #   out_format: str - 输出格式，默认 "mp3"（可选）
        # 返回值: Dict，包含:
        #   - file: str - 语音文件路径

        record_info = await self.bot.api.get_record(
            file=file_id,
            out_format="mp3"  # 转换为 mp3 格式
        )

        file_path = record_info.get("file")
        print(f"语音文件路径: {file_path}")
```

---

### 4. download_file - 下载文件到缓存目录

下载网络文件到本地缓存。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "下载文件示例"

    async def download_file_example(self):
        # download_file: 下载文件到缓存目录
        # 参数说明:
        #   url: str - 文件URL（与 base64 二选一）
        #   base64: str - 文件的 base64 编码（与 url 二选一）
        #   name: str - 保存的文件名（可选）
        #   headers: List[str] - 请求头，格式如 ["User-Agent: xxx"]（可选）
        # 返回值: Dict，包含:
        #   - file: str - 下载后的文件路径

        # 方式1: 通过 URL 下载
        result = await self.bot.api.download_file(
            url="https://example.com/file.zip",
            name="downloaded_file.zip"
        )

        file_path = result.get("file")
        print(f"文件已下载到: {file_path}")

        # 方式2: 通过 base64 保存
        import base64
        content = base64.b64encode(b"Hello World").decode()
        result = await self.bot.api.download_file(
            base64=content,
            name="hello.txt"
        )
```

---

## 群文件相关 API

### 1. upload_group_file - 上传群文件

上传文件到群文件。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "上传群文件示例"

    @on_message(message_type="group", command="上传文件")
    async def handle_upload_group_file(self, event: MessageEvent):
        # upload_group_file: 上传群文件
        # 参数说明:
        #   group_id: int - 群号（必填）
        #   file: str - 本地文件路径（必填）
        #   name: str - 上传后的文件名（可选，默认使用原文件名）
        #   folder_id: str - 目标文件夹ID，不填则上传到根目录（可选）
        # 返回值: Dict（通常为空）

        await self.bot.api.upload_group_file(
            group_id=event.group_id,
            file="C:/path/to/file.txt",  # 本地文件路径
            name="上传的文件.txt"          # 自定义文件名
        )

        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message="文件上传成功！"
        )
```

**使用场景举例：**
```python
# 场景: 上传到指定文件夹
await self.bot.api.upload_group_file(
    group_id=123456789,
    file="C:/documents/report.pdf",
    name="月度报告.pdf",
    folder_id="abc123"  # 文件夹ID，从 get_group_root_files 获取
)
```

---

### 2. upload_private_file - 上传私聊文件

向好友发送文件。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "上传私聊文件示例"

    async def upload_private_file_example(self, user_id: int, file_path: str):
        # upload_private_file: 上传私聊文件
        # 参数说明:
        #   user_id: int - 目标用户 QQ 号（必填）
        #   file: str - 本地文件路径（必填）
        #   name: str - 上传后的文件名（可选）
        # 返回值: Dict（通常为空）

        await self.bot.api.upload_private_file(
            user_id=user_id,
            file=file_path,
            name="发送的文件.zip"
        )

        print(f"文件已发送给 {user_id}")
```

---

### 3. get_group_root_files - 获取群根目录文件列表

获取群文件根目录的文件和文件夹列表。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "群文件列表示例"

    @on_message(message_type="group", command="群文件")
    async def handle_group_files(self, event: MessageEvent):
        # get_group_root_files: 获取群根目录文件列表
        # 参数说明:
        #   group_id: int - 群号（必填）
        # 返回值: Dict，包含:
        #   - files: List[Dict] - 文件列表
        #   - folders: List[Dict] - 文件夹列表

        result = await self.bot.api.get_group_root_files(
            group_id=event.group_id
        )

        files = result.get("files", [])
        folders = result.get("folders", [])

        msg = f"群文件统计:\n文件数: {len(files)}\n文件夹数: {len(folders)}"

        # 列出前5个文件
        if files:
            msg += "\n\n最近文件:"
            for f in files[:5]:
                name = f.get("file_name", "未知")
                size = f.get("file_size", 0)
                msg += f"\n- {name} ({size} 字节)"

        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message=msg
        )
```

---

### 4. get_group_files_by_folder - 获取群子目录文件列表

获取群文件指定文件夹内的文件列表。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "群文件夹内容示例"

    async def get_folder_files_example(self, group_id: int, folder_id: str):
        # get_group_files_by_folder: 获取群子目录文件列表
        # 参数说明:
        #   group_id: int - 群号（必填）
        #   folder_id: str - 文件夹ID（必填）
        # 返回值: Dict，包含 files 和 folders 列表

        result = await self.bot.api.get_group_files_by_folder(
            group_id=group_id,
            folder_id=folder_id
        )

        files = result.get("files", [])
        folders = result.get("folders", [])

        print(f"文件夹内有 {len(files)} 个文件，{len(folders)} 个子文件夹")
```

---

### 5. get_group_file_url - 获取群文件资源链接

获取群文件的下载链接。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "群文件链接示例"

    async def get_file_url_example(self, group_id: int, file_id: str):
        # get_group_file_url: 获取群文件资源链接
        # 参数说明:
        #   group_id: int - 群号（必填）
        #   file_id: str - 文件ID（必填，从文件列表获取）
        # 返回值: Dict，包含:
        #   - url: str - 文件下载链接

        result = await self.bot.api.get_group_file_url(
            group_id=group_id,
            file_id=file_id
        )

        url = result.get("url")
        print(f"文件下载链接: {url}")
```

---

### 6. get_group_file_system_info - 获取群文件系统信息

获取群文件系统的容量信息。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "群文件系统信息示例"

    @on_message(message_type="group", command="群文件空间")
    async def handle_file_system_info(self, event: MessageEvent):
        # get_group_file_system_info: 获取群文件系统信息
        # 参数说明:
        #   group_id: int - 群号（必填）
        # 返回值: Dict，包含:
        #   - file_count: int - 文件总数
        #   - limit_count: int - 文件数量上限
        #   - used_space: int - 已用空间（字节）
        #   - total_space: int - 总空间（字节）

        info = await self.bot.api.get_group_file_system_info(
            group_id=event.group_id
        )

        file_count = info.get("file_count", 0)
        limit_count = info.get("limit_count", 0)
        used_space = info.get("used_space", 0)
        total_space = info.get("total_space", 0)

        # 转换为 MB
        used_mb = used_space / 1024 / 1024
        total_mb = total_space / 1024 / 1024

        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message=f"群文件空间:\n文件数: {file_count}/{limit_count}\n已用: {used_mb:.2f}MB / {total_mb:.2f}MB"
        )
```

---

### 7. delete_group_file - 删除群文件

删除群文件。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "删除群文件示例"

    async def delete_file_example(self, group_id: int, file_id: str):
        # delete_group_file: 删除群文件
        # 参数说明:
        #   group_id: int - 群号（必填）
        #   file_id: str - 文件ID（必填）
        # 返回值: Dict（通常为空）
        # 注意: 需要管理员权限或是文件上传者

        await self.bot.api.delete_group_file(
            group_id=group_id,
            file_id=file_id
        )

        print(f"文件 {file_id} 已删除")
```

---

### 8. create_group_file_folder - 创建群文件夹

在群文件中创建新文件夹。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "创建群文件夹示例"

    async def create_folder_example(self, group_id: int, folder_name: str):
        # create_group_file_folder: 创建群文件夹
        # 参数说明:
        #   group_id: int - 群号（必填）
        #   folder_name: str - 文件夹名称（必填）
        # 返回值: Dict（通常为空）

        await self.bot.api.create_group_file_folder(
            group_id=group_id,
            folder_name=folder_name
        )

        print(f"文件夹 '{folder_name}' 创建成功")
```

---

### 9. delete_group_folder - 删除群文件夹

删除群文件中的文件夹。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "删除群文件夹示例"

    async def delete_folder_example(self, group_id: int, folder_id: str):
        # delete_group_folder: 删除群文件夹
        # 参数说明:
        #   group_id: int - 群号（必填）
        #   folder_id: str - 文件夹ID（必填）
        # 返回值: Dict（通常为空）
        # 注意: 文件夹必须为空才能删除

        await self.bot.api.delete_group_folder(
            group_id=group_id,
            folder_id=folder_id
        )

        print(f"文件夹 {folder_id} 已删除")
```

---

### 10. rename_group_folder - 重命名群文件夹

重命名群文件中的文件夹。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "重命名群文件夹示例"

    async def rename_folder_example(self, group_id: int, folder_id: str, new_name: str):
        # rename_group_folder: 重命名群文件夹
        # 参数说明:
        #   group_id: int - 群号（必填）
        #   folder_id: str - 文件夹ID（必填）
        #   new_folder_name: str - 新的文件夹名称（必填）
        # 返回值: Dict（通常为空）

        await self.bot.api.rename_group_folder(
            group_id=group_id,
            folder_id=folder_id,
            new_folder_name=new_name
        )

        print(f"文件夹已重命名为: {new_name}")
```

---

## 系统相关 API

### 1. get_version_info - 获取版本信息

获取 OneBot 实现的版本信息。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "版本信息示例"

    @on_message(message_type="group", command="版本")
    async def handle_version(self, event: MessageEvent):
        # get_version_info: 获取版本信息
        # 参数: 无
        # 返回值: Dict，包含:
        #   - app_name: str - 应用名称
        #   - app_version: str - 应用版本
        #   - protocol_version: str - OneBot 协议版本

        info = await self.bot.api.get_version_info()

        app_name = info.get("app_name", "未知")
        app_version = info.get("app_version", "未知")

        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message=f"OneBot 实现: {app_name}\n版本: {app_version}"
        )
```

---

### 2. get_status - 获取 Bot 状态

获取机器人的运行状态。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "状态示例"

    @on_message(message_type="group", command="状态")
    async def handle_status(self, event: MessageEvent):
        # get_status: 获取 Bot 状态
        # 参数: 无
        # 返回值: Dict，包含:
        #   - online: bool - 是否在线
        #   - good: bool - 状态是否正常

        status = await self.bot.api.get_status()

        online = status.get("online", False)
        good = status.get("good", False)

        online_text = "在线" if online else "离线"
        status_text = "正常" if good else "异常"

        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message=f"机器人状态:\n在线状态: {online_text}\n运行状态: {status_text}"
        )
```

---

### 3. clean_cache - 清理缓存

清理 OneBot 实现的缓存。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "清理缓存示例"

    @on_message(message_type="private", command="清理缓存")
    async def handle_clean_cache(self, event: MessageEvent):
        # clean_cache: 清理缓存
        # 参数: 无
        # 返回值: Dict（通常为空）

        await self.bot.api.clean_cache()

        await self.bot.api.send_private_msg(
            user_id=event.user_id,
            message="缓存已清理"
        )
```

---

### 4. set_restart - 重启 OneBot 实现

重启 OneBot 服务。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "重启示例"

    async def restart_example(self):
        # set_restart: 重启 OneBot 实现
        # 参数说明:
        #   delay: int - 延迟重启的毫秒数，默认 0（可选）
        # 返回值: Dict（通常为空）
        # 警告: 此操作会导致机器人暂时离线

        await self.bot.api.set_restart(
            delay=3000  # 3秒后重启
        )

        print("OneBot 将在 3 秒后重启")
```

---

### 5. set_online_status - 设置在线状态

设置机器人的在线状态。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "在线状态示例"

    @on_message(message_type="private", command="设状态")
    async def handle_set_status(self, event: MessageEvent):
        # set_online_status: 设置在线状态
        # 参数说明:
        #   status: int - 状态码（必填）
        #     10 = 在线
        #     30 = 离开
        #     40 = 隐身
        #     50 = 忙碌
        #     60 = Q我吧
        #     70 = 请勿打扰
        #   ext_status: int - 扩展状态，默认 0（可选）
        #   battery_status: int - 电量状态，默认 0（可选）
        # 返回值: Dict（通常为空）

        # 设置为忙碌状态
        await self.bot.api.set_online_status(
            status=50  # 忙碌
        )

        await self.bot.api.send_private_msg(
            user_id=event.user_id,
            message="已设置为忙碌状态"
        )
```

**状态码对照表：**
```python
# 在线状态码
STATUS_ONLINE = 10      # 在线
STATUS_AWAY = 30        # 离开
STATUS_INVISIBLE = 40   # 隐身
STATUS_BUSY = 50        # 忙碌
STATUS_QME = 60         # Q我吧
STATUS_DND = 70         # 请勿打扰
```

---

### 6. get_cookies - 获取 Cookies

获取 QQ 相关的 Cookies。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "Cookies示例"

    async def get_cookies_example(self):
        # get_cookies: 获取 Cookies
        # 参数说明:
        #   domain: str - 域名，默认空（可选）
        # 返回值: Dict，包含:
        #   - cookies: str - Cookies 字符串

        cookies = await self.bot.api.get_cookies(
            domain="qun.qq.com"  # 指定域名
        )

        cookie_str = cookies.get("cookies", "")
        print(f"Cookies: {cookie_str}")
```

---

## 其他 API

### 1. ocr_image - 图片 OCR

识别图片中的文字。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "OCR示例"

    @on_message(message_type="group", command="识别文字")
    async def handle_ocr(self, event: MessageEvent):
        # ocr_image: 图片 OCR
        # 参数说明:
        #   image: str - 图片，支持 http://, file://, base64://（必填）
        # 返回值: Dict，包含:
        #   - texts: List[Dict] - 识别结果列表
        #   - language: str - 识别的语言

        # 从消息中获取图片
        image_url = None
        for seg in event.message:
            if seg.get("type") == "image":
                image_url = seg["data"].get("url")
                break

        if image_url:
            result = await self.bot.api.ocr_image(
                image=image_url
            )

            texts = result.get("texts", [])

            if texts:
                # 合并所有识别的文字
                all_text = "\n".join([t.get("text", "") for t in texts])
                await self.bot.api.send_group_msg(
                    group_id=event.group_id,
                    message=f"识别结果:\n{all_text}"
                )
            else:
                await self.bot.api.send_group_msg(
                    group_id=event.group_id,
                    message="未识别到文字"
                )
```

---

### 2. send_group_sign - 群打卡

在群里进行打卡。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "群打卡示例"

    @on_message(message_type="group", command="打卡")
    async def handle_sign(self, event: MessageEvent):
        # send_group_sign: 群打卡
        # 参数说明:
        #   group_id: int - 群号（必填）
        # 返回值: Dict（通常为空）

        await self.bot.api.send_group_sign(
            group_id=event.group_id
        )

        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message="打卡成功！"
        )
```

---

### 3. set_qq_avatar - 设置 QQ 头像

设置机器人的 QQ 头像。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "设置头像示例"

    async def set_avatar_example(self, image_path: str):
        # set_qq_avatar: 设置 QQ 头像
        # 参数说明:
        #   file: str - 图片，支持 http://, file://, base64://（必填）
        # 返回值: Dict（通常为空）

        await self.bot.api.set_qq_avatar(
            file=image_path  # 例如: "file:///C:/avatar.jpg"
        )

        print("头像设置成功")
```

---

### 4. get_avatar - 获取头像

获取用户或群的头像。

```python
from core import Plugin, on_message, MessageEvent

class MyPlugin(Plugin):
    name = "获取头像示例"

    @on_message(message_type="group", command="我的头像")
    async def handle_get_avatar(self, event: MessageEvent):
        # get_avatar: 获取头像
        # 参数说明:
        #   user_id: int - 用户 QQ 号（与 group_id 二选一）
        #   group_id: int - 群号（与 user_id 二选一）
        #   size: int - 头像尺寸，默认 640（可选）
        # 返回值: Dict，包含:
        #   - url: str - 头像URL

        # 获取用户头像
        result = await self.bot.api.get_avatar(
            user_id=event.user_id,
            size=640  # 640x640 像素
        )

        avatar_url = result.get("url")

        # 发送头像图片
        await self.bot.api.send_group_msg(
            group_id=event.group_id,
            message=[
                {"type": "text", "data": {"text": "你的头像:\n"}},
                {"type": "image", "data": {"file": avatar_url}}
            ]
        )
```

**使用场景举例：**
```python
# 场景1: 获取群头像
result = await self.bot.api.get_avatar(
    group_id=123456789,
    size=640
)
group_avatar = result.get("url")

# 场景2: 获取小尺寸头像（节省流量）
result = await self.bot.api.get_avatar(
    user_id=123456789,
    size=100  # 100x100 像素
)
```

---

## 附录：消息段类型参考

在发送消息时，可以使用以下消息段类型：

```python
# 文本消息
{"type": "text", "data": {"text": "文本内容"}}

# @某人
{"type": "at", "data": {"qq": "123456789"}}  # @指定用户
{"type": "at", "data": {"qq": "all"}}        # @全体成员

# 图片
{"type": "image", "data": {"file": "http://example.com/img.jpg"}}  # URL
{"type": "image", "data": {"file": "file:///C:/img.jpg"}}          # 本地文件
{"type": "image", "data": {"file": "base64://..."}}                # Base64

# QQ 表情
{"type": "face", "data": {"id": "1"}}  # 表情ID

# 回复
{"type": "reply", "data": {"id": "消息ID"}}

# 语音
{"type": "record", "data": {"file": "http://example.com/audio.mp3"}}

# 视频
{"type": "video", "data": {"file": "http://example.com/video.mp4"}}

# 链接分享
{"type": "share", "data": {
    "url": "https://example.com",
    "title": "标题",
    "content": "描述",
    "image": "https://example.com/img.jpg"
}}

# JSON 消息（卡片消息）
{"type": "json", "data": {"data": "{\"app\":\"...\"}"}}
```

---

## 附录：常见问题

### Q1: API 调用返回空字典怎么办？

API 调用失败时会返回空字典 `{}`。可以通过检查返回值判断是否成功：

```python
result = await self.bot.api.send_group_msg(group_id=123, message="test")
if result:
    print(f"发送成功，消息ID: {result.get('message_id')}")
else:
    print("发送失败")
```

### Q2: 如何处理权限不足的情况？

某些 API 需要管理员或群主权限，调用前可以先检查权限：

```python
# 获取机器人在群里的信息
bot_info = await self.bot.api.get_login_info()
bot_id = bot_info.get("user_id")

member_info = await self.bot.api.get_group_member_info(
    group_id=event.group_id,
    user_id=bot_id
)

role = member_info.get("role")
if role in ["owner", "admin"]:
    # 有权限，执行操作
    await self.bot.api.set_group_ban(...)
else:
    await self.bot.api.send_group_msg(
        group_id=event.group_id,
        message="机器人权限不足，无法执行此操作"
    )
```

### Q3: 如何发送复杂的消息？

使用消息段列表组合多种类型的内容：

```python
message = [
    {"type": "reply", "data": {"id": str(event.message_id)}},  # 回复
    {"type": "at", "data": {"qq": str(event.user_id)}},        # @发送者
    {"type": "text", "data": {"text": " 你好！\n"}},           # 文本
    {"type": "image", "data": {"file": "https://example.com/img.jpg"}},  # 图片
    {"type": "face", "data": {"id": "1"}}                      # 表情
]

await self.bot.api.send_group_msg(
    group_id=event.group_id,
    message=message
)
```

---

## 附录：插件目录结构

每个插件是 `plugins/` 目录下的一个文件夹，推荐的目录结构如下：

```
plugins/
├── my_plugin/              # 插件目录
│   ├── __init__.py         # 插件主文件（必需）
│   ├── data/               # 数据目录（可选）
│   └── ui/                 # UI 目录（可选）
│       └── index.html      # 插件配置界面
└── _disabled_plugin/       # 以 _ 开头的目录会被忽略
```

### 插件 UI 配置界面

插件可以提供一个 HTML 配置界面，放置在 `ui/index.html`。用户可以通过插件管理页面的"打开UI"按钮在浏览器中打开此界面。

**创建步骤：**
1. 在插件目录下创建 `ui` 文件夹
2. 在 `ui` 文件夹中创建 `index.html` 文件
3. 编写 HTML/CSS/JavaScript 实现配置界面
4. 在插件管理页面点击"打开UI"按钮即可在浏览器中打开

**UI 文件用途：**
- 提供可视化的插件配置界面
- 让用户无需修改代码即可调整插件参数
- 支持保存配置到 localStorage 或发送到后端

**简单示例：**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>插件设置</title>
    <style>
        body { font-family: sans-serif; padding: 20px; max-width: 600px; margin: 0 auto; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
        .form-group input, .form-group textarea { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
        .btn { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        .btn:hover { background: #0056b3; }
    </style>
</head>
<body>
    <h1>插件设置</h1>

    <div class="form-group">
        <label>触发关键词（多个用逗号分隔）</label>
        <input type="text" id="keywords" placeholder="你好,hello,hi">
    </div>

    <div class="form-group">
        <label>回复消息模板</label>
        <textarea id="reply_template" rows="3" placeholder="你好 {nickname}！"></textarea>
    </div>

    <div class="form-group">
        <label>冷却时间（秒）</label>
        <input type="number" id="cooldown" value="5" min="0">
    </div>

    <button class="btn" onclick="saveConfig()">保存设置</button>

    <script>
        // 插件名称，用于 localStorage 键名前缀
        const PLUGIN_NAME = 'my_plugin';

        // 保存配置
        function saveConfig() {
            const config = {
                keywords: document.getElementById('keywords').value,
                reply_template: document.getElementById('reply_template').value,
                cooldown: document.getElementById('cooldown').value
            };

            // 保存到 localStorage
            localStorage.setItem(PLUGIN_NAME + '_config', JSON.stringify(config));
            alert('设置已保存！');
        }

        // 页面加载时读取配置
        window.onload = function() {
            const saved = localStorage.getItem(PLUGIN_NAME + '_config');
            if (saved) {
                const config = JSON.parse(saved);
                document.getElementById('keywords').value = config.keywords || '';
                document.getElementById('reply_template').value = config.reply_template || '';
                document.getElementById('cooldown').value = config.cooldown || 5;
            }
        }
    </script>
</body>
</html>
```

**注意事项：**
- UI 文件是纯前端 HTML，运行在浏览器中
- 配置数据默认保存在浏览器的 localStorage 中
- 如需与插件后端通信，可以通过 HTTP API 实现
- 点击"添加Demo插件"按钮会自动创建包含完整 UI 模板的示例插件

### 插件管理界面功能

在桌面 UI 的插件管理页面中，每个插件提供以下功能：

- **启用/禁用**: 控制插件是否运行
- **打开目录**: 在文件管理器中打开插件所在目录
- **打开UI**: 在浏览器中打开插件的 `ui/index.html` 配置界面（如果存在）

点击"添加Demo插件"按钮可以快速创建一个包含完整示例代码的演示插件，包括：
- 完整的 `__init__.py` 示例代码
- `data/` 数据目录
- `ui/index.html` 配置界面模板

---

*文档完成。如有问题，请参考 OneBot11 协议文档或 LLOneBot 官方文档。*

