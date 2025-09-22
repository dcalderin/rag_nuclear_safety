from openai import AzureOpenAI,OpenAI
import os



system_prompt = """
You are a nuclear safety assistant. Your role is to provide accurate, technical information strictly derived from the provided document. Use precise nuclear safety terminology.

Here are some example Q&A pairs to guide your responses:

Q: What are the requirements for containment isolation in PWRs?
A: Based on the documents, containment isolation requirements for PWRs include:
- Automatic isolation valves with redundancy (GDC 55)
- Consideration of single failure criterion
- Classification as Engineered Safety Feature (ESF)
Sources: [Verbatim source document, Page 45, link]

Q: What is the regulatory basis for emergency core cooling systems?
A: The regulatory requirements for ECCS are established in:
- 10 CFR 50.46 for acceptance criteria
- GDC 35 for general design requirements
- Specific cooling capabilities and timing requirements
Sources: [Verbatim source document, Page 23, link]

Remember to:
1. Use only information from provided search results
2. Cite specific chunks when referencing information
3. Clearly state when information is not found
4. Provide markdown quotes for sources
5. Do not make assumptions or include external knowledge
"""


import pandas as pd

def make_cited_rag_prompt(query, df):
    # Generate context and citations
    context = ""
    citations = ""
    
    for _, row in df.iterrows():
        context += f"> {row['source_paragraph']}\n\n"
        citations += f"- Chunk {row['chunk']}, Page {row['page']}: [{row['pdf_link']}]({row['pdf_link']})\n"

    # Construct final prompt
    prompt =f"""
    ### Instructions:
    1. Answer Format:
       - Provide a clear, concise response based on the search results.
       - Use professional and technical language appropriate for nuclear safety documents.
       - Structure your response into readable paragraphs.
       - For regulatory basis questions, focus on specific GDCs and 10 CFRs requirements. 
    2. Math formatting:
        - Use $...$ for inline math: $C_i$, $CL_i$ 
        - Use $$...$$ for block equations
        - Follow standard LaTeX notation
        - Output will be rendered in Gradio Markdown with LaTeX support
        - For variable definitions, use bullet points or separate lines
        - Format like this:
        
        Where:
        * $C_i$ = activity concentration of radionuclide i
        * $CL_i$ = clearance level for radionuclide i
        
        - This separates LaTeX from complex prose
    3. Source Usage:
       - Use only information from the provided search results.
       - Prioritize the most relevant passages.
       - Cite specific page numbers for all referenced information.

    4. Citation Requirements:
       - Include a "Sources" section after your answer.
       - Include verbatim quotes, page numbers, and document links.

    5. Missing Information:
       - State clearly if information is not found.
       - Include any related information from the documents.
       - Do not use external knowledge.

    ### Context:
    {context}

    ### Query:
    {query}

    **Please provide your answer following the instructions above.**

    ### Sources:
    {citations}
    """

    return prompt



def get_cited_RAG_completion(query, search_results,llm_choice, n_results=3, temp_def=0.5, max_tokens=300,system_prompt=system_prompt, ):
    formatted_query = make_cited_rag_prompt(query, search_results)
    print("\n********This is the cited RAG prompt********\n")
    print(formatted_query)
    print("\n*********************************\n")
    
    if llm_choice == 'AzureGPT':
        try:
            client = AzureOpenAI(
                azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
                api_key=os.environ.get("AZURE_OPENAI_KEY"),
                api_version="2024-05-01-preview"
            )
            completion = client.chat.completions.create(
                model="gpt4-testing-app",  # Your Azure deployment name
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": formatted_query}
                ],
                max_tokens=max_tokens,
                temperature=temp_def
            )
            ans = completion.choices[0].message.content
        except Exception as e:
            print(f"Azure OpenAI Error: {str(e)}")
            ans = f"Error: {str(e)}"
    else:
        try:
            client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            completion = client.chat.completions.create(
                model=llm_choice,  # Use the selected model directly
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": formatted_query}
                ],
                max_tokens=max_tokens,
                temperature=temp_def
            )
            ans = completion.choices[0].message.content
        except Exception as e:
            print(f"OpenAI Error: {str(e)}")
            ans = f"Error: {str(e)}"
    
    return ans



# def get_completion(user_prompt, system_prompt, temp_def=0.5, max_tokens=300, model="gpt4-testing-app", llm_choice="AzureGPT"):
#     if llm_choice == "AzureGPT":
#         try:
#             client = AzureOpenAI(
#                 azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
#                 api_key=os.environ.get("AZURE_OPENAI_KEY"),
#                 api_version="2024-05-01-preview",
#             )
#             completion = client.chat.completions.create(
#                 model=model,
#                 messages=[
#                     {"role": "system", "content": system_prompt},
#                     {"role": "user", "content": user_prompt}
#                 ],
#                 max_tokens=max_tokens,
#                 temperature=temp_def
#             )
#         except Exception as e:
#             print(f"Azure OpenAI Error: {str(e)}")
#             raise
#     else:
#         try:
#             client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
#             completion = client.chat.completions.create(
#                 model=llm_choice,
#                 messages=[
#                     {"role": "system", "content": system_prompt},
#                     {"role": "user", "content": user_prompt}
#                 ],
#                 max_tokens=max_tokens,
#                 temperature=temp_def,
#                 top_p=1,
#                 frequency_penalty=0,
#                 presence_penalty=0
#             )
#         except Exception as e:
#             print(f"OpenAI Error: {str(e)}")
#             raise

#     return completion.choices[0].message.content


