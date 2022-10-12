from tg_bot_template.bot_content.classes import Feature, Button

ping_ftr = Feature(
    commands=["ping", "health", "healthcheck"],
    text="200 pong",
    text2="Bot is alive",
)
empty = Feature()
start_ftr = Feature(
    slashed_command="/start",
    slashed_command_descr="start bot",
    text="Hello there",
)
help_ftr = Feature(
    slashed_command="/help",
    slashed_command_descr="bot help",
    text="Here will be help anytime",
)
register_ftr = Feature(
    commands=["bot"],
    text=f"Welcome to bot"
)
cancel_ftr = Feature(
    slashed_command="/cancel",
    button="Отмена",
    text="Принял, отбой, возвращаюсь в главное меню.",
    keyboard=[[Button(text="Отмена")]],
)
register_failed = "Для регистрации заполните, пожалуйста, Имя пользователя в своем профиле, иначе вас не смогут найти" \
                  " другие участники!"
please_register = "Enter passphrase for register in bot:"
text_error = "What? Dont understand."

BOT_COMMAND_FEATURES_LIST = [start_ftr, help_ftr]
