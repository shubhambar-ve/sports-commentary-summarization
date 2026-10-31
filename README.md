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

## References
- Supplied Experiment 1, Experiment 3 and Experiment 6 course materials.
- https://huggingface.co/google/flan-t5-small
- https://huggingface.co/docs/transformers/model_doc/flan-t5
- https://huggingface.co/docs/hub/spaces-sdks-docker
- https://fastapi.tiangolo.com/
