from tg_bot_template.bot_content.classes import Ftr, Button

ping_ftr = Ftr(
    commands=["ping", "health", "healthcheck"],
    text="200 pong",
    text2="Bot is alive",
)
empty = Ftr()
start_ftr = Ftr(
    slashed_command="/start",
    slashed_command_descr="start bot",
    text="Hello there",
)
help_ftr = Ftr(
    slashed_command="/help",
    slashed_command_descr="bot help",
    text="Here will be help anytime",
)
register_ftr = Ftr(
    commands=["bot"],
    text=f"Welcome to bot"
)
cancel_ftr = Ftr(
    slashed_command="/cancel",
    button="Отмена",
    text="Принял, отбой, возвращаюсь в главное меню.",
    keyboard=[[Button(text="Отмена")]],
)
register_failed = "Для регистрации заполните, пожалуйста, Имя пользователя в своем профиле, иначе вас не смогут найти" \
                  " другие участники!"
please_register = "Enter passphrase for register in bot:"
text_error = "What? Dont understand."
