import pandas as pd

file = open('Test_README.md')
data = []

for line in file.readlines():
   if ('###' in line) or ('- [x]' in line) or ('- [ ]' in line):
      if '###' in line:
         data.append('question: ' + line.replace("###", "").replace("\n", ""))
      elif '- [x]' in line:
         data.append('correct answer: ' + line.replace("- [x]", "").replace("\n", ""))
      elif '- [ ]' in line:
         data.append('not correct answer: ' + line.replace("- [ ]", "").replace("\n", ""))

df = pd.DataFrame(data=data)
df.to_csv('generated.csv', index=False)
