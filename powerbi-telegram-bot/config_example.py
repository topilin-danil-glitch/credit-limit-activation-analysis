# Скопируйте этот файл в config.py и заполните своими данными
TELEGRAM_TOKEN = "ВАШ_ТОКЕН_ОТ_BOTFATHER"

# DAX-запрос, который будет выполняться при команде /chart
# Замените 'Sales' на имя таблицы в вашей модели Power BI
DAX_QUERY = "EVALUATE TOPN(20, 'Sales')"