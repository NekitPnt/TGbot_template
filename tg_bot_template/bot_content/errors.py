from dataclasses import dataclass


@dataclass
class Errors:
    text: str = "What? Dont understand."
    text_form: str = "Не вижу в сообщении текста, попробуйте еще раз!"
    photo_form: str = "Не вижу в сообщении фото, попробуйте еще раз! Возможно вам нужно отправить фото без сжатия."
    register_failed: str = (
        "Для регистрации заполните, пожалуйста, Имя пользователя в своем профиле, иначе вас не "
        "смогут найти другие участники!"
    )
    please_register: str = "Enter passphrase for register in bot:"
