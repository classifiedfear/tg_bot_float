FROM python:3.12-slim
WORKDIR /app
COPY tg_bot_float_scheduler/requirements.txt tg_bot_float_scheduler/
RUN pip install --no-cache-dir --upgrade -r tg_bot_float_scheduler/requirements.txt
COPY tg_bot_float_scheduler/ tg_bot_float_scheduler/
COPY settings.py .
ENTRYPOINT [ "python", "-m", "tg_bot_float_scheduler.main"]
