import os
import sys
from scrapy.cmdline import execute

file_path = os.path.dirname(os.path.abspath(__file__))

sys.path.append(file_path)

execute(["scrapy","crawl","jobbole"])



