import pandas as pd

file = open('Test_README.md')
data = []
for line in file.readlines():
   if '###' in line:
      print('question')
      print(line)
   elif '- [x]' in line:
      print('correct answer')
      print(line)
   #print(data)
   elif '- [ ]' in line:
      print('not correct answer')
      print(line)
   if ('###' in line) or ('- [x]' in line) or ('- [ ]' in line):
      data.append(line)

print(data)

df = pd.DataFrame(data=data)
df.to_csv('generated.csv')
