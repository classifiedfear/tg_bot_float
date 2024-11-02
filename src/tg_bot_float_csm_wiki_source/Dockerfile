FROM python:3.12-slim
WORKDIR /app
COPY tg_bot_float_csm_wiki_source/requirements.txt tg_bot_float_csm_wiki_source/
RUN pip install --no-cache-dir --upgrade -r tg_bot_float_csm_wiki_source/requirements.txt
COPY tg_bot_float_common_dtos/csm_wiki_source_dtos/ tg_bot_float_common_dtos/csm_wiki_source_dtos/
COPY tg_bot_float_csm_wiki_source/ tg_bot_float_csm_wiki_source/
EXPOSE 5003
ENTRYPOINT [ "python", "-m", "uvicorn", "tg_bot_float_csm_wiki_source.main:app", "--host", "0.0.0.0", "--port", "5003"]
