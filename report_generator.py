import os

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate


DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


def generate_report(dataframe, groq_api_key, model_name=DEFAULT_MODEL):
    """Generate a written EDA report for ``dataframe`` using a Groq-hosted LLM."""
    chat_groq = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name=model_name)

    # Create a prompt template for generating the report
    prompt_template = PromptTemplate(
        input_variables=["data_summary", "data_sample"],
        template="""
        ### DATA ANALYSIS REQUEST:
        You are an expert data analyst. Analyze the following data and generate a comprehensive report, including insights, trends, and statistical summaries.

        ### DATA SUMMARY:
        {data_summary}

        ### DATA SAMPLE:
        {data_sample}

        ### INSTRUCTIONS:
        Provide the analysis in a structured format with clear insights, potential trends, and any relevant statistical information. 
        Make sure to summarize the findings effectively. Generate the report in format with headings, bullet points, and a conclusion. Any statistical summary should be calculated using {data_summary} only.
        """
    )

    # Prepare data summary and sample for the prompt
    data_summary = dataframe.describe(include='all').to_json()
    data_sample = dataframe.head().to_json()

    # Create the complete prompt
    prompt = prompt_template.format(data_summary=data_summary, data_sample=data_sample)

    # Call Groq API to generate the report
    response = chat_groq.invoke(prompt)

    return getattr(response, "content", "No report generated.")

