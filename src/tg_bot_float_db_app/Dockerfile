FROM python:3.12-slim
WORKDIR /app
COPY tg_bot_float_db_app/requirements.txt tg_bot_float_db_app/
RUN pip install --no-cache-dir --upgrade -r tg_bot_float_db_app/requirements.txt
COPY tg_bot_float_db_app/ tg_bot_float_db_app/
COPY tg_bot_float_common_dtos/ tg_bot_float_common_dtos/
COPY tg_bot_float_misc/ tg_bot_float_misc/
EXPOSE 5001
ENTRYPOINT ["python", "-m", "uvicorn", "tg_bot_float_db_app.main:app", "--host", "0.0.0.0", "--port", "5001"]
