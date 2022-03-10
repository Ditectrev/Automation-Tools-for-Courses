file = open('Test_README.md')

def generate_answer_string(answers):
   answer_arr = []
   raw_arr = []
   for i, answer in enumerate(answers):
      if "- [x]" in answer:
         formatted_answer = answer.strip("- [x] ")
         answer_arr.append(str(i))
      else:
         formatted_answer = answer.strip("- [ ] ")
      raw_arr.append(formatted_answer.replace("\n", "").replace(",", ""))
      last_item = len(answers) - 1
      if len(answers) < 6 and i == last_item:
         missing_difference = 6 - len(answers)
         for j in range(missing_difference):
            raw_arr.append('')
   return raw_arr, answer_arr, len(answer_arr) > 1


def generate_questions(lines):
   indexes = [i for i in range(len(lines)) if lines[i].startswith("###")]
   questions = [lines[indexes[i] : indexes[i + 1]] for i in range(len(indexes) - 1)]
   for question in questions:
      buffer = ""
      buffer += question[0].strip("### ").replace("\n", "").replace(",", "")
      # Part of the code to generate URLs for table of content.
      #buffer += question[0].strip("### ").replace("\n", "").replace(" ", "-").replace(".", "").replace("\"","").replace(":","").replace("’", "").replace(")", "").replace("(", "").replace(",", "").replace("[", "").replace("]", "").replace("“","").replace("”","").replace("✑","").replace("---","-").replace("--","-").replace("?","").replace("%", "").lower()
      # buffer += "\n"
      buffer += ","
      answers, correct_idxs, is_ma = generate_answer_string(question[2:-1])
      buffer += "multi-select," if is_ma else "multiple-choice,"
      buffer += ",".join(answers)
      correct_idxs_integers = list(map(int, correct_idxs))
      correct_idxs_integers_incremented = []
      for correct_idx_integer in correct_idxs_integers:
         correct_idx_integer += 1
         correct_idxs_integers_incremented.append(correct_idx_integer)
      string_ints = [str(int) for int in correct_idxs_integers_incremented]
      if (len(string_ints) == 1):  
         buffer += ',' + ",".join(string_ints)
      else:
         buffer += ',' + '"' + ",".join(string_ints) + '"'
      buffer += ',,\n' # For 'Explanation' and 'Knowledge Area' to keep these fields empty.
      with open("test.csv","a") as f:
         f.write(buffer)

generate_questions(file.readlines())
