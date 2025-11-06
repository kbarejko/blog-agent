# 🤖 Blog Agent - Alternatywne wersje dla różnych platform AI

Główna wersja (`blog_agent.py`) używa Anthropic Claude API. Poniżej znajdziesz instrukcje jak dostosować agenta dla innych platform.

---

## 1. OpenAI (ChatGPT / GPT-4)

### Instalacja
```bash
pip install openai --break-system-packages
```

### Modyfikacje w kodzie

Zamień w pliku `blog_agent.py`:

```python
# ZAMIAST:
import anthropic
self.client = anthropic.Anthropic(api_key=self.api_key)
self.model = "claude-sonnet-4-20250514"

message = self.client.messages.create(
    model=self.model,
    max_tokens=4000,
    messages=[{"role": "user", "content": prompt}]
)
response_text = message.content[0].text

# UŻYJ:
from openai import OpenAI
self.client = OpenAI(api_key=self.api_key)
self.model = "gpt-4-turbo-preview"  # lub "gpt-4", "gpt-3.5-turbo"

response = self.client.chat.completions.create(
    model=self.model,
    max_tokens=4000,
    messages=[{"role": "user", "content": prompt}]
)
response_text = response.choices[0].message.content
```

### Zmienna środowiskowa
```bash
export OPENAI_API_KEY='sk-...'
```

---

## 2. Google Gemini

### Instalacja
```bash
pip install google-generativeai --break-system-packages
```

### Modyfikacje w kodzie

```python
# ZAMIAST importu anthropic:
import google.generativeai as genai

class BlogAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    # W metodach gdzie wysyłasz prompt:
    response = self.model.generate_content(prompt)
    response_text = response.text
```

### Zmienna środowiskowa
```bash
export GOOGLE_API_KEY='AIza...'
```

---

## 3. Ollama (Lokalne modele)

### Instalacja Ollama
```bash
# Linux/Mac
curl -fsSL https://ollama.com/install.sh | sh

# Ściągnij model
ollama pull llama3.1
ollama pull mistral
```

### Instalacja biblioteki Python
```bash
pip install ollama --break-system-packages
```

### Modyfikacje w kodzie

```python
# ZAMIAST importu anthropic:
import ollama

class BlogAgent:
    def __init__(self, model_name: str = "llama3.1"):
        self.model = model_name
    
    # W metodach gdzie wysyłasz prompt:
    response = ollama.chat(
        model=self.model,
        messages=[{'role': 'user', 'content': prompt}]
    )
    response_text = response['message']['content']
```

### Użycie
```python
# Nie potrzebujesz klucza API!
agent = BlogAgent(model_name="llama3.1")
```

---

## 4. Cohere

### Instalacja
```bash
pip install cohere --break-system-packages
```

### Modyfikacje w kodzie

```python
# ZAMIAST importu anthropic:
import cohere

class BlogAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("COHERE_API_KEY")
        self.client = cohere.Client(self.api_key)
        self.model = "command"
    
    # W metodach gdzie wysyłasz prompt:
    response = self.client.chat(
        message=prompt,
        model=self.model
    )
    response_text = response.text
```

### Zmienna środowiskowa
```bash
export COHERE_API_KEY='...'
```

---

## 5. Azure OpenAI

### Instalacja
```bash
pip install openai --break-system-packages
```

### Modyfikacje w kodzie

```python
# ZAMIAST importu anthropic:
from openai import AzureOpenAI

class BlogAgent:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.environ.get("AZURE_OPENAI_KEY"),
            api_version="2023-05-15",
            azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT")
        )
        self.model = "gpt-4"  # Nazwa twojego deployment
    
    # W metodach gdzie wysyłasz prompt:
    response = self.client.chat.completions.create(
        model=self.model,
        messages=[{"role": "user", "content": prompt}]
    )
    response_text = response.choices[0].message.content
```

### Zmienne środowiskowe
```bash
export AZURE_OPENAI_KEY='...'
export AZURE_OPENAI_ENDPOINT='https://your-resource.openai.azure.com/'
```

---

## 6. Hugging Face (Inference API)

### Instalacja
```bash
pip install huggingface_hub --break-system-packages
```

### Modyfikacje w kodzie

```python
# ZAMIAST importu anthropic:
from huggingface_hub import InferenceClient

class BlogAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("HF_TOKEN")
        self.client = InferenceClient(token=self.api_key)
        self.model = "meta-llama/Llama-2-70b-chat-hf"
    
    # W metodach gdzie wysyłasz prompt:
    response = self.client.text_generation(
        prompt=prompt,
        model=self.model,
        max_new_tokens=2000
    )
    response_text = response
```

### Zmienna środowiskowa
```bash
export HF_TOKEN='hf_...'
```

---

## 7. Perplexity AI

### Instalacja
```bash
pip install openai --break-system-packages  # Perplexity używa OpenAI SDK
```

### Modyfikacje w kodzie

```python
# ZAMIAST importu anthropic:
from openai import OpenAI

class BlogAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("PERPLEXITY_API_KEY")
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.perplexity.ai"
        )
        self.model = "llama-3.1-sonar-large-128k-online"
    
    # W metodach gdzie wysyłasz prompt:
    response = self.client.chat.completions.create(
        model=self.model,
        messages=[{"role": "user", "content": prompt}]
    )
    response_text = response.choices[0].message.content
```

### Zmienna środowiskowa
```bash
export PERPLEXITY_API_KEY='pplx-...'
```

---

## 8. Bash z curl (bez Pythona!)

Możesz użyć blog agenta bezpośrednio z bash i curl. Oto przykład:

```bash
#!/bin/bash

# Konfiguracja
API_KEY="twój-klucz-api"
TOPIC="Jak AI zmienia content marketing"

# Funkcja do wysyłania promptu
call_api() {
    local prompt="$1"
    curl -s https://api.anthropic.com/v1/messages \
        -H "x-api-key: $API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "content-type: application/json" \
        -d "{
            \"model\": \"claude-sonnet-4-20250514\",
            \"max_tokens\": 4000,
            \"messages\": [{\"role\": \"user\", \"content\": \"$prompt\"}]
        }" | jq -r '.content[0].text'
}

# 1. Tworzenie konspektu
echo "Tworzę konspekt..."
OUTLINE=$(call_api "Stwórz konspekt artykułu na temat: $TOPIC")
echo "$OUTLINE"

# 2. Pisanie sekcji (uproszczone)
echo "Piszę artykuł..."
ARTICLE=$(call_api "Na podstawie tego konspektu napisz pełny artykuł: $OUTLINE")

# 3. Zapisanie
echo "$ARTICLE" > article.md
echo "Gotowe! Artykuł zapisany w article.md"
```

---

## Porównanie platform

| Platforma | Zalety | Wady | Koszt |
|-----------|---------|------|-------|
| **Claude (Anthropic)** | Najlepsza jakość tekstów, świetne zrozumienie kontekstu | Wymaga API key | $$$ |
| **GPT-4 (OpenAI)** | Bardzo dobra jakość, popularne | Drogie | $$$$ |
| **GPT-3.5 (OpenAI)** | Tanie, szybkie | Średnia jakość | $ |
| **Gemini (Google)** | Darmowy tier, dobre multimodalne | Różna jakość | $-$$ |
| **Ollama** | Całkowicie darmowe, prywatne | Wymaga mocy obliczeniowej | Gratis |
| **Mistral** | Dobry balans jakości/ceny | Mniejsza dostępność | $$ |
| **Llama 3.1** | Open source, elastyczne | Trzeba hostować | Gratis/$$$ |

---

## Zalecenia

**Dla najlepszej jakości artykułów:**
1. Claude Sonnet 4 (używane domyślnie)
2. GPT-4 Turbo
3. Claude Opus 4

**Dla balansu jakość/cena:**
1. Claude Sonnet 4
2. GPT-3.5 Turbo
3. Mistral Large

**Dla prywatności/darmowe:**
1. Ollama + Llama 3.1
2. Local Mistral
3. Hugging Face (self-hosted)

---

## Szybka konwersja

Stworzyłem gotowe warianty w katalogu `variants/`:

```bash
variants/
├── blog_agent_openai.py      # Wersja dla OpenAI
├── blog_agent_gemini.py      # Wersja dla Google Gemini
├── blog_agent_ollama.py      # Wersja dla Ollama (lokalna)
└── blog_agent.sh             # Wersja bash (curl)
```

---

**Potrzebujesz pomocy z konkretną platformą?** 
Sprawdź dokumentację danej platformy lub otwórz issue na GitHubie!
