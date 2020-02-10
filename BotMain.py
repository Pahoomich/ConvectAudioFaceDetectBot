import telebot
import config
from pydub import AudioSegment
from io import BytesIO

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start', 'help'])
def start_massege(message):
    if message.text.lower() == '/start':
        bot.send_message(message.chat.id, 'Привет, мой пользователь')
    elif message.text.lower() == '/help':
        bot.send_message(message.chat.id,
                         'Я умею следующее: \n 1. Сохранять аудиосообщения \n 2. Конвектировать аудио \n 3. Искать лица на фото')


@bot.message_handler(content_types=['voice'])
def audio_message_save(massage):
    user_id = massage.from_user.id
    user_name = massage.from_user.username
    num_audio = 0

    # get voice msg id and info
    voice_id = massage.voice.file_id
    voice_file_info = bot.get_file(voice_id)
    # download voice by bytes
    download_file = bot.download_file(voice_file_info.file_path)
    # read bytes
    voice_bytes = BytesIO(download_file)
    # create audiosegment and change frame to 16000
    voice_file = AudioSegment.from_file(voice_bytes).set_frame_rate(16000)
    # save voice massage in wav format file
    voice_file.export('{}_message_{}.wav'.format(user_id, num_audio),
                      format='wav',
                      tags={'uid': '{}'.format(user_id),
                            'username': '{}'.format(user_name)})

    # we have the file in bytes and we can save its to disk
    # with open('{}_{}.oga'.format(user_id, num_audio), 'wb') as new_voice_file:
    #     new_voice_file.write(download_file)


if __name__ == '__main__':
    bot.polling(none_stop=True)
