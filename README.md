# AI Business Analysis Report Generator

Upload a CSV, get a written analysis back. This is a small Flask app that computes summary
statistics locally with pandas, sends that summary to a LLaMA model hosted on Groq, and renders
the model's report in the browser.

The point is that the numbers are never guessed. `pandas.describe()` does the arithmetic, and the
LLM is only asked to interpret and write up figures it has been handed — which keeps the statistics
in the report honest.

## How it works

```
CSV upload  ->  pandas.describe()  ->  prompt template  ->  Groq (LLaMA)  ->  rendered report
                     + df.head()       (LangChain)
```

- **pandas** computes the summary statistics and takes a sample of rows.
- **LangChain** (`PromptTemplate`) builds the prompt from those two pieces.
- **Groq** runs the LLaMA model and returns the write-up.
- **Flask** handles the upload and renders the result.

## Setup

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
   python app.py
   ```
   Open http://127.0.0.1:5000 and upload a CSV.

## Configuration

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `GROQ_API_KEY` | yes | — | Your Groq API key |
| `GROQ_MODEL` | no | `llama-3.3-70b-versatile` | Which Groq model to use |
| `FLASK_SECRET_KEY` | no | random per run | Flask session signing key |

`.env` is gitignored. Do not commit it.

## Notes and limitations

- Only the summary statistics and the first five rows are sent to the API, not the full dataset.
  That keeps requests small, but it also means the model cannot see row-level detail beyond the sample.
- Very wide CSVs produce a large `describe()` payload and can run into the model's context limit.
- There is no upload size cap yet, and reports are not persisted between requests.

## Credits

Built on the [genAI-data-analysis-report-generator](https://github.com/amlanmohanty1/genAI-data-analysis-report-generator)
project by Amlan Mohanty, released under the MIT License. This version adds environment-based
configuration, input and API-key validation, a configurable model, and assorted fixes.

Maintained by Shiva Singh.

## License

MIT — see [LICENSE](LICENSE).
