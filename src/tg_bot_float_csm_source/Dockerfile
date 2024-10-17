FROM python:3.12-slim
WORKDIR /app
COPY tg_bot_float_csm_source/requirements.txt tg_bot_float_csm_source/
RUN pip install --no-cache-dir --upgrade -r tg_bot_float_csm_source/requirements.txt
COPY tg_bot_float_csm_source/ tg_bot_float_csm_source/
COPY tg_bot_float_common_dtos/csm_source_dtos/ tg_bot_float_common_dtos/csm_source_dtos/
EXPOSE 5004
ENTRYPOINT [ "python", "-m", "uvicorn", "tg_bot_float_csm_source.main:app", "--host", "0.0.0.0", "--port", "5004"]
