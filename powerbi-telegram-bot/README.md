# Power BI Desktop → Telegram Bot

Отправляет графики из локально открытого отчёта Power BI Desktop прямо в Telegram.

Важно

- Работает только на Windows.
- Power BI Desktop должен быть открыт с загруженным отчётом (`.pbix`).
- Бот подключается к локальному движку Analysis Services (`msmdsrv.exe`), который запускается вместе с Power BI.

Быстрый старт

1. Клонируйте репозиторий

```bash
git clone https://github.com/ваш-username/powerbi-telegram-bot.git
cd powerbi-telegram-bot
```

2. Установите зависимости

```bash
pip install -r requirements.txt
```

3. Создайте бота в Telegram

1. Напишите `@BotFather` в Telegram.
2. Отправьте `/newbot`, придумайте имя и username.
3. Скопируйте токен (выглядит как `1234567890:ABCdef...`).

4. Настройте конфигурацию

Скопируйте `config.example.py` в `config.py` и заполните:

```python
# config.py
TELEGRAM_TOKEN = "ВАШ_ТОКЕН_ЗДЕСЬ"
DAX_QUERY = "EVALUATE TOPN(10, 'ВашаТаблица')"  # Замените на ваш DAX-запрос
```

5. Запустите

1. Откройте ваш `.pbix` файл в Power BI Desktop.
2. В терминале выполните:

```bash
python bot.py
```

6. Используйте

В Telegram отправьте боту команду `/chart`. Он подключится к открытому Power BI, выполнит DAX-запрос и пришлёт график.

Как это работает

- `pbi_connector.py` автоматически находит порт, который Power BI Desktop использует для локального Analysis Services.
- Бот выполняет DAX-запрос через `pyadomd` и получает данные в виде таблицы.
- Matplotlib строит график, который отправляется в чат.

Если не подключается

- Убедитесь, что Power BI Desktop открыт и в нём загружен отчёт.
- Проверьте, что в `DAX_QUERY` указано реальное имя таблицы из вашей модели.
- Попробуйте запустить терминал от имени администратора.
- Если видите ошибку про `ADOMD.NET` — установите его с сайта Microsoft.

Как узнать имя таблицы

Если не работает DAX-запрос, откройте Power BI Desktop, перейдите на вкладку «Модель» и посмотрите название таблицы. Или выполните в боте тестовый запрос:

```dax
EVALUATE INFO.TABLES()
```

Он вернёт список всех таблиц в модели.

Зависимости

- `python-telegram-bot` — Telegram API.
- `pyadomd` — подключение к локальному Analysis Services.
- `pandas` — работа с таблицами.
- `matplotlib` — построение графиков.

Лицензия

MIT
