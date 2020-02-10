import telebot
import config
from pydub import AudioSegment
from io import BytesIO
import os
from DBRepository import DBRepository

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

    db = DBRepository()
    # check user in db
    if (db.find_user_by_uid(user_id)):
        # if user exist check last num of his voice and add new
        num_audio = db.count_voice_rows_by_id(user_id) + 1
    else:
        num_audio = 0
        # if user not exist add new user on db
        db.save_new_user((user_id, user_name))
        os.mkdir(os.path.join(config.data_path, str(user_id)))

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
    voice_out_path = os.path.join(str(user_id)
                                  , 'audio_message_{}.wav'.format(num_audio))
    voice_file.export(os.path.join(config.data_path, voice_out_path),
                      format='wav',
                      tags={'uid': '{}'.format(user_id),
                            'username': '{}'.format(user_name)})
    # save voice info to db
    db.save_voice((voice_out_path, user_id))

    db.close()


if __name__ == '__main__':
    bot.polling(none_stop=True)
