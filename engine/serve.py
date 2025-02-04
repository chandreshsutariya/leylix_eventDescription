#!/usr/bin/env python

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes
# import getpass
import os


# configuring for langsmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = ""

#configuring for openaig
os.environ["OPENAI_API_KEY"] = ""


model = ChatOpenAI(model="gpt-4")

# 1. Create prompt template
"""
I am making a event handeline and showcasing application where a event organizer can \
create an event, and other users can see that event and can participate in it.\
So, when the event organizer is creating an event on the application, I want to \
give him/her a automated event description when they type event title.\

So, I am giving you a title of an event, please give me desctiption accordingly.
"""
system_template = "I am making a event handeline and showcasing application where a event organizer can \
create an event, and other users can see that event and can participate in it.\
So, when the event organizer is creating an event on the application, I want to \
give him/her a automated event description when they type event title.\
\
So, I am giving you a title of an event, please give me desctiption accordingly."
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{title}')
])

# 2. Create model
model = ChatOpenAI()

# 3. Create parser
parser = StrOutputParser()

# 4. Create chain
chain = prompt_template | model | parser


# 4. App definition
app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

# 5. Adding chain route
add_routes(
    app,
    chain,
    path="/chain",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)