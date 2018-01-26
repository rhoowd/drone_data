import logging

logger_env = logging.getLogger('Energy')
logger_env.setLevel(logging.INFO)
sh = logging.StreamHandler()
# fm = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > [%(name)s] %(message)s')
fm = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(message)s')
sh.setFormatter(fm)
logger_env.addHandler(sh)
