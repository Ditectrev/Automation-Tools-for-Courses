file = open('Test_README.md')

def generate_urls(lines):
   indexes = [i for i in range(len(lines)) if lines[i].startswith("###")]
   questions = [lines[indexes[i] : indexes[i + 1]] for i in range(len(indexes) - 1)]
   for question in questions:
      buffer = ""
      buffer += question[0].strip("### ").replace("\n", "").replace(" ", "-").replace(".", "").replace("\"","").replace(":","").replace("’", "").replace(")", "").replace("(", "").replace(",", "").replace("[", "").replace("]", "").replace("“","").replace("”","").replace("✑","").replace("---","-").replace("--","-").replace("?","").replace("%", "").replace("'", "").replace("/", "").lower()
      buffer += "\n"
      with open("urls.csv","a") as f:
         f.write(buffer)

generate_urls(file.readlines())
