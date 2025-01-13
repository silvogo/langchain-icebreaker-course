from dotenv import load_dotenv
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
import os

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from third_parties.twitter import scrape_user_tweets
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent


def ice_break_with(name: str) -> str:
    # Get linkedin url
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url= linkedin_username)

    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(username=twitter_username, mock=True)

    summary_template = """
            given the information {information} about a person from linkedin {information},
            and their latest twitter posts {twitter_posts} I want you to create:
            1. a short summary
            2. two interesting facts about them
            
            Use both information from twitter and Linkedin
        
        """

    summary_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
    chain = summary_prompt_template | llm

    res = chain.invoke(input={"information": linkedin_data, "twitter_posts": tweets})


    print(res)

if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker Enter")
    ice_break_with(name='Eden Marco Udemy')
