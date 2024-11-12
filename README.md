## Telegram-私信机器人
Telegram私聊机器人，用于信息的接收、发送、管理、禁止等

### 一、创建TG机器人，获取机器人`Token`，并设置机器人命令描述
#### 1.打开Telegram搜索[@BotFather](https://t.me/BotFather)，或点击直达

![image](https://github.com/user-attachments/assets/c38accac-011d-4f78-9e54-c9e256493c14) 

⚠️带认证且用户名为[@BotFather](https://t.me/BotFather)，主页描述如下图，不要搞错了

![image](https://github.com/user-attachments/assets/f4fb358d-8449-4a05-aa70-be5c9b639d8d)

#### 2.创建一个私聊机器人，并获取机器人`Token`

1）进入机器人输入命令`/newbot`或者选择菜单命令`/newbot`

2）输入机器人名称（名称即昵称，随便填，可以和任何人相同、重复，不唯一）

3）输入机器人的用户名（用户名唯一标识，必须以`“大写字母开头Bot结尾”`或者`“小写字母开头_bot结尾”`两种格式二选一。图中作者以`test_bot`为用户名提示被占用创建不了机器人，所以为了演示就随便起了一个用户名`scxsd_bot`。为防止带来误解特此说明）

4）获得机器人`TOKEN`，备用ℹ️ℹ️ℹ️

![image](https://github.com/user-attachments/assets/3f04b164-7bea-4697-85a6-8a003820e34e)

#### 3.设置机器人命令及描述

1）输入`/mybots`，点击刚刚创建的机器人

![image](https://github.com/user-attachments/assets/65a9a6ca-ea76-47a2-bb08-ba3c3d50c487)

2）点击编辑机器人

![image](https://github.com/user-attachments/assets/4c4e663b-e3ed-4eb8-b1fa-7919375dad78)

3）点击编辑命令

![image](https://github.com/user-attachments/assets/27db7230-038c-419d-b54f-f377015eb1f0)

4）输入以下指令及描述，机器人配置完毕
```
ban - 禁言
unban - 解除禁言
enter_1v1 - 进入1v1
exit_1v1 - 退出1v1
```
![image](https://github.com/user-attachments/assets/503c2aa9-d5ca-4621-bb07-b1f873df2f90)

### 二、获取个人用户ID
1.打开Telegram搜索[@KinhRoBot](https://t.me/KinhRoBot)，或点击直达

![image](https://github.com/user-attachments/assets/d86ff2b6-d308-4cf6-8859-07545043f3be)

2.输入`/id`命令，得到个人`用户ID`，备用ℹ️ℹ️ℹ️

![image](https://github.com/user-attachments/assets/2f9727be-2e0e-44eb-912d-81951ca4a797)

### 三、服务器部署
1.安装依赖
```
pip install python-telegram-bot
```
2.复制粘贴以下命令终端执行，下载并赋予脚本权限
```
git clone https://github.com/QingshiLane/Telegram-homing_pigeon_bot.git
cd Telegram-homing_pigeon_bot
chmod +x ./tg_bot_start.sh ./tg_bot_stop.sh
```
3.复制下列命令，修改其中TOKEN和YOUR_USER_ID的值，将机器人的`Token`填入脚本`" "`中（注意将值填入双引号中，保留双引号）。你的`用户ID`同理。终端执行
```python
#修改脚本中TOKEN和YOUR_USER_ID的值，将机器人的Token填入脚本" "中（注意将值填入双引号中，保留双引号）。你的用户ID同理
sed -i '' 's/^TOKEN=.*/TOKEN="机器人的Token"/; s/^YOUR_USER_ID=.*/YOUR_USER_ID="你的用户ID"/' tg_bot_start.sh tg_bot_stop.sh
```
4.终端输入下面命令执行启动脚本，机器人部署完毕，并且开始运行，可以去tg尝试ok不ok。
```
./tg_bot_start.sh
```
*特别说明*：该脚本实现后台启动一个进程执行机器人程序。每次执行会检查机器人程序进程是否已经存在，没有存在则执行脚本启动机器人，若已经存在则中断脚本运行。起到保活作用。

⚠️⚠️⚠️该脚本可以结合青龙面板或者其他定时方法对进程进行保活⚠️⚠️⚠️

5.若要停止机器人的话，终端进入该项目的目录，执行以下终止脚本
```
./tg_bot_stop.sh
```

### 四、使用说明
其他人私聊该机器人，机器人将把信息转发给你，同样你可以通过`回复`机器人转发的信息，给来信者回信。

若嫌回复麻烦，可进入`1v1`模式，即选择一个目标，你`直接`发给机器的信息即可，`无需回复操作`，机器人将直接把你的信息发给你选择的目标。
