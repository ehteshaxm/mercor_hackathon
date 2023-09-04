

<p align="center">
    <a href="https://docs.textbase.ai">
        <img alt="Documentation" src="https://img.shields.io/website/http/huggingface.co/docs/transformers/index.svg?down_color=red&down_message=offline&up_message=online">
    </a>
</p>

<h1 align="center">
    <p>✨ Youtube Chatbot with Textbase, Assembly AI and Open AI ✨</p>
</h1>

#### Features
+ Generate Summaries
+ Generate Chapters - Timestamp based real YouTube links
+ Generate Subtitles - Actual `.srt` file to use with the video
+ Ask Questions - Get refined answers with `Langchain` x `Assembly AI` x `Open AI` features.



#### Note
1. Add Open AI `API_KEY` and Assembly AI `API_KEY` in `main.py` and repo will take care of the rest :)

2. Use accurate YouTube video links, Make sure while posting that `&t=` query params is not present in the link pasted


## Installation
Make sure you have `python version >=3.9.0`, it's always good to follow the [docs](https://docs.textbase.ai/get-started/installation) 👈🏻
### 1. Through pip
```bash
pip install textbase-client
```

### 2. Local installation
Clone the repository and install the dependencies using [Poetry](https://python-poetry.org/) (you might have to [install Poetry](https://python-poetry.org/docs/#installation) first).

For proper details see [here]()

```bash
git clone https://github.com/ehteshaxm/mercor_hackathon
cd textbase
poetry shell
poetry install
```

## Start development server

Run the following command:
- if installed locally
    ```bash
    poetry run python textbase/textbase_cli.py test
    ```
- if installed through pip
    ```bash
    textbase-client test
    ```
Response:
```bash
Path to the main.py file: examples/openai-bot/main.py # You can create a main.py by yourself and add that path here. NOTE: The path should not be in quotes
```
Now go to the link in blue color which is shown on the CLI and you will be able to chat with your bot!
![Local UI](assets/test_command.png)

### `Other commands have been mentioned in the documentaion website.` [Have a look](https://docs.textbase.ai/usage) 😃!


## Contributions

Contributions are welcome! Please open an issue or create a pull request.
