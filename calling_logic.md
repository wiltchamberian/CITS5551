# Tha basic structure of mRNAid backend.

## The first entry point for async algorithm processing is:
routines.py
@app.route('/api/v1/optimize', methods=['POST'])
- def optimization():  
  - parse the input
  - parse = RequestParse(request)
  - parameters = parser.parse()
  - spawn an async celery,task, return task.id
    

## the task is 
@celery.task()
def optimization_evaluation_task(parameters:dict) -> str:

- parameters = OptimizationParameters.parse_obj(parameters)// get the optimized parameters.

- optimization_problems = [initialize_optimization_problem(parameters) for _ in range(parameters.number_of_sequences)]//init problems by parameters
- result = pool.map(optimization_task, optimization_problems) //map the same task to multiple problems


- evaluator = Evaluation(list(set(result)), parameters)
- final_response = evaluator.get_evaluation()
  - pool = Pool()
  - optimized_results = pool.map(self.get_seq_properties, tag_seqs)
    - get_seq_properties
      - use MFE and CAI // here is the algorithms
  - 

# second entry for query task performing output by taskid

@app.route('/api/v1/status/<task_id>', methods=['GET'])
def status(task_id: str) -> str:


# some simple class
## Logger.py 
is just for output log to files. 
## Exceptions.py 
used to define exception which can be raised if necessary.
## DataTypes.py : 
wrapper some parameters to class
## RequestParser.py: 
parse parameters to construct OptimizationParameters