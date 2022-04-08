import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from fake_useraagent import UserAgent
import csv
import time 

RESULT_PATH = 'C:\\Users\\서지혜\\세미 플젝\\crawling_result\\'
now = datetime.now()

