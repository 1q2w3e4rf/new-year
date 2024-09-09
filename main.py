import telebot
from telebot import types
from bs4 import BeautifulSoup
import requests
from db import DB
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

db = DB()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Приветствую, {0.first_name}! Я - бот, который поможёт тебе найти нужный новогодний факт".format(message.from_user))

def parse_legends(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    legends = soup.find_all('p')
    return [legend.text for legend in legends]

def parser_fakts(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    fakt = soup.find_all('p')
    return [fakt.text.strip() for fakt in fakt]

fakt = parser_fakts('https://basetop.ru/top-7-strashnyih-istoriy-pro-rozhdestvo/')

legends = parse_legends('https://gainynv-news.ru/news/media/2021/12/6/100-i-1-zabavnyih-faktov-pro-novyij-god/')

@bot.message_handler(commands=['legend'])
def send_fakt(message):
    keyboard = types.InlineKeyboardMarkup(
        [
            [types.InlineKeyboardButton("1. Ла Бефана", callback_data="la_befana")],
            [types.InlineKeyboardButton("2. Святой Томас", callback_data="svyatoy_tomas")],
            [types.InlineKeyboardButton("3. Йольский кот", callback_data="yolskiy_kot")],
            [types.InlineKeyboardButton("4. Фрау Перхта", callback_data="frau_perhta")],
            [types.InlineKeyboardButton("5. Крампус", callback_data="kram_pus")],
            [types.InlineKeyboardButton("6. Хольда", callback_data="hol_da")],
            [types.InlineKeyboardButton("7. Рождество и оборотни", callback_data="rozhdestvo_i_oborotni")],
        ]
    )
    
    bot.send_message(message.chat.id, fakt[0], reply_markup=keyboard)

@bot.message_handler(commands=['fact'])
def send_legends(message):
    keyboard = types.ReplyKeyboardMarkup()
    for i in range(1, len(legends) + 1):
        keyboard.add(types.KeyboardButton(str(i)))
    bot.send_message(message.chat.id, "Выберите номер факта:", reply_markup=keyboard)

removed_numbers = set()

user_removed_numbers = {}

@bot.message_handler(content_types=['text'])
def send_fact(message):
    user_id = message.chat.id
    if user_id not in user_removed_numbers:
        user_removed_numbers[user_id] = set()

    if message.text.isdigit() and 0 < int(message.text) <= len(legends):
        fact_number = int(message.text) - 1
        bot.send_message(message.chat.id, legends[fact_number])
        user_removed_numbers[user_id].add(int(message.text))  # Add the selected fact number to the user's set
        keyboard = types.ReplyKeyboardMarkup()
        for i in range(1, len(legends) + 1):
            if i not in user_removed_numbers[user_id]:
                keyboard.add(types.KeyboardButton(str(i)))
        bot.send_message(message.chat.id, "Выберите номер факта:", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Неверный номер факта")
photo = [
    open('1.jpg', 'rb'),
    open('2.jpg', 'rb'),
    open('3.jpg', 'rb'),
    open('4.jpg', 'rb'),
    open('5.jpg', 'rb'),
    open('6.jpg', 'rb'),
    open('7.jpg', 'rb'),
]
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "la_befana":
        bot.send_photo(call.message.chat.id, photo[6])
        bot.send_message(call.message.chat.id, "Рождественская ведьма с крючковатым носом, одетая в дырявые чулки, длинный плащ и остроконечную шляпу. Она летает на метле 6-ого января (день Торжества Богоявления), Ла Бефана дарит подарки хорошо воспитанным мальчикам и девочкам. Вместо подарка для «плохишей» Ла Бефана бросает в дымоход уголь или набивает углем чулок, подвешенный на елке. Итальянские родители предупреждают своих шалунов и шалуний, что если те будут плохо себя вести, Ла Бефана унесет их с собой. Во многих отношениях Ла Бефана играет такую же роль как Святой Николай и Крампус «в одном флаконе». Есть предание, что Ла Бефана связана с тремя волхвами. Она предоставила мудрецам кров и еду, но отказалась идти посмотреть на младенца Христа, потому что у нее слишком много работы по дому. Затем Ла Бефана передумала, но не смогла найти ни Иисуса ни волхвов. Вот и летает теперь по миру в их поисках.")
    elif call.data == "svyatoy_tomas":
        bot.send_photo(call.message.chat.id, photo[5])
        bot.send_message(call.message.chat.id, "По праву занимает вторую строчку в списке самых страшных легенд, связанных с Рождеством австрийская история о Святом Томасе. Не имеет значения, хорошо вы себя вели целый год или были отъявленным негодяем, Томас наказывает всех. Этот человек с длинной бородой, разделенной на две половины, приходил 21 декабря с наступлением темноты. Если дверь в дом была открыта, Томас проникал в жилище, молча разглядывал его обитателей и указывал на одного из них. Имя бедолаги теперь было записано в Книгу Смерти и до следующего Нового года дожить ему было не суждено. Однако Томаса можно было задобрить, предложив ему особое печенье. А чтобы он не зашел в дом за дверью нужно было поставить скрещенные вилы или мётлы. А вот двери амбаров от Святого Томаса не запирали, чтобы был хороший урожай, потому что к растительности он относился добрее, чем к людям.")
    elif call.data == "yolskiy_kot":
        bot.send_photo(call.message.chat.id, photo[4])
        bot.send_message(call.message.chat.id, "На четвертом месте нашего страшдественского хит-парада находится существо, которого боятся дети в Исландии. Йольский кот бродит ночами во время Йоля (Святок) и наказывает тех, кто не приобрел новую шерстяную одежду на Рождество. Его описывают как гигантского черного пушистого зверя, который напоминает исландцам о необходимости усердно трудиться на протяжении всего предстоящего года. Ведь кто работает, тот может позволить себе обновку. А кто не работает, того Йольский кот съест. Особенно любит он полакомиться ленивыми и непослушными детьми. Есть и более гуманная версия истории, согласно ей Йольский зверь съедает не детишек, а праздничное угощение. Зато хорошим детям кот дарит подарки.")
    elif call.data == "frau_perhta":
        bot.send_photo(call.message.chat.id, photo[3])
        bot.send_message(call.message.chat.id, "Еще одна языческая германская богиня, вошедшая в наш рейтинг удивительных рождественских историй. Ее днем считалась Двенадцатая ночь (6 января). Любимые блюда фрау Перхты - рыба и каши. Тем, кто ест что-либо другое в ее праздник капризная богиня могла набить животы соломой. Чтобы задобрить Перхту рекомендовалось оставить ей молоко или кашу. Возможно, это имеет связь с традицией оставлять молоко и печенье для Санта-Клауса.")
    elif call.data == "kram_pus":
        bot.send_photo(call.message.chat.id, photo[1])
        bot.send_message(call.message.chat.id, "Благодаря Интернету, комиксам и фильмам ужасов произошла вспышка интереса к этому демоническому помощнику Святого Николая. В Восточном Тироле и немецкоговорящих областях Южного Тироля Крампус - это уродливое и волосатое существо, которого могут вызвать дети в канун дня Святого Николая. Проснувшись, Крампус следует за Святым Николаем, но если последний одаривает хороших детей, то Крампус наказывает плохих. Он либо кладет им под подушку уголь, либо сажает в мешок и уносит в пещеру. Считается, что похищенного ребенка Крампус использует в качестве главного блюда на своем рождественском ужине. Не шалите!")
    elif call.data == "hol_da":
        bot.send_photo(call.message.chat.id, photo[0])
        bot.send_message(call.message.chat.id, "Также известная как Холле и Холл, Хольда является германской богиней, которую можно найти в фольклоре Скандинавии, Северной Германии и альпийских регионов Баварии, Австрии, Швейцарии и Южного Тироля. По легенде Хольда проводит ночи между Рождеством и Богоявлением путешествуя на повозке или верхом на лошади как участница Дикой Охоты. Считается, что она ведет души некрещеных младенцев и тех, кто еще не готов попасть на небеса, то есть язычников и ведьм. «Ехать с Холл» - значит прогуляться с ведьмой.")
    elif call.data == "rozhdestvo_i_oborotni":
        bot.send_photo(call.message.chat.id, photo[2])
        bot.send_message(call.message.chat.id, "Согласно поверьям Центральной и Южной Европы дети, родившиеся на Рождество, могут стать оборотнями. Почему? Потому что родились в тот же день, что и Иисус Христос, а это рассматривалось как кощунство по отношению к Сыну Божьему. В своем знаменитом романе «Оборотень в Париже» Гай Эндор напомнил об этой легенде. Герой его книги родился как раз на Рождество")

bot.infinity_polling()