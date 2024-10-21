FROM python:3.12-slim
WORKDIR /app
COPY tg_bot_float_db_updater/requirements.txt tg_bot_float_db_updater/
RUN pip install --no-cache-dir --upgrade -r tg_bot_float_db_updater/requirements.txt
COPY tg_bot_float_db_updater/ tg_bot_float_db_updater/
COPY tg_bot_float_common_dtos/schema_dtos/ tg_bot_float_common_dtos/schema_dtos/
COPY tg_bot_float_common_dtos/update_db_scheduler_dtos/ tg_bot_float_common_dtos/update_db_scheduler_dtos/
COPY tg_bot_float_common_dtos/csm_wiki_source_dtos/csm_wiki_dto.py tg_bot_float_common_dtos/csm_wiki_source_dtos/
COPY tg_bot_float_misc/router_controller/ tg_bot_float_misc/router_controller/
EXPOSE 5006
ENTRYPOINT ["python", "-m", "uvicorn", "tg_bot_float_db_updater.main:app", "--host", "0.0.0.0", "--port", "5006"]
