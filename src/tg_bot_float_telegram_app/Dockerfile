FROM python:3.12-slim
WORKDIR /app
COPY tg_bot_float_telegram_app/requirements.txt tg_bot_float_telegram_app/
RUN pip install --no-cache-dir --upgrade -r tg_bot_float_telegram_app/requirements.txt
COPY tg_bot_float_telegram_app/ tg_bot_float_telegram_app/
COPY tg_bot_float_common_dtos/ tg_bot_float_common_dtos/
EXPOSE 5010
ENTRYPOINT ["python", "-m", "uvicorn", "tg_bot_float_telegram_app.main:app", "--host", "0.0.0.0", "--port", "5010"]
