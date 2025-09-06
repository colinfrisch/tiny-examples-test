


from retrieve import retrieve
from generate import generate


def infer(question : str) -> str:
    """
    Whole pipeline for question answering with RAG
    """

    # Compare question
    top_chunk = retrieve(question)
    print(top_chunk+"\n ----------------------- \n\n")

    # Generate
    message_text = f"""
    Based on this context :
    {top_chunk}

    answer the following question :
    {question}
    """

    answer = generate(message_text)

    return answer


if __name__ == "__main__":
    input_question = input("Enter your question: ")
    answer = infer(input_question)
    print(answer)






