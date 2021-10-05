import pandas as pd

file = open('Test_README.md')
data = []
for line in file.readlines():
   data.append(line.split('###'))  # provide more general splitter

df = pd.DataFrame(data=data)
df.to_csv('generated.csv')
