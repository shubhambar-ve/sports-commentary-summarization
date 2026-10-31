---
title: Sports Commentary Summarization
emoji: 🏏
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
---
# MatchBrief: Sports Commentary Summarization

A small ESE project: vanilla HTML interface + FastAPI + pretrained FLAN-T5-small, with an explicitly labelled offline extractive baseline. No API key, training, paid LLM API, database or scraped dataset is needed. Internet is needed for installation and the first model download.

## Quick start (Windows, Python 3.11)
Open a terminal in this folder:
```powershell
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt
python -m uvicorn app:app --host 0.0.0.0 --port 7860
```
Open http://localhost:7860 and http://localhost:7860/docs . Choose a sample, keep FLAN-T5 selected, then Generate recap. First use downloads model weights; allow several minutes. Use short English inputs. The 512-token limit includes instructions and is checked without silent truncation.

Linux/macOS: use `python3 -m venv .venv` and `source .venv/bin/activate`. For macOS, install `torch==2.6.0` from normal PyPI instead of the CPU index. If PowerShell activation is blocked, call `.venv\Scripts\python.exe` directly for pip and uvicorn.

## Docker
Install and start Docker Desktop, then:
```sh
docker compose up --build
```
Open http://localhost:7860 . Stop with `docker compose down`. The named model-cache volume preserves downloads. Alternatively:
```sh
docker build -t sports-commentary .
docker run --rm -p 7860:7860 sports-commentary
```
The image uses Python 3.11 and a non-root user. CPU PyTorch avoids downloading CUDA packages. The port can be changed through PORT. Docker files are provided; no Docker engine was available in the authoring environment, so the image was not built there.

## Publish to GitHub
1. Sign in to GitHub and create a new empty repository named `sports-commentary-summarization`.
2. In this folder run the commands below, replacing YOUR_USERNAME. Do not commit `.venv`, tokens or private files.
```sh
git init
git add .
git commit -m "Add sports commentary summarization ESE project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/sports-commentary-summarization.git
git push -u origin main
```
Use GitHub's browser sign-in or credential manager if prompted. Alternatively upload the extracted files using GitHub's Add file > Upload files. Upload files, not the ZIP.

## Public deployment: Hugging Face Docker Spaces
1. Sign in at https://huggingface.co and create a new Space.
2. Name it `sports-commentary-summarization`, select **Docker**, blank template and **Public** visibility. Select available CPU hardware and review any cost shown before proceeding.
3. Upload this folder's files to the Space root. In particular retain README.md (with its YAML header), Dockerfile, requirements.txt, core.py, app.py, static/index.html and data/samples.json.
4. Wait for the build to finish. Open the App tab and run a short FLAN-T5 example. The first request downloads the model. Check Logs if it fails.
5. Copy the actual Space URL and GitHub URL into report/config.json. Do not submit example URLs as real links.
6. Run the evaluation and report commands below, add your actual LLM observations, and regenerate the report.

The existing Sites hosting option does not run this Python/PyTorch container. No GitHub repository or authenticated external cloud deployment was created in the authoring environment. The report records this explicitly.

## Evaluation and report
```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python evaluate.py --engine extractive
python evaluate.py --engine flan-t5
python build_report.py
```
Evaluation saves real outputs to `report/results-ENGINE.json`. It records exceptions as errors. Three fictional, hand-authored examples are demonstration fixtures, not a benchmark. References are supplied for manual comparison. Word reduction is a length metric, not accuracy. Manually check winner, score and major events against the input.

Edit `report/config.json` with your name, UID, college, faculty, GitHub and deployment URLs. Blank values are visibly marked. `build_report.py` creates an editable Markdown report and a PDF with the requested seven sections, workflow figure and measured results. It only includes available evaluation output. If you add screenshots, use your actual running application; do not present a design illustration as execution evidence.

## Course mapping
- Experiment 1: tokenization and encoder-decoder Transformer inference in `core.generate`.
- Experiment 3: autoregressive decoder generation, greedy vs beam decoding and maximum new tokens. This transfers the concept; it does not reproduce the GPT-2 lab.
- Experiment 6: FLAN-T5-small, FastAPI, Uvicorn and Docker packaging.
- Experiments 7/8: deployment extension only; AWS/GCP deployment is not claimed.
- Experiments 2/5: masked language modelling and QA fine-tuning are deliberately outside this simple project's scope.

## Explain it in a two-minute demo
1. Load Football commentary and identify the 2-1 final score in the input.
2. Run the baseline and explain sentence ranking and chronological ordering.
3. Switch to FLAN-T5, generate a recap, and compare score, names, omissions and length.
4. Switch from beam search to greedy and observe whether the wording changes.
5. Open /docs and demonstrate POST /summarize.
6. Show Dockerfile and explain image vs running container.

## Viva answers
- **Did you train a model?** No. This is inference using a pretrained instruction-tuned model.
- **Why T5 instead of BERT MLM?** T5 encodes input and generates a variable-length summary; MLM predicts masked tokens.
- **What is autoregressive decoding?** Each generated token depends on earlier generated tokens and the encoded input.
- **Does a shorter summary mean a better summary?** No. It can omit the winner or change the score.
- **What does the baseline do?** It ranks source sentences using event words and outcome cues; it is not machine learning.
- **Why Docker?** It packages the runtime and dependencies for repeatable execution.
- **Limitations?** Small general-purpose model, no sports fine-tuning, 512-token input budget, possible hallucinations and CPU latency. No live feed, audio transcription or full-match long-document support.

## Files
`core.py`: engines; `app.py`: API; `static/`: UI; `data/`: examples; `tests/`: checks; `evaluate.py`: real results; `build_report.py`: reproducible report; `report/config.json`: identity and links.

## References
- Supplied Experiment 1, Experiment 3 and Experiment 6 course materials.
- https://huggingface.co/google/flan-t5-small
- https://huggingface.co/docs/transformers/model_doc/flan-t5
- https://huggingface.co/docs/hub/spaces-sdks-docker
- https://fastapi.tiangolo.com/
