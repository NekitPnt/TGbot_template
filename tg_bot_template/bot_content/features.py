from dataclasses import dataclass

from tg_bot_template.bot_lib.bot_feature import Button, Feature, FeatureMenu, TgUtils


@dataclass
class Buttons:
    menu: str = "Меню"


empty = Feature()
ping_ftr = Feature(
    commands=["ping", "health", "healthcheck"],
    text="200 pong",
    text2="Bot is alive",
)
creator_ftr = Feature(
    commands=["creator"],
    text="*Master?*",
)
set_user_info = Feature(
    slashed_command="/set_info",
    slashed_command_descr="set profile info",
    button="Мой профиль",
    about="добавить инфу о себе, чтобы все знали кто самый сильный игрок тут.",
    keyboard=[[Button(text=Buttons.menu)]],
    text="Напишите ваше имя",
    text2="Готово, данные обновлены.",
    set_to_bot_commands=True,
)
set_user_name = Feature(text="Отлично, записал. Теперь немного расскажите о себе.", data_key="name")
set_user_about = Feature(text="Отлично, записал. Теперь скиньте свое фото.", data_key="info")
press_button_ftr = Feature(
    slashed_command="/push_the_button",
    slashed_command_descr="we gonna push the button",
    button="Нажми меня",
    about="просто жми и не думай",
    text="Нажатий за последнюю сессию: {last_session}",
    callback_action="tap",
    set_to_bot_commands=True,
)
rating_ftr = Feature(
    slashed_command="/rating",
    slashed_command_descr="global rating",
    about="общий рейтинг",
    button="Рейтинг",
    keyboard=[[Button(text=Buttons.menu)]],
    text="Всего нажатий твоих: {user_taps}\nВсего нажатий: {total_taps}",
    text2=f"Лучший жмакер:\n{{name}}[{TgUtils.dog}{{username}}]\n{{info}}",
    set_to_bot_commands=True,
)
start_ftr = Feature(
    slashed_command="/start",
    slashed_command_descr="main menu",
    commands=["menu"],
    about="в главное меню",
    text="Добро пожаловать в главное меню",
    button=Buttons.menu,
    callback_action="main_menu",
    menu=FeatureMenu(grid=[[press_button_ftr], [rating_ftr], [set_user_info]]),
    set_to_bot_commands=True,
    one_time_keyboard=True,
)
help_ftr = Feature(
    slashed_command="/help",
    slashed_command_descr="bot help",
    text="Бот для соревнования по тыканью по кнопке. Тыкай в кнопку и побеждай!",
    set_to_bot_commands=True,
)
register_ftr = Feature(text="Welcome to bot")
cancel_ftr = Feature(
    slashed_command="/cancel",
    button="Отмена",
    text="Принял, отбой, возвращаюсь в главное меню.",
    keyboard=[[Button(text="Отмена")]],
)
