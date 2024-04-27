# Repo Amigo 2

## Setup

1. Clone the repo
```shell
git clone https://github.com/Marvin-Deng/Repo-Amigo-2.git
cd Repo-Amigo-2
```

2. Create a virtual environment
```shell
python -m venv venv

or

python3 -m venv venv
```

3. Start the virtual environment
```shell
# Windows
venv\Scripts\activate

# Mac
source venv/bin/activate
```

4. Install requirements
```shell
pip install -r requirements.txt
```

5. Create a directory `streamlit` with a `secrets.toml` file in the project root and add your [Google Gemini API key](https://aistudio.google.com/app/apikey)
```shell
# streamlit/scretes.toml
GOOGLE_API_KEY=""
```

## Running
```shell
streamlit run app.py
```

## Testing

```shell
# Run all tests
python3 -m unittest

# Run specific tests
python3 -m unittest tests.test_embedder
```