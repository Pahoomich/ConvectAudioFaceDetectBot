import telebot
import config
from pydub import AudioSegment
from io import BytesIO
import os
from DBRepository import DBRepository
import numpy as np
import cv2

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start', 'help'])
def start_massege(message):
    if message.text.lower() == '/start':
        bot.send_message(message.chat.id, 'Привет, мой пользователь')
    elif message.text.lower() == '/help':
        bot.send_message(message.chat.id,
                         'Я умею следующее: \n 1. Сохранять аудиосообщения \n 2. Конвектировать аудио \n 3. Искать лица на фото')


@bot.message_handler(content_types=['voice'])
def audio_message_save(message):
    voice_messages_path = os.path.join(config.data_path, 'voice_messages')
    user_id = message.from_user.id
    user_name = message.from_user.username

    db = DBRepository()
    # check user in db
    if (db.find_user_by_uid(user_id)):
        # if user exist check last num of his voice and add new
        num_audio = db.count_voice_rows_by_id(user_id)
    else:
        num_audio = 0
        # if user not exist add new user on db
        db.save_new_user((user_id, user_name))
        os.mkdir(os.path.join(voice_messages_path, str(user_id)))

    # get voice msg id and info
    voice_id = message.voice.file_id
    voice_file_info = bot.get_file(voice_id)

    # download voice by bytes
    download_file = bot.download_file(voice_file_info.file_path)

    # read bytes
    voice_bytes = BytesIO(download_file)
    # create audiosegment and change frame to 16000
    voice_file = AudioSegment.from_file(voice_bytes).set_frame_rate(16000)

    # save voice message in wav format file
    voice_out_path = os.path.join(str(user_id)
                                  , 'audio_message_{}.wav'.format(num_audio))
    voice_file.export(os.path.join(voice_messages_path, voice_out_path),
                      format='wav',
                      tags={'uid': '{}'.format(user_id),
                            'username': '{}'.format(user_name)})
    # save voice info to db
    db.save_voice((os.path.join('voice_messages', voice_out_path), user_id))

    db.close()

    bot.send_message(message.chat.id, 'Я сохранил твой сладкий голосок')


@bot.message_handler(content_types=['photo'])
def find_face_and_save(message):
    face_path = os.path.join(config.data_path, 'photo_face')
    face_num = len(os.listdir(face_path)) + 1

    user_id = message.from_user.id

    photo_id = message.photo[-1].file_id
    photo_file_info = bot.get_file(photo_id)

    # download photo by bytes
    download_file = bot.download_file(photo_file_info.file_path)

    # read bytes
    photo_bytes = BytesIO(download_file)

    # create numpy array from bytes and create image
    nparr = np.frombuffer(download_file, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # load dnn model from OpenCV created in TF represent
    net = cv2.dnn.readNetFromTensorflow(config.model_path, config.config_path)

    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)),
                                 1.0, (300, 300), [104, 117, 123], False, False)
    # face detect
    net.setInput(blob)
    detections = net.forward()
    conf_threshold = 0.7
    first_detection = False
    for i in range(detections.shape[2]):
        if detections[0, 0, i, 2] > conf_threshold and first_detection == False:
            first_detection = True
            break

            # save image
    if (first_detection):
        cv2.imwrite(os.path.join(face_path, '{}_face_{}.png'.format(str(user_id), face_num)),image)
        bot.send_message(message.chat.id, 'Я сохранил твою мордочку')
    else:
        bot.send_message(message.chat.id, 'Увы, я не нашел лица')


if __name__ == '__main__':
    bot.polling(none_stop=True)
