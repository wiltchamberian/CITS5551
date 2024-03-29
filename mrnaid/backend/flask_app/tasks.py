import json
import os

import numpy as np

import sys
sys.path.append(os.path.abspath("../common"))

from Evaluation import Evaluation
from OptimizationProblems import initialize_optimization_problem
from OptimizationTask import optimization_task
from billiard import Pool
from celery import Celery
from utils.Datatypes import OptimizationParameters
from utils.Logger import MyLogger


# Setting up logger
logger = MyLogger(__name__)



#CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL'),
#CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
CELERY_BROKER_URL="redis://127.0.0.1:6379"
CELERY_RESULT_BACKEND="redis://127.0.0.1:6379"

NUMBER_OF_ATTEMPTS = 3

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


def init_pool():
    np.random.seed()


@celery.task()
def optimization_evaluation_task(parameters: dict) -> str:
    """
    Optimize sequences using Optimization class, evaluate results using Evaluation class
    :param parameters: Dictionary created from OptimizationParameters class
    :return: JSON with the response dictionary containing both input and optimized sequences and their evaluation
    """

    parameters = OptimizationParameters.parse_obj(parameters)

    ## why use a loop to call initialize_optimization_problem
    # maybe to produce multiple instances
    optimization_problems = [initialize_optimization_problem(parameters) for _ in range(parameters.number_of_sequences)]

    pool = Pool(initializer=init_pool)
    ##apply function optimization_task to each instance of optimization_problems
    result = pool.map(optimization_task, optimization_problems)

    if len(set(result)) < parameters.number_of_sequences:
        logger.info('Less sequences than required!')
        attempt_count = 0
        while len(set(result)) < parameters.number_of_sequences and attempt_count < NUMBER_OF_ATTEMPTS:
            logger.info('Performing additional optimization attempt')
            result.append(optimization_task(initialize_optimization_problem(parameters)))
            attempt_count += 1

            if len(set(result)) == parameters.number_of_sequences:
                logger.info(f'Correct number achieved! Stopping...')
                break
            elif (attempt_count == parameters.number_of_sequences) and (
                    len(set(result)) < parameters.number_of_sequences):
                logger.info('Not able to provide required number of results. Stopping...')
                break
            else:
                pass

    evaluator = Evaluation(list(set(result)), parameters)
    final_response = evaluator.get_evaluation()
    final_response["input_parameters"] = parameters.dict()
    return json.dumps(final_response)
