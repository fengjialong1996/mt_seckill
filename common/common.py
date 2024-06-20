from typing import List
from selenium.webdriver.common.service import Service

class MyService(Service):
    def command_line_args(self, **options) -> List[str]:
        return []