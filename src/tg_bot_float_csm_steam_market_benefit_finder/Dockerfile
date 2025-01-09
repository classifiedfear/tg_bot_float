FROM python:3.12-slim
WORKDIR /app
COPY tg_bot_float_sub_benefit_finder/requirements.txt tg_bot_float_sub_benefit_finder/
RUN pip install --no-cache-dir --upgrade -r tg_bot_float_sub_benefit_finder/requirements.txt
COPY tg_bot_float_csm_steam_market_benefit_finder/ tg_bot_float_csm_steam_market_benefit_finder/
COPY tg_bot_float_common_dtos/tg_result_dtos/ tg_bot_float_common_dtos/tg_result_dtos/
COPY tg_bot_float_common_dtos/steam_source_dtos/ tg_bot_float_common_dtos/steam_source_dtos/
COPY tg_bot_float_common_dtos/csm_source_dtos/ tg_bot_float_common_dtos/csm_source_dtos/
COPY tg_bot_float_common_dtos/schema_dtos/subscription_to_find_dto.py tg_bot_float_common_dtos/schema_dtos/
EXPOSE 5007
ENTRYPOINT [ "python", "-m", "uvicorn", "tg_bot_float_sub_benefit_finder.main:app", "--host", "0.0.0.0", "--port", "5007" ]
