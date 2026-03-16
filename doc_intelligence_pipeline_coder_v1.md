Your runnable pipeline package is ready.

**Download it here:**
[Download the codebase](sandbox:/mnt/data/doc_intelligence_pipeline.zip)

### What’s inside the package

```
doc_intelligence_pipeline/

config.py

ingestion/
  batch_processor.py
  document_expander.py

ocr/
  ocr_router.py
  paddle_ocr.py
  numarkdown_ocr.py

layout/
  layout_graph.py
  table_reconstruction.py

templates/
  template_store.py
  template_retriever.py

extraction/
  deterministic_parser.py
  gliner_extractor.py
  numarkdown_extractor.py
  nuextract_extractor.py

consensus/
  consensus_engine.py

learning/
  failure_store.py

pipeline/
  extraction_pipeline.py

run_pipeline.py

requirements.txt
```

### Quick start

1. **Unzip**

```
unzip doc_intelligence_pipeline.zip
cd doc_intelligence_pipeline
```

2. **Install dependencies**

```
pip install -r requirements.txt
```

3. **Place test files**

```
./input_docs/
   sample.pdf
   sample.msg
   sample.jpg
```

4. **Run**

```
python run_pipeline.py
```

### Configure paths

Edit **config.py**

```python
CONFIG = {
 "input_directory": "./input_docs",
 "ocr_engine": "paddle",  # paddle | numarkdown | hybrid
 "execution_mode": "single",
 "ingestion_mode": "batch"
}
```

Your local models will be expected under:

```
/research/models
```

---

### Important note

This version is a **fully runnable skeleton** with working pipeline flow.
The following pieces are **stubbed placeholders** ready for you to plug real models:

* PaddleOCR call
* nuMarkdown call
* nuExtract call
* GLiNER call
* sentence-transformer embeddings
* Kafka consumer
* Ray distributed workers

The architecture and interfaces are already wired so you can drop those models in easily.

---
