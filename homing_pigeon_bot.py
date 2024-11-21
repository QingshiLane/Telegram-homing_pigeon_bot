from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
import datetime
import asyncio,sys
# 此处替换为你的机器人Token
TOKEN = 'TOKEN'
# 此处替换为你的用户ID
YOUR_USER_ID = 0

# Dictionary to store the mapping between message_id and the original sender's user_id
message_sender_map = {}
# Dictionary to store the mapping between user_id and username
usernames = {}
fullnames = {}
# Set to store banned user IDs
banned_users = set()
# List to keep track of recent chatters
recent_chatters = []

user_last_interaction = {}
user_timers = {}

if_private = False
privater_id = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("您好，我是传话的，有啥说的尽管说！")

async def relay_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "Unknown"
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    fullname = f"{first_name} {last_name}" if last_name else first_name
    print("# xinxiaoxi )")
    if user_id != YOUR_USER_ID:
        # Add to recent chatters
        if user_id not in recent_chatters:
            if len(recent_chatters) >= 4:
                recent_chatters.pop(0)
            recent_chatters.append(user_id)
        
        # Store the username
        usernames[user_id] = username
        fullnames[user_id] = fullname
        
        # Check if the user is banned
        if user_id not in banned_users:
            # Forward message to you and save mapping
            sent_message = await context.bot.forward_message(chat_id=YOUR_USER_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
            message_sender_map[sent_message.message_id] = user_id
        else:
            await update.message.reply_text("你被禁止发送消息")
    elif user_id == YOUR_USER_ID:
        if if_private:
            user_last_interaction[user_id] = datetime.datetime.now()
            if user_id in user_timers:
                user_timers[user_id].cancel()
            print("# 设置一个新的定时器任务)")
            user_timers[user_id] = asyncio.create_task(check_inactivity(user_id, context))
            
        # This is your reply to a forwarded message
        if update.message.reply_to_message:
            original_message_id = update.message.reply_to_message.message_id
            original_sender_id = message_sender_map.get(original_message_id)
            if original_sender_id:
                message = update.message
                if message.text:
                    # 处理文本信息
                    await context.bot.send_message(chat_id=original_sender_id, text=message.text)
                elif message.photo:
                    # 处理图片信息
                    await context.bot.send_photo(chat_id=original_sender_id, photo=message.photo[-1].file_id)
                elif message.video:
                    # 处理视频信息
                    await context.bot.send_video(chat_id=original_sender_id, video=message.video.file_id)
                elif message.voice:
                    # 处理语音信息
                    await context.bot.send_voice(chat_id=original_sender_id, voice=message.voice.file_id)
                elif message.audio:
                    # 处理音频信息
                    await context.bot.send_audio(chat_id=original_sender_id, audio=message.audio.file_id)
                elif message.document:
                    # 处理文件信息
                    await context.bot.send_document(chat_id=original_sender_id, document=message.document.file_id)
                # await context.bot.send_message(chat_id=original_sender_id, text=update.message.text, photo=update.message.photo[-1].file_id, video=update.message.video.file_id)
            else:
                await update.message.reply_text("无法识别原始发送者，无法发送消息")
        else:
            if if_private:
                message = update.message
                if message.text:
                    # 处理文本信息
                    await context.bot.send_message(chat_id=privater_id, text=message.text)
                elif message.photo:
                    # 处理图片信息
                    await context.bot.send_photo(chat_id=privater_id, photo=message.photo[-1].file_id)
                elif message.video:
                    # 处理视频信息
                    await context.bot.send_video(chat_id=privater_id, video=message.video.file_id)
                elif message.voice:
                    # 处理语音信息
                    await context.bot.send_voice(chat_id=privater_id, voice=message.voice.file_id)
                elif message.audio:
                    # 处理音频信息
                    await context.bot.send_audio(chat_id=privater_id, audio=message.audio.file_id)
                elif message.document:
                    # 处理文件信息
                    await context.bot.send_document(chat_id=privater_id, document=message.document.file_id)
                # await context.bot.send_message(chat_id=privater_id, text=update.message.text)
            else:
                await update.message.reply_text("非1v1，您发送的信息仅存在此窗口")

async def check_inactivity(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> None:
    await asyncio.sleep(180)  # 3分钟 = 180秒
    
    # 检查用户是否仍然没有互动
    last_interaction = user_last_interaction.get(user_id)
    if last_interaction and (datetime.datetime.now() - last_interaction).total_seconds() >= 180:
        
        global if_private
        if if_private:
            if_private=False
            global privater_id
            privater_id=0
            await context.bot.send_message(chat_id=user_id, text=f"你已经3分钟未对话，退出1v1")


async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == YOUR_USER_ID:
        keyboard = [
            [InlineKeyboardButton(f"禁言🚫{fullnames.get(recent_chatters[i])}@{usernames.get(recent_chatters[i], 'Unknown')}", callback_data=f"ban_{recent_chatters[i]}")]
            for i in range(min(len(recent_chatters), 4))
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("选择要禁止的聊天者", reply_markup=reply_markup)
    else:
        await update.message.reply_text("您无权进行此操作，您只能向我发消息")

async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == YOUR_USER_ID:
        keyboard = [
            [InlineKeyboardButton(f"解除禁言🔊{fullnames.get(banned_user)}@{usernames.get(banned_user, 'Unknown')}", callback_data=f"unban_{banned_user}")]
            for banned_user in banned_users
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("选择要解除禁止的聊天者", reply_markup=reply_markup)
    else:
        await update.message.reply_text("您无权进行此操作，您只能向我发消息")

async def enter_private_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == YOUR_USER_ID:
        keyboard = [
            [InlineKeyboardButton(f"1v1💬{fullnames.get(recent_chatters[i])}@{usernames.get(recent_chatters[i], 'Unknown')}", callback_data=f"enterprivatechat_{recent_chatters[i]}")]
            for i in range(min(len(recent_chatters), 4))
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("选择要1v1的聊天者", reply_markup=reply_markup)
    else:
        await update.message.reply_text("您无权进行此操作，您只能向我发消息")

async def exit_private_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == YOUR_USER_ID:
        global if_private
        if if_private:
            if_private=False
            global privater_id
            privater_id=0
            await update.message.reply_text("您已退出1v1模式")
        else:
            await update.message.reply_text("您已处于非1v1模式，无需重复操作")
    else:
        await update.message.reply_text("您无权进行此操作，您只能向我发消息")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    
    if data.startswith("ban_"):
        user_id = int(data.split("_")[1])
        banned_users.add(user_id)
        await query.answer(text=f"已禁止用户 {fullnames.get(user_id)}@{usernames.get(user_id, 'Unknown')}.")
    elif data.startswith("unban_"):
        user_id = int(data.split("_")[1])
        banned_users.discard(user_id)
        await query.answer(text=f"已解除对用户 {fullnames.get(user_id)}@{usernames.get(user_id, 'Unknown')} 的禁止")
    elif data.startswith("enterprivatechat_"):
        global if_private
        if_private=True
        user_id = int(data.split("_")[1])
        global privater_id
        privater_id=user_id
        await query.answer(text=f"已进入和用户 {fullnames.get(user_id)}@{usernames.get(user_id, 'Unknown')} 的1v1模式")

if __name__ == '__main__':
    args = sys.argv
    TOKEN=args[1]
    YOUR_USER_ID=int(args[2])
    print("1")
    app = ApplicationBuilder().token(TOKEN).build()

    # Command handler to start the bot
    app.add_handler(CommandHandler('start', start))
    print("2")
    
    # Command handlers for ban and unban
    app.add_handler(CommandHandler('ban', ban))
    app.add_handler(CommandHandler('unban', unban))
    print("3")

    # Command handlers for enter_1v1 and exit_1v1
    app.add_handler(CommandHandler('enter_1v1', enter_private_chat))
    app.add_handler(CommandHandler('exit_1v1', exit_private_chat))
    print("4")
    
    # Message handler to relay all types of messages
    app.add_handler(MessageHandler(~filters.COMMAND, relay_message))
    # app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, relay_message))
    print("5")
    
    # Callback query handler for inline buttons
    app.add_handler(CallbackQueryHandler(button))
    print("6")
    
    # Run the bot
    app.run_polling()
    print("7")
