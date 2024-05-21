FROM python:3.12-slim
WORKDIR /app
COPY tg_bot_float_steam_source/requirements.txt tg_bot_float_steam_source/
RUN pip install --no-cache-dir --upgrade -r tg_bot_float_steam_source/requirements.txt
COPY tg_bot_float_steam_source/ tg_bot_float_steam_source/
COPY settings.py .
COPY tg_bot_float_common_dtos/ tg_bot_float_common_dtos/
EXPOSE 5005
ENTRYPOINT [ "python", "-m", "uvicorn", "tg_bot_float_steam_source.main:app", "--host", "0.0.0.0", "--port", "5005"]
