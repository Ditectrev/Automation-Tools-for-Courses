import pandas as pd

file = open('Test_README.md')
for line in file.readlines():
   with open("test.csv","a") as f:
      if '###' in line:
         f.write("\n" + line.replace("### ", "").replace("\n", "") + ',')
      if '- [x]' in line:
         f.write(line.replace("- [x]", "").replace("\n", "") + ',')
      if '- [ ]' in line:
         f.write(line.replace("- [ ]", "").replace("\n", "") + ',')


# if line.count('- [x]') > 1:
#             f.write('multi-select,')
#          if line.count('- [x]') == 1:
#             f.write('multiple-choice,')