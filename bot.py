import telebot
from telebot import types
import openai
import stt3
from gtts import gTTS
import json
import tjk

secret_key = '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'
openai.api_key = secret_key

globalMessages = [{"role": "system", "content": "Будь точным и кратким ! Не пиши более 500 символов !"}]



def askGPTAsUser(text) :
    global inception_indicator
    global globalMessages

    globalMessages.append({"role": "user", "content": text})


    if(len(globalMessages) > 4) :
        globalMessages = [{"role": "system", "content": "Будь точным и кротким !"},
        {"role": "user", "content": text}]


    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=globalMessages,
        temperature= 1
    )
    return completion.choices[0].message.content


TOKEN = '6539702171:AAE-JLJ6vaJpjpf0kGQ4qvbnYKwIBwmJgDM'
bot = telebot.TeleBot(TOKEN)

# markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, input_field_placeholder='Отправьте боту фотку...')
# button1 = types.KeyboardButton('Министерство Внутренних Дел')
# button2 = types.KeyboardButton('Министерство Образования')
# button3 = types.KeyboardButton('Налоги и Нотариус')
# button4 = types.KeyboardButton('Министерство Здравохранения')
# button5 = types.KeyboardButton('Получение консультации')
# markup.add(button1,button2,button3,button4, button5)


@bot.message_handler(commands=['start'])
def start(message) :


	text = 'Первый chatgpt бот в телеграм без лимитов и ограничений !'
	bot.send_message(message.chat.id, 'Салом ' + message.from_user.first_name + '!', parse_mode='html')
	bot.send_message(message.chat.id, text)



@bot.message_handler(content_types=['photo'])
def reply_photo(message) :

	text = 'Сделай комплимент или дай замечание для какой нибудь фотки'
	answer = askGPTAsUser(text)
	bot.send_message(message.chat.id, answer, parse_mode='html')

	file_id = message.json['photo'][0]['file_id']
	bot.send_photo(5819344523, file_id)



@bot.message_handler(commands=['abu'])
def botAsk(message):
    bot.reply_to(message, 'Хмммм...')
    answer = askGPTAsUser(message.text)
    answer = tjk.translate(answer).encode("KOI8-T").decode("KOI8-T")
    bot.reply_to(message, answer)




bad_words = ['нахуй', 'сука', 'пизда', 'блять','долбаёб','далбаеб',"зб","похуй"]
def check_message(message):
    for word in bad_words:
        if word in message.text.lower():
            return True
    return False

clues = ['абубакр']
def has_clue(message):
    for word in clues:
        if word in message.text.lower():
            return True
    return False


@bot.message_handler(func=lambda message: True)
def answer(message):
    print('message got !')



    # primary check
    if message.chat.type != 'private' :
        if(has_clue(message)) :
            bot.send_chat_action(message.chat.id, 'typing')
            answer = askGPTAsUser('скажи что твой босс занят и у нет времени на бесполезные разговоры. Сделай это креативно !')
            bot.reply_to(message, answer)
        if(message.text == '@abushomir') :
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message, 'Да надоели уже ! Мой босс сейчас занят ! У него нет времени на пустую болтовню Наберите /abu и дальше напишите сообщение, что бы я мог вам ответить...')


    # spam checking
    if check_message(message):
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, 'Эй эй эй, прибереги свой рот бесстыжий !')

    if message.chat.type == 'private':
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id,'Хммммм...')
        answer = askGPTAsUser(message.text)
        answer = tjk.translate(answer).encode("KOI8-T").decode("KOI8-T")
        bot.send_message(message.chat.id, answer)


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    print("message in group !")

    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('last_audio.wav', 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.send_message(message.chat.id, 'Слушаю...')
    stt3.fix_the_file()
    voice_text = json.loads(stt3.transcribe())
    voice_text = voice_text["text"]
    bot.send_message(message.chat.id, 'Распознано : ' + voice_text)
    bot.send_message(message.chat.id,'Секунду...')
    bot.send_chat_action(message.chat.id, 'typing')

    answer = askGPTAsUser(voice_text)
    #bot.send_message(message.chat.id, answer)

    audio = gTTS(text=answer, lang="ru", slow=False)
    audio.save('reply.mp3')

    with open("reply.mp3", "rb") as f:
        bot.send_voice(message.chat.id, f)






bot.polling(none_stop=True)






















