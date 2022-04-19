Скрипт для генерации видеоролика с визуализацией звука в виде волны с ипользованием ffmpeg-python.
Цвет волны изменяется каждые n секунд. В качестве фона можно использовать gif-изображения. 


Флаги:

--audiofile - путь до аудиофайла, используемого в качестве объекта визуализации 
--gif - путь до изображения в формате gif, используемого в качестве фона
--n - интервал изменения цвета волны (в секундах)

Пример использования скрипта:

python main.py --audiofile "audio_files/Fallin' Down.mp3" --gif "background_gifs/background.gif" --n 1


