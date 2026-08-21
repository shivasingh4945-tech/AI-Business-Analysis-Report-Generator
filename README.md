# AI Business Analysis Report Generator

Upload a CSV, get a written analysis back. This is a FastAPI service that computes summary
statistics locally with pandas, sends that summary to a LLaMA model hosted on Groq, and returns
the model's report — either rendered in the browser or as JSON from the API.

The point is that the numbers are never guessed. `pandas.describe()` does the arithmetic, and the
LLM is only asked to interpret and write up figures it has been handed — which keeps the statistics
in the report honest.

## How it works

```
CSV upload  ->  pandas.describe()  ->  prompt template  ->  Groq (LLaMA)  ->  report
                     + df.head()       (LangChain)             (HTML or JSON)
```

- **pandas** computes the summary statistics and takes a sample of rows.
- **LangChain** (`PromptTemplate`) builds the prompt from those two pieces.
- **Groq** runs the LLaMA model and returns the write-up.
- **FastAPI** handles the upload and returns the result — as a rendered page (`POST /`) or as JSON
  (`POST /api/reports`) — in a single request.

## Setup

### Option A: Docker

1. Get a free API key from https://console.groq.com/keys, then create your `.env`:
   ```
   cp .env.example .env
   ```
   Open `.env` and paste your key into `GROQ_API_KEY`.

2. Build and run:
   ```
   docker compose up --build
   ```
   Open http://localhost:8000 and upload a CSV.

### Option B: Local Python

1. Clone and enter the repo:
   ```
   git clone https://github.com/shivasingh4945-tech/AI-Business-Analysis-Report-Generator.git
   cd AI-Business-Analysis-Report-Generator
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Get a free API key from https://console.groq.com/keys, then create your `.env`:
   ```
   cp .env.example .env
   ```
   Open `.env` and paste your key into `GROQ_API_KEY`.

4. Run it:
   ```
   uvicorn main:app --reload
   ```
   Open http://127.0.0.1:8000 and upload a CSV. Interactive API docs are at `/docs`.

## API

`POST /api/reports` accepts a multipart CSV upload and returns the report as JSON:

```
curl -F "file=@data.csv" http://localhost:8000/api/reports
```

## Configuration

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `GROQ_API_KEY` | yes | — | Your Groq API key |
| `GROQ_MODEL` | no | `llama-3.3-70b-versatile` | Which Groq model to use |

`.env` is gitignored. Do not commit it.

## Notes and limitations

- Only the summary statistics and the first five rows are sent to the API, not the full dataset.
  That keeps requests small, but it also means the model cannot see row-level detail beyond the sample.
- Very wide CSVs produce a large `describe()` payload and can run into the model's context limit.
- There is no upload size cap yet, and reports are not persisted between requests.


## License

MIT — see [LICENSE](LICENSE).
