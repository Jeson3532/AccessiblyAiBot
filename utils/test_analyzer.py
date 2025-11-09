import pandas as pd
from ai_agent.yandex_gpt import generate_theme_blocks
import pprint
import json

path_ = "../files/test.csv"


def get_theme_blocks(path):
    data = pd.read_csv(path)
    result = generate_theme_blocks(str(data))
    return result


pprint.pp(get_theme_blocks(path_))
