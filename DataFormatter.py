from collections import defaultdict
import os
import csv
import re

class DataFormatter:
    def __init__(self, file):
        self.rawFileData = file
        self.linkedQuestion = None
        self.formattedData = self.formatData(file)

    def formatData(self, file):
        #holds student answer data and question data
        questions = []
        questionIDArr = []

        source_data = None

        #stores old file name
        fileDir = os.path.splitext(file)[0]
        fileName = fileDir.split('/')[len(fileDir.split('/'))-1]
        fileType = os.path.splitext(file)[1]
        print(f'fileName: {fileName}, fileType: {fileType}, fileDir: {fileDir}')

        #Used to write new question file and new student answer file
        questionFile = fileDir + "-questions" + fileType
        stuAnsFile = fileDir + "-studentAnswers" + fileType


        studentCount = 0
        #opens the input file for reading
        with open(file) as data:
            rd = csv.reader(data, delimiter=',', quotechar='"')
            #opens the question file for writing
            with open(questionFile, 'w') as data2:
                ques_writer = csv.writer(data2)
                ques_writer.writerow(["question_id", "question_content", "original_type", "linked_question", "source_data",
                                      "correct_option", "max_score", "option_0", "option_1", "option_2", "option_3",
                                      "option_4", "reference"])
                #opens the student answer file for writing
                with open(stuAnsFile, 'w') as data3:
                    stuAns_writer = csv.writer(data3)
                    stuAns_writer.writerow(
                        ["Key", "Student_ID", "Question_ID", "Source_Data", "Chosen_Option", "Reasoning_ID", "Reasoning", "Score"])

                    #Begins to iterate through the original file
                    for student in rd:

                        #looks at first row of data, and extract question info
                        if studentCount == 0:
                            print(f'Student Count: {studentCount}')

                            #goes item by item to extract each question from the file
                            for item in range(len(student)):
                                #File is formatted weird, so only every other column has an actual question
                                if item % 2 == 1:

                                    #extracts all the data after calling extractQuestion() function
                                    question_id, question_content, original_type, \
                                    linked_question, source_data, correct_option = self.extractQuestion(fileName, student[item])

                                    #once data is extracted, write data into our own csv file
                                    ques_writer.writerow(
                                            [question_id, question_content, original_type,
                                             linked_question, source_data, correct_option])

                                    #stores all the question id's and content in an array for future use
                                    questionIDArr.append(question_id)
                                    questions.append(question_content)

                        #every row after the first row is student answer data
                        else:
                            print(f'Student Count: {studentCount}')
                            studentAns = self.extractStudent(student, questionIDArr, source_data)

                            for ans in studentAns:
                                stuAns_writer.writerow(ans)


                        studentCount += 1

        return file

    def extractQuestion(self, fileName, text):
        print("\nNext Question")
        #print(f'text: {text}')
        #print(f'Linked Question: {self.linkedQuestion}')

        question_id = re.match('q[0-9]+([a-z]?)([0-9]?)', text)
        if question_id != None:
            question_id = question_id.group(0)
        #print(question_id)

        #Question Content

        question_content = re.split(':', text)
        #print(question_content)

        if len(question_content) > 1:
            question_content = question_content[1].strip()
            question_content = re.split('\n', question_content)[0]
            #print(question_content)
        else:
            question_content = None

        #print(question_content)

        #Source File

        source_data = fileName.split('.')[0]
        #print(source_data)

        #Correct Option

        correct_option = None
        correct_opt = re.split('\n', text)
        correct_opt = re.split(',', correct_opt[len(correct_opt)-1])
        correct_opt = re.split('Correct option = (\s)?', correct_opt[0])

        #print(f'correct_opt: {correct_opt}')

        linked_question = None
        original_type = None
        if len(correct_opt) > 1:
            correct_option = correct_opt[len(correct_opt)-1]
            self.linkedQuestion = question_id
            original_type = "MC"
        # Linked Question
        else:
            linked_question = self.linkedQuestion
            self.linkedQuestion = question_id
            original_type = "SA"

        #print(f'correct_option: {correct_option}')
        #print(f'linked_question: {linked_question}')
        #print(f'original_type: {original_type}')

        return question_id, question_content, original_type, linked_question, source_data, correct_option


    def extractStudent(self, student, questions, source_data):
        answers = []

        print(f'student: {student}')
        print(f'questions: {questions}')
        student_id = student[0]

        print(f'Question Length: {len(questions)}')
        print(f'Student Length: {len(student)}')

        #Key, Student_ID, Question_ID, Source_Data, Chosen_Option, Reasoning_ID, Reasoning, Score

        for item in range(1,len(student)-1):
            #each student answer corresponds with 4 columns, so you can extract all the data by
            # working by multiples of 4
            if item % 4 == 1:
                question_id = questions[(int)(item/2)]
                key = student_id + "_" + question_id
                chosen_option = student[item]
                reasoning_id = questions[((int)(item/2)) + 1]
                reasoning = student[item+2]
                score = student[item+3]
                #print(f'Key: {key}, Student Id: {student_id}, Question Id: {question_id}, Source Data: {source_data}, '
                 #     f'Chosen Option: {chosen_option}, Reasoning_Id: {reasoning_id}, Reasoning: {reasoning}, Score: {score}')
                answers.append([key, student_id, question_id, source_data, chosen_option, reasoning_id, reasoning, score])

        print(f'answers: {answers}')
        print(f'answers length: {len(answers)}')

        return answers

    #def extractKey:
    #def extractStudentId:
    #def extractQuestionId:
    #def extractSourceFile:
    #def extractChosenOption:
    #def extractReasoningId:
    #def extractReasoning:
    #def extractScore:


