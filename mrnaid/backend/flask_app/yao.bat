
set ENV_NAME := mRNAid
set SHELL := /bin/bash
set CONDA_ACTIVATE = eval "$$(conda shell.bash hook)" && conda activate $(ENV_NAME)


rem this is for celery tasks
set CELERY_BROKER_URL=redis://127.0.0.1:6379
set CELERY_RESULT_BACKEND=redis://127.0.0.1:6379
set LOG_FILE=./logs/logs.log
set BACKEND_OBJECTIVES_DATA=../common/objectives/data
set PYTHONPATH=../common:../common/objectives:../common/constraints
python3.11 -m celery -A tasks worker --loglevel=info


rem : flower run:
CELERY_BROKER_URL=redis://127.0.0.1:6379 \
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379 \
celery flower --port=5566