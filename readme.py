import pandas as pd

file = open('Test_README.md')
data = []
for line in file.readlines():
   if ('###' in line) or ('- [x]' in line) or ('- [ ]' in line):
      #data.append(line)
      if '###' in line:
         print('question')
         print(line)
         data.append('question: ' + line.replace("###", "").replace("\n", ""))
      elif '- [x]' in line:
         print('correct answer')
         print(line)
         data.append('correct answer: ' + line.replace("- [x]", "").replace("\n", ""))
      #print(data)
      elif '- [ ]' in line:
         print('not correct answer')
         print(line)
         data.append('not correct answer: ' + line.replace("- [ ]", "").replace("\n", ""))

print(data)

df = pd.DataFrame(data=data)
df.to_csv('generated.csv')
