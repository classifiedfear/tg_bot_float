# tg_bot_float

To run tg_bot_float_db_ap in docker container you need to cd to the src directory and run these two commands:

`docker build -t tg_bot_float_db_app -f tg_bot_float_db_app/Dockerfile .`

`docker run -it --rm -p 5001:5001 --name tg_bot_fast_db_app tg_bot_float_db_app`
