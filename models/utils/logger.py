import logging


def log_fitness_table(iteration, solution, fitness):
    if iteration == 0:
        logging.info('iteration | solution' + ' ' * 51 + '| fitness')
        logging.info('-' * 80)
    str_sol = str(solution)
    str_solution = str_sol+' '*(59-len(str_sol)) if len(str_sol) < 59 else \
        str_sol[:56]+'...'
    logging.info(f'{iteration} {" "*(11 - len(str(iteration)))}| '
                 f'{str_solution}| {fitness}')


def log_hive_detail(details: dict):
    logging.info('#'*80)
    logging.info('\t\t HIVE DETAILS')
    for k, v in details.items():
        logging.info(f'\t{k}:\t{v}')
    logging.info('#' * 80)

