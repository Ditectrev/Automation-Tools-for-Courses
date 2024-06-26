file = open('Test_README.md')

def generate_answer_string(answers):
    answer_arr = []
    correctness_arr = []
    for i, answer in enumerate(answers):
        if "- [x]" in answer:
            formatted_answer = answer.strip("- [x] ")
            correctness_arr.append('1')
        else:
            formatted_answer = answer.strip("- [ ] ")
            correctness_arr.append('0')
        formatted_answer = formatted_answer.replace("\n", "").replace(",", "")
        answer_arr.append(formatted_answer)
    return answer_arr, correctness_arr


def generate_questions(lines):
   indexes = [i for i in range(len(lines)) if lines[i].startswith("###")]
   questions = [lines[indexes[i] : indexes[i + 1]] for i in range(len(indexes) - 1)]
   for question in questions:
      buffer = '"'
      buffer += question[0].strip("### ").replace("\n", "").replace(",", "") + '"'
      buffer += ","
      answers, correctness = generate_answer_string(question[2:-1])
      buffer += ",".join(answers)
      buffer += ',"' + ",".join(correctness) + '"'
      buffer += '\n'
      with open("test-eduonix.csv","a") as f:
         f.write(buffer)

generate_questions(file.readlines())
