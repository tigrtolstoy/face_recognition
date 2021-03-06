# Face Recognition

Клиент-серверное приложение для идентификации лиц.<br>
На стороне клиента работает web-камера. При нажатии клавиши "пробел" приложение просит пользователя ввести идентификационный номер. После ввода номера, номер и кадр с web-камеры отправляются на сервер. На стороне сервера происходит обработка изображения и идентификация пользователя. После идентификации отчет отправляется клиенту, на чьей сторое происходит его сохранение в json-файл, фотография, отрпавленная на сервер, сохраняется. Так же производится логирование операций и результатов.

## Отчеты об идентификации

Каждый отчет содержит 4 поля:

- `coincidence_confidence` - процент "уверенности" алгоритма распознавания в том, что на сравниваемых фото совпадают
- `filename` - имя файла под которым сохранена присланная для идентификация фотография
- `msg` - подробное сообщение о результате идентификации
- `status` - статус идентификации (`successful`, `unsuccessful`)

Каждый отчет сохраняется в json-файл формата `YYYY-mm-dd__hh:mm:ss_identification_info.json`, где `YYYY` - год, `mm` - месяц, `dd` - день, `hh` - час, `mm` - минуты, `ss` - секунды.

### Возможные варианты отчетов

**Успешная идентификация**:

```json
{
  "coincidence_confidence": 80,
  "filename": "35.png",
  "msg": "Пользователь [123] успешно идентифицирован",
  "status": "successful"
}

```

**Человек неопознан**:

```json
{
  "coincidence_confidence": 70,
  "filename": "46.png",
  "msg": "Другой человек в кадре",
  "status": "unsuccessful"
}
```

**В кадре отсутсвует человек**:

```json
{
  "coincidence_confidence": "-",
  "filename": "47.png",
  "msg": "Нет лица в кадре",
  "status": "unsuccessful"
}
```

**В кадре несколько лиц**:

```json
{
  "coincidence_confidence": "-",
  "filename": "48.png",
  "msg": "Больше одного лица в кадре",
  "status": "unsuccessful"
}
```

В репозиторий добавлены примеры логов [сервера](https://github.com/tigrtolstoy/face_recognition/blob/master/server.log) и [клиента](https://github.com/tigrtolstoy/face_recognition/blob/master/client.log).

При проваленой идентификации повторная попытка возможна на ренее, чем через 5 секунд.

## Установка зависимостей

1. Установить `cmake` (для работы с `dlib`)
2. Установить необходимые библиотеки: `pip3 install -r requirements.txt`

## Инструкция по работе с приложением

1. В папку `staff_faces` загрузить фотографии сотрудников с раширением `.png`. Названия файла фотографии соответствует `id` сотрудника.
2. В файле `client_config.json` установить значение параметра `camera_id` соответсвующее id web-камеры.
3. Запустить клиентскую часть приложений с помощью команды `python3 secure_camera.py`.
4. Запустить серверную часть приложений с помощью команды `python3 secure_system.py`.
5. После нажатия на пробел ввести в консоль идентификационный номер.

## Дополнительные настройки

В файле `clietn_config.json` находятся параметры клиентской части приложения <br>
Значения по умолчанию:

```json
{
    "camera_id": 0,
    "frame_width": 640,
    "frame_height": 480,

    "wrong_ident_timeout": 5,

    "server_host": "0.0.0.0",
    "server_port": 5051
}
```

`camera_id` - id web-камеры в системе <br>
`frame_width` - ширина кадра в пикселях <br>
`frame_height` - высота кадра в пикселях <br>

`wrong_ident_timeout` - время после проваленой идентификации, в течение которого нельзя отправлять повторный запрос <br>
`server_host` - хост, на котором работает серверная часть приложения <br>
`server_port` - порт, на котором работает серверная часть приложения <br>

В файле `server_config.json` находятся параметры серверной части приложения <br>
Значения по умолчанию:

```json
{
    "host": "0.0.0.0",
    "port": 5051,
    "path_to_save_photos": "identification_photos",
    "db_path": "staff_faces",
    "accuracy_thrashold": 0.9
}
```

`host` - хост, на котором работает серверная часть приложения <br>
`port` - порт, на котором работает серверная часть приложения <br>
`path_to_save_photos` - директория для сохранения присылаемых с камеры фотографий <br>
`db_path` - директория, в которой хранятся эталонные фотографии сотрудников <br>
`accuracy_thrashold` - порог "уверенности" для идентификации человека <br>

В папке `path_to_save_photos` находятся две директории:

- successful
- unsuccessful

successful - директория, в которой сохраняются фотографии после успешной идентификации <br>
unsuccessful - директория, в которой сохраняются фотографии после проваленной идентификации <br>

## Проблемы

Детектирование лиц происходит с помощью HOG-дескрипторов (сверточные сети не использовал ввиду требовательности к ресурсам). HOG-дескрипторы очень чувствительны к ориентации лица, качеству снимка и освещению. Поэтому достаточно часто возникает ситуация, когда на изображении лицо не обнаруживается, хотя фактически оно там есть.