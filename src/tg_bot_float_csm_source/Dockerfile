FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    gnupg \
    tzdata \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY tg_bot_float_csm_source/requirements.txt tg_bot_float_csm_source/
RUN pip install --no-cache-dir --upgrade -r tg_bot_float_csm_source/requirements.txt
COPY tg_bot_float_common_dtos/csm_source_dtos/ tg_bot_float_common_dtos/csm_source_dtos/
COPY tg_bot_float_csm_source/ tg_bot_float_csm_source/
COPY tg_bot_float_misc/router_controller/ tg_bot_float_misc/router_controller/
EXPOSE 5004
ENTRYPOINT [ "python", "-m", "uvicorn", "tg_bot_float_csm_source.main:app", "--host", "0.0.0.0", "--port", "5004"]
