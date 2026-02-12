import os
import sys
import pandas as pd

print("=== MAIN START ===")
print("cwd:", os.getcwd())
print("python:", sys.executable)
print("file:", __file__)

from strats.weeklyBTC import WeeklyBTC

w = WeeklyBTC()
w.createFile()
print(pd.read_csv(w.path).tail())
print("Latest return:", w.get_return())