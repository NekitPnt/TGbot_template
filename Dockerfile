FROM python:3.10
# set work directory
WORKDIR /usr/src/tg_bot_template/
# copy project
COPY . /usr/src/tg_bot_template/
# install dependencies
#RUN pip install --upgrade pip
RUN pip install --user -r requirements.txt
# run app
CMD ["python", "-m", "tg_bot_template.bot"]