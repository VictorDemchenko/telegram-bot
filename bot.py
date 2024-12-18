from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Токен вашего бота
TOKEN = "7800081122:AAFIBS7T4KMeR_9ab4Rf4nYj77Ujjk-RaxM"

# Функция для подсчета цифр
def format_block(numbers, digit):
    count = str(numbers).count(str(digit))
    return str(digit) * count if count > 0 else "-"

# Функция для внешнего квадрата
def count_total(blocks, keys):
    return sum(len(blocks[key].replace("-", "")) for key in keys)

# Основная функция для расчета матрицы судьбы
async def calculate_matrix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Получаем дату рождения
        date_of_birth = update.message.text.strip()
        day, month, year = map(int, date_of_birth.split("."))

        # Разбиваем дату рождения на цифры
        digits = list(map(int, date_of_birth.replace(".", "")))

        # Дополнительные числа
        first_sum = sum(digits)  # Первое дополнительное число
        second_sum = sum(map(int, str(first_sum)))  # Второе дополнительное число (Число судьбы)
        first_digit_day = int(str(day)[0]) if str(day)[0] != "0" else int(str(day)[1])
        third_sum = first_sum - 2 * first_digit_day  # Третье дополнительное число
        fourth_sum = sum(map(int, str(abs(third_sum))))  # Четвертое дополнительное число

        # Собираем все числа для подсчета
        all_numbers = digits + [first_sum, second_sum, third_sum, fourth_sum]

        # Подсчет количества цифр от 1 до 9
        blocks = {
            "Характер (1)": format_block(all_numbers, 1),
            "Энергия (2)": format_block(all_numbers, 2),
            "Интерес (3)": format_block(all_numbers, 3),
            "Здоровье (4)": format_block(all_numbers, 4),
            "Логика (5)": format_block(all_numbers, 5),
            "Труд (6)": format_block(all_numbers, 6),
            "Удача (7)": format_block(all_numbers, 7),
            "Долг (8)": format_block(all_numbers, 8),
            "Память (9)": format_block(all_numbers, 9),
        }

        # Внешний квадрат
        temperament = count_total(blocks, ["Интерес (3)", "Логика (5)", "Удача (7)"])
        goal = count_total(blocks, ["Характер (1)", "Здоровье (4)", "Удача (7)"])
        family = count_total(blocks, ["Энергия (2)", "Логика (5)", "Долг (8)"])
        habits = count_total(blocks, ["Интерес (3)", "Труд (6)", "Память (9)"])
        life = count_total(blocks, ["Здоровье (4)", "Логика (5)", "Труд (6)"])

        # Число судьбы
        destiny_number = second_sum if second_sum in [10, 11] else sum(map(int, str(second_sum)))

        # Формирование результата
        result = f"Дата рождения: {date_of_birth}\n\n"
        result += "Ваша психоматрица:\n"
        for block, value in blocks.items():
            result += f"{block}: {value}\n"

        result += f"\n🔮 Число судьбы: {destiny_number}\n\n"
        result += f"Темперамент: {temperament}\n"
        result += f"Цель: {goal}\n"
        result += f"Семья: {family}\n"
        result += f"Привычки: {habits}\n"
        result += f"Быт: {life}\n"

        # Отправляем результат
        await update.message.reply_text(result)

    except Exception as e:
        await update.message.reply_text(" Пожалуйста, введите дату в формате ДД.ММ.ГГГГ.")

# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для расчета психоматрицы по Пифагору.\n"
        "Введите вашу дату рождения в формате ДД.ММ.ГГГГ, и я покажу вашу матрицу!"
    )

# Основной запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate_matrix))

    print("Бот запущен...")
    app.run_polling()
