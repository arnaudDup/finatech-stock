## IMPORT
from typing import List
import os
import yahoo_finance as yahoo


## LOCAL IMPORT
from utils.config import Config_Reader
from utils.logger import Logger
logger = Logger(os.path.basename(__file__))

## LOCAL CONSTANT

class StockOption:
    def __init__(self, name:str):
        if self._test_if_exist(name):
            logger.warning("The stock options refered with the name {} does not exist".format(name))
        self.history, self.current_value = self._get_stocks_values(name)
        pass

    def _test_if_exist(self, name: str) -> bool:
        return True

    def _get_stocks_values(self, name: str) -> (List[float], float):
        first_date = Config_Reader.getattr("date")

        historical_value = yahoo.get_historical('2014-04-25', '2014-04-29')
        return True