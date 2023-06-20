from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain
from langchain.chat_models import ChatOpenAI

from .models import Exam, Question

class CreateExamView(APIView):
    def post(self, request):
        #get the profession from query body
        profession = request.data["profession"]
        
        llm = ChatOpenAI(
            temperature=1,
            model_name="gpt-3.5-turbo-16k",
            max_tokens=10000,
            request_timeout=120
        )

        knowledge_prompt = PromptTemplate(
            input_variables=["profession"],
            template="""Bullet list of top 10 key concepts/skills a "{profession}" SHOULD know, no explanations""",
        )
        knowledge_chain = LLMChain(
            llm=llm,
            prompt=knowledge_prompt,
            output_key="knowledge",
        )

        exam_prompt = PromptTemplate(
            input_variables=["profession", "knowledge"],
            template="""
Write a 30-minute HR assesment for the position of "{profession}".
Make sure the difficulty is appropriate for their expected skill level and possible tasks on the job.
Ask multiple choice questions with 4 options and definitely add at least one free-text questions
And make sure to INCLUDE the correct answers for each question.
Example of a multiple choice question:
Q1 : What is the capital of France?
        a) Paris
        b) London
        c) Berlin
        d) Madrid
    Correct answer is a) Paris
Example of a free-text question:
Q2) Why is the sky blue?
    Correct answer is: "The sky appears blue because of a phenomenon called Rayleigh scattering. When sunlight passes through the Earth's atmosphere, the shorter blue and violet wavelengths of light are scattered more by the nitrogen and oxygen molecules in the air. Our eyes are more sensitive to blue light, so we perceive the scattered blue light, making the sky appear blue."
Cover the following concepts (ONE QUESTION CAN COVER MORE THAN ONE SUBJECT.):
{knowledge}""",
        )
        exam_chain = LLMChain(
            llm=llm,
            prompt=exam_prompt,
            output_key="exam",
        )

        json_prompt = PromptTemplate(
            input_variables=["exam"],
            template="""
Please extract the questions in the given text below, output format SHOULD be a python list of dictionaries here is one example:
EXAMPLE
INPUT
Q1 : What is the capital of France?
        a) Paris
        b) London
        c) Berlin
        d) Madrid
    Correct answer is a) Paris
Q2) Why is the sky blue?
    Correct answer is: "The sky appears blue because of a phenomenon called Rayleigh scattering. When sunlight passes through the Earth's atmosphere, the shorter blue and violet wavelengths of light are scattered more by the nitrogen and oxygen molecules in the air. Our eyes are more sensitive to blue light, so we perceive the scattered blue light, making the sky appear blue."
OUTPUT
[
    {{
        "question": "What is the capital of France?",
        "is_free_text": False,
        "is_multiple_choice": True,
        "a" : "Paris",
        "b" : "London",
        "c" : "Berlin",
        "d" : "Madrid",
        "answer": "a"
    }},
    {{
        "question": "Why is the sky blue?",
        "is_free_text": True,
        "is_multiple_choice": False,
        "a": ",
        "b": ",
        "c": ",
        "d": ",
        "answer": "The sky appears blue because of a phenomenon called Rayleigh scattering. When sunlight passes through the Earth's atmosphere, the shorter blue and violet wavelengths of light are scattered more by the nitrogen and oxygen molecules in the air. Our eyes are more sensitive to blue light, so we perceive the scattered blue light, making the sky appear blue."
    }}
]

END OF EXAMPLE

{exam}
"""
        )
        json_chain = LLMChain(
            llm=llm,
            prompt=json_prompt,
            output_key="json",
        )

        overall_chain = SequentialChain(
            chains=[knowledge_chain, exam_chain, json_chain],
            input_variables=["profession"],
            # Here we return multiple variables
            output_variables=["json"],
            verbose=True
        )

        exam = overall_chain.run(profession=profession)

        try:
            exam = eval(exam)
            print(exam)
        except Exception:
            return Response({'message': 'Error creating test'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        #create exam object
        exam_obj = Exam.objects.create(profession=profession)
        #create questions objects
        for i, question in enumerate(exam):
            Question.objects.create(
                exam=exam_obj,
                question=question["question"],
                is_multiple_choice=question["is_multiple_choice"],
                is_free_text=question["is_free_text"],
                a=question["a"],
                b=question["b"],
                c=question["c"],
                d=question["d"],
                answer=question["answer"],
                id_in_exam=i
            )
            #pop the answer from the question
            exam[i].pop("answer")
            exam[i]["id_in_exam"] = i

        return Response({'message': 'Test created', 'exam': exam, 'exam_id': exam_obj.pk}, status=status.HTTP_201_CREATED)
    
class GetResultsView(APIView):
    def post(self, request):
        #get the exam id from query body
        exam_id = request.data["exam_id"]
        #get the exam object
        exam_obj = Exam.objects.get(pk=exam_id)
        #get the questions objects
        questions = Question.objects.filter(exam=exam_obj)
        #order by id in exam
        questions = questions.order_by("id_in_exam")
        #get the answers from the query body
        answers = request.data["answers"]
        
        #get the number of correct answers
        score = 0

        for i, question in enumerate(questions):
            #if the question is multiple choice
            if question.is_multiple_choice:
                if question.answer == answers[str(i)]:
                    score += 1
            #if the question is free text
            elif question.is_free_text:
                #if the answer is correct
                score += handle_free_text_answer(question, answers[str(i)])

        #calculate the score
        score = score / len(questions) * 100
        return Response({'message': 'Test results', 'score': score}, status=status.HTTP_200_OK)
    
def handle_free_text_answer(question, user_answer):
    llm = ChatOpenAI(
            temperature=1,
            model_name="gpt-3.5-turbo-16k",
            max_tokens=10000,
            request_timeout=120
        )
    #create the prompt
    scoring_prompt = PromptTemplate(
        input_variables=["question", "answer", "user_answer"],
        template="""
Given the following question and its correct answer, please provide a score out of 10 to the user's answer.
EXAMPLE
INPUT
Question: Why is the sky blue?
Answer: The sky appears blue because of a phenomenon called Rayleigh scattering. When sunlight passes through the Earth's atmosphere, the shorter blue and violet wavelengths of light are scattered more by the nitrogen and oxygen molecules in the air. Our eyes are more sensitive to blue light, so we perceive the scattered blue light, making the sky appear blue.
Users Answer: The sky appears blue because the sunlight contains blue pigment. When the sun shines, it releases tiny blue particles that spread throughout the atmosphere, giving the sky its blue color. These blue particles then reflect the sunlight back to our eyes, creating the blue sky phenomenon.
OUTPUT
2
END OF EXAMPLE
Question: {question}
Answer: {answer}
Users Answer: {user_answer}
"""
    )
    scoring_chain = LLMChain(
        llm=llm,
        prompt=scoring_prompt,
        output_key="score",
    )

    extraction_prompt = PromptTemplate(
        input_variables=["score"],
        template="""
Please extract the score that is out of 10 in alphanumeric format from the given text below, output format SHOULD be a python integer here is one example:
EXAMPLE
INPUT
Score: 2/10 The user's answer is incorrect as it talks about the sun releasing blue pigment, which is not true. The explanation given is also not scientifically accurate. Therefore, the score is 2/10.
OUTPUT
2
END OF EXAMPLE
EXAMPLE
INPUT
Score: 10/10 The user's answer is correct as it talks about the sun releasing blue particles, which is true. The explanation given is also scientifically accurate. Therefore, the score is 10/10.
OUTPUT
10
END OF EXAMPLE
EXAMPLE
INPUT
5
OUTPUT
5
END OF EXAMPLE
EXAMPLE
INPUT
N/A
OUTPUT
0
END OF EXAMPLE
EXAMPLE 
INPUT
I couldn't find the score
OUTPUT
0
END OF EXAMPLE
IF YOU CAN'T FIND THE SCORE, PLEASE RETURN 0

Here is the score:
{score}
"""
    )
    extraction_chain = LLMChain(
        llm=llm,
        prompt=extraction_prompt,
    )

    overall_chain = SequentialChain(
        chains=[scoring_chain, extraction_chain],
        input_variables=["question", "answer", "user_answer"],
        verbose=True
    )

    score = overall_chain.run(question=question.question, answer=question.answer, user_answer=user_answer)
    try:
        score = int(score)
    except Exception:
        extraction_chain.run(score=score)
        score = int(score)
    
    return score/10