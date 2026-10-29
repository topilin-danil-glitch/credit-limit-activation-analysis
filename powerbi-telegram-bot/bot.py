import io
import logging

import matplotlib
matplotlib.use("Agg")  # Работа без графического интерфейса
import matplotlib.pyplot as plt

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from pbi_connector import query_pbi
import config

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def chart_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /chart."""
    await update.message.reply_text("Подключаюсь к Power BI Desktop...")

    try:
        # 1. Получаем данные из Power BI
        df = query_pbi(config.DAX_QUERY)

        if df.empty:
            await update.message.reply_text("Данные пусты. Проверьте DAX-запрос.")
            return

        # 2. Строим график
        fig, ax = plt.subplots(figsize=(10, 5))

        numeric_cols = df.select_dtypes(include=["number"]).columns

        if len(numeric_cols) > 0:
            col = numeric_cols[0]
            df[col].plot(ax=ax, marker="o", linestyle="-")
            ax.set_title(f"Power BI: {col}")
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
        else:
            # Если чисел нет — отправляем текст
            await update.message.reply_text(
                f"Данные:\n```\n{df.head(10).to_string()}\n```",
                parse_mode="Markdown",
            )
            return

        # 3. Отправляем картинку
        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight", dpi=100)
        buf.seek(0)
        plt.close(fig)

        await update.message.reply_photo(
            photo=buf,
            caption=f"Данные из Power BI Desktop. Строк: {len(df)}",
        )

    except ConnectionError as e:
        await update.message.reply_text(f"{e}")
    except Exception as e:
        logger.exception("Ошибка")
        await update.message.reply_text(f"Ошибка: {e}")


async def tables_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает список таблиц в модели Power BI."""
    await update.message.reply_text("Запрашиваю список таблиц...")
    try:
        df = query_pbi("EVALUATE INFO.TABLES()")
        if df.empty:
            await update.message.reply_text("Таблиц не найдено.")
            return
        name_col = "Name" if "Name" in df.columns else df.columns[0]
        names = df[name_col].tolist()
        text = "Таблицы в модели:\n" + "\n".join(f"- {n}" for n in names)
        await update.message.reply_text(text)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я достаю данные из открытого Power BI Desktop.\n\n"
        "Команды:\n"
        "/chart — построить график по вашему DAX-запросу\n"
        "/tables — показать список таблиц в модели"
    )


def main():
    if config.TELEGRAM_TOKEN == "ВАШ_ТОКЕН_ОТ_BOTFATHER":
        print("Ошибка: заполните TELEGRAM_TOKEN в config.py")
        return

    app = Application.builder().token(config.TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("chart", chart_command))
    app.add_handler(CommandHandler("tables", tables_command))

    print("Бот запущен. Убедитесь, что Power BI Desktop открыт.")
    app.run_polling()


if __name__ == "__main__":
    main()