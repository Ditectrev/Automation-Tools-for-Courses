import markdown as md

with open('Test_README.md', 'r') as f:
   text = f.read()
   html = md.markdown(text)

with open('Test_README.html', 'w') as f:
   f.write(html)