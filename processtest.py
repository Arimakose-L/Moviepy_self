import proglog

import time  # for simulating computing time
from proglog import default_bar_logger

def my_routine(iterations=10, logger='bar'):
    """Run several loops to showcase Proglog."""
    logger = default_bar_logger(logger)  # shorthand to generate a bar logger
    for i in logger.iter_bar(iteration=range(iterations)):
        for j in logger.iter_bar(animal=['dog', 'cat', 'rat', 'duck']):
            time.sleep(0.1)  # simulate some computing time

my_routine()