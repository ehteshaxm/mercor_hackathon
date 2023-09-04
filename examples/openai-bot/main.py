from textbase import bot, Message
from typing import List
from pytube import YouTube
import os
import assemblyai as aai
from langchain.document_loaders import YoutubeLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain

aai.settings.api_key = f"a40e575635994111ac4d1b0fe72b18bf" 
transcriber = aai.Transcriber()
link_added = False
youtube_path=None
youtube_url=''
qa_transcript=None

def save_audio(url):
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download()
    base, ext = os.path.splitext(out_file)
    file_name = base + '.mp3'
    os.rename(out_file, file_name)
    print(yt.title + " has been successfully downloaded.")
    print(file_name)
    print(yt.length)
    return yt.title, file_name, yt.thumbnail_url

def chapter_generation(url):
    transcript = transcriber.transcribe(url, config=aai.TranscriptionConfig(auto_chapters=True))
    return transcript

def summary_generator(url):
    config=aai.TranscriptionConfig(
        summarization=True,
        summary_model=aai.SummarizationModel.informative,
        summary_type=aai.SummarizationType.bullets_verbose
    )
    transcript = transcriber.transcribe(
        url,
        config=config
    )
    return transcript.summary

def subtitle_generator(url):
    transcript = transcriber.transcribe(url)
    with open('sub.srt', 'w', encoding='utf-8') as srt_file:
        srt_file.write(transcript.export_subtitles_srt())
    print(transcript.export_subtitles_srt())

def ask_question(url, question):
    global qa_transcript
    if qa_transcript is None:
        qa_transcript = transcriber.transcribe(url)
    questions = [
        aai.LemurQuestion(
        question=question, answer_format='bullet points'),
    ]
    params={
        "questions": questions,
        "final_model": "default"
    }
    result = qa_transcript.lemur.question(**params)
    print(result)
    print(result.response)
    return result

def question_ans(url, query):
    embeddings = OpenAIEmbeddings(openai_api_key='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')
    db=None
    if os.path.isdir("faiss_index"):
        db = FAISS.load_local("faiss_index", embeddings)
    else:
        loader = YoutubeLoader.from_youtube_url(
        "https://www.youtube.com/watch?v=Aih05VGzE-o", add_video_info=True
        )

        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            length_function=len,
            add_start_index=True,
            )

        documents = text_splitter.split_documents(docs)

        db = FAISS.from_documents(documents, embeddings)
        db.save_local("faiss_index")
        
    print("started")
    docs = db.similarity_search(query)
    llm = ChatOpenAI(openai_api_key='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')
    chain = load_qa_chain(llm, chain_type="stuff")
    answer = chain.run(input_documents=docs, question=query)
    print(answer)
    return answer

@bot()
def on_message(message_history: List[Message], state: dict = None):

    global link_added
    global youtube_path
    global youtube_url

    command=message_history[-1]['content'][0]['value']
        
    if 'youtube' in command and link_added == False:
        video_title, save_location, video_thumbnail = save_audio(command)
        youtube_path = save_location
        youtube_url = command
        link_added=True
        response = {
            "data": {
                "messages": [
                    {
                        "data_type": "STRING",
                        "value": "Use any of the commands below \n /generate_summary. \n /generate_chapters. \n /ask_question. \n /generate_subtitles"
                    }
                ],
                "state": state
            },
            "errors": [
                {
                    "message": ""
                }
            ]
        }
        
        return {
        "status_code": 200,
        "response": response
        }
    
    elif '/generate_summary' in command and link_added == True:
        summary = summary_generator(youtube_path)
        response = {
        "data": {
            "messages": [
                {
                    "data_type": "STRING",
                    "value": summary
                }
            ],
            "state": state
        },
        "errors": [
            {
                "message": ""
            }
        ]
        }

        return {
            "status_code": 200,
            "response": response
        }
    
    elif '/generate_chapters' in command and link_added == True:
        transcript = chapter_generation(youtube_path)

        def handle_chapters(chapter):
            time = int(chapter.start/1000)
            return {
                "data_type": "STRING",
                "value": f"{chapter.headline} \n\n {youtube_url}&t={time}s \n\n {chapter.summary}"
            }
        
        response = {
            "data": {
                "messages": list(map(handle_chapters , transcript.chapters)) ,
                "state": state
            },
            "errors": [
                {
                    "message": ""
                }
            ]
        }

        return {
            "status_code": 200,
            "response": response
        }
    
    elif '/generate_subtitles' in command and link_added == True:
        subtitle_generator(youtube_path)
        response = {
            "data": {
                "messages": [
                    {
                        "data_type": "STRING",
                        "value": "Subtitles generation complete"
                    }
                ],
                "state": state
            },
            "errors": [
                {
                    "message": ""
                }
            ]
        }
        
        return {
        "status_code": 200,
        "response": response
        }
    

    elif '/ask_question. ' in command:
        question = command.split(". ")[1]
        ans = question_ans(youtube_url, question)
        print(ans)
        response = {
            "data": {
                "messages": [
                    {
                        "data_type": "STRING",
                        "value": ans
                    }
                ],
                "state": state
            },
            "errors": [
                {
                    "message": ""
                }
            ]
        }
        
        return {
        "status_code": 200,
        "response": response
        }

    
    elif youtube_path == None:
        response = {
            "data": {
                "messages": [
                    {
                        "data_type": "STRING",
                        "value": "Please paste link to a YouTube video 😊"
                    }
                ],
                "state": state
            },
            "errors": [
                {
                    "message": ""
                }
            ]
        }
        
        return {
        "status_code": 200,
        "response": response
        }
    
    else:
        response = {
            "data": {
                "messages": [
                    {
                        "data_type": "STRING",
                        "value": "Use any of the commands below \n /generate_summary. \n /generate_chapters. \n /ask_question. \n /generate_subtitles"
                    }
                ],
                "state": state
            },
            "errors": [
                {
                    "message": ""
                }
            ]
        }
        
        return {
        "status_code": 200,
        "response": response
        }
    