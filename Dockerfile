FROM python:3.10

WORKDIR /app/tg_bot_template/
COPY . /app/tg_bot_template/

RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "-m", "tg_bot_template.bot"]