import sqlite3
from django.shortcuts import render
from first_project import settings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain
def getOutput():
    db_path = settings.DATABASES['default']['NAME']
    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()
    result=cursor.execute("SELECT * FROM playground_user_info")
    connection.commit()
    row=result.fetchall()
    data_tuple=row[0]
    cuisine_name=data_tuple[1]
    height=data_tuple[4]
    weight=data_tuple[5]
    age=data_tuple[6]
    goals_raw=data_tuple[7]
    issues_raw=data_tuple[8]
    gender=data_tuple[9]
    allergies_raw=data_tuple[3]
    if goals_raw=='':
        goals="No goals"
    else:
        goals=goals_raw
    if issues_raw=='':
        issues="No issues"
    else:
        issues=issues_raw

    if allergies_raw=='':
        allergies="No allergies"
    else:
        allergies=allergies_raw

    food_list=data_tuple[2]
    food_type="".join(food_list)
    length=len(food_type)
    final_food_type=""
    for i in range(1,length-1):
        if(food_type[i]==','):
            final_food_type=final_food_type+" and"
        else:
            final_food_type=final_food_type+food_type[i]
    llm=ChatOpenAI(openai_api_key="OPENAI_API_KEY", model_name="gpt-3.5-turbo",temperature=0.18)
    prompt_template1=ChatPromptTemplate.from_messages(
        [
            ("system","calculate the BMI of a user and return the answer as a single number"),
            ("human","the user's weight is 50 kg"),
            ("human","the user's height is 165 cm"),
            ("ai","18.37"),
            ("human","the user's weight is {weight} kg"),
            ("human","the user's height is {height} cm"),
        ]
    )
    chain1=LLMChain(prompt=prompt_template1,llm=llm)
    user_bmi=chain1.run(weight=weight,height=height)
    prompt_template2=ChatPromptTemplate.from_messages(
        [
            ("system","the user's BMI is {user_bmi}"),
            ("human","based on my BMI tell me if I am overweight, healthy or underweight"),
        ]
    )
    chain2=LLMChain(prompt=prompt_template2,llm=llm)
    response1=chain2.run(user_bmi=user_bmi)
    prompt_template3=ChatPromptTemplate.from_messages(
        [
            ("system","you are a dietitian"),
            ("human","My BMI is {user_bmi}"),
            ("human","My gender is {gender}"),
            ("human","suggest whether I am underweight, healthy or overweight"),
            ("human","I am {age} years old"),
            ("human","My preferred cuisine is {user_cuisine}"),
            ("human","I eat {food_type}"),
            ("human","I am allergic to or do not eat {allergies}"),
            ("human","My goal is {goals}"),
            ("human","I have the following health issues {issues}"),
            ("human","recommend me a meal plan based on my {goals} with the quantity in brackets and calories in brackets."),
            ("human","Please adjust the calories based on my {goals} and {weight} in kilograms"),
            ("human","I want to {goals}"),
            ("human","all weights are in Kilograms"),
            ("ai","based on your preferences here is 7 day meal plan suited to your preferred cuisine")

        ]
    )
    chain3=LLMChain(prompt=prompt_template3,llm=llm)
    response2=chain3.run(user_bmi=user_bmi,age=age,user_cuisine=cuisine_name,food_type=final_food_type,allergies=allergies,goals=goals,issues=issues, gender=gender,weight=weight)
    title_prompt_template = ChatPromptTemplate.from_messages(
        [
            ("human", "What is BMI and its categories"),
            ("ai", '''BMI stands for Body Mass Index. It is a measure of body fat based on a person's weight and height. BMI is calculated by dividing a person's weight (in kilograms) by their height (in meters squared).

    The categories for BMI are:

    - Underweight: BMI below 18.5
    - Normal weight: BMI between 18.5 and 24.9
    - Overweight: BMI between 25 and 29.9
    - Obese: BMI of 30 or higher'''),
            ("user", "{sentence}"),
        ]
    )
    chain4 = LLMChain(prompt=title_prompt_template, llm=llm)
    title_response = chain4.run("What is BMI and its categories")
    follow_prompt=ChatPromptTemplate.from_messages(
        [
            ("human","My weight is {weight} in kilograms"),
            ("human", "My height is {height} in centimeter"),
            ("human", "My BMI is {user_bmi}"),
            ("system","Normal weight: BMI between 18.5 and 24.9"),
            ("system","Underweight: BMI below 18.5"),
            ("system"," Overweight: BMI between 25 and 29.9"),
            ("system",''' Obesity:
  - Class 1: BMI between 30 and 34.9
  - Class 2: BMI between 35 and 39.9
  - Class 3 (Morbid Obesity): BMI of 40 or higher'''),
            ("human", "tell me how many more kilograms do I have to loose or gain to be healthy if I am not healthy"),


        ]
    )
    follow_prompt2=ChatPromptTemplate.from_messages(
        [
            ("human","My weight is {weight}"),
            ("human", "My height is {height}"),
            ("human", "My BMI is {user_bmi}"),
            ("system","Normal weight: BMI between 18.5 and 24.9"),
            ("system","Underweight: BMI below 18.5"),
            ("system"," Overweight: BMI between 25 and 29.9"),
            ("system",'''- Obesity:
  - Class 1: BMI between 30 and 34.9
  - Class 2: BMI between 35 and 39.9
  - Class 3 (Morbid Obesity): BMI of 40 or higher'''),
            ("human", "tell me how many more kilograms do I have to loose or gain to be obese"),

        ]
    )
    chain6=LLMChain(prompt=follow_prompt2,llm=llm)
    response4=chain6.run(weight=weight,height=height,user_bmi=user_bmi)
    chain5=LLMChain(prompt=follow_prompt,llm=llm)
    response3=chain5.run(weight=weight,height=height,user_bmi=user_bmi)
    context = {
        "title_response": title_response,
        "response1": response1,
        "response3":response3,
        "response2": response2,
        "response4":response4,
    }
    cursor.execute("DELETE FROM playground_user_info")
    connection.commit()
    return context
