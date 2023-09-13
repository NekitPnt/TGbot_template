FROM python:3.10  as base
# set work directory
WORKDIR /app/tg_bot_template/
FROM base as deps
COPY requirements.txt ./
RUN pip install --user -r requirements.txt

FROM deps as app
# copy project
COPY . ./
# run app
CMD ["python", "-m", "tg_bot_template.bot"]