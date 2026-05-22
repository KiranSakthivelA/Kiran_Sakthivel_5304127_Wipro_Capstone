import logging
import os

_step_logs = []

class StepLogAccumulator(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        _step_logs.append(log_entry)

def get_and_clear_step_logs():
    global _step_logs
    if not _step_logs:
        return ""
    logs = "\n".join(_step_logs)
    _step_logs.clear()
    return logs

class LogGen:
    @staticmethod
    def loggen():
        log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_file = os.path.join(log_dir, 'automation.log')
        
        accumulator_handler = StepLogAccumulator()
        accumulator_handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(message)s'))
        
        logging.basicConfig(
            handlers=[logging.FileHandler(log_file, encoding='utf-8'), logging.StreamHandler(), accumulator_handler],
            format='%(asctime)s: %(levelname)s: %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p',
            force=True
        )
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        return logger

