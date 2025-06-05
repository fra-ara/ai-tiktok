# 🎬 AI TikTok Story Generator

Projekt AI, który automatycznie generuje krótką historię na podstawie promptu tekstowego, zamienia ją na narrację głosową, a następnie łączy ją z gotowym plikiem wideo. Finalny film zawiera również automatycznie synchronizowane napisy.

---

## 📌 Funkcje projektu

- ✅ Generowanie historii przy użyciu modelu językowego (`distilgpt2`)
- ✅ Przekształcenie tekstu w głos przy użyciu modelu Bark (TTS)
- ✅ Podział tekstu na segmenty do lepszej synchronizacji z dźwiękiem
- ⚠️ (W TRAKCIE) Automatyczne generowanie napisów `.srt`
- ⚠️ (W TRAKCIE) Łączenie narracji audio, wideo i napisów w finalny film `.mp4`

---

## 🧠 Wykorzystane technologie

| Komponent | Opis |
|----------|------|
| `transformers` | Generowanie historii na podstawie promptu |
| `bark` | Generowanie głosu z tekstu |
| `moviepy` | Łączenie dźwięku z wideo |
| `pysrt` | Tworzenie napisów `.srt` |
| `pydub` | Manipulacja plikami dźwiękowymi |
| `ffmpeg` | Łączenie napisów z filmem |

---

## 🗂️ Struktura projektu

├── main.py # Główna logika całego pipeline'u
├── 1.mp4 # Przykładowe wejściowe wideo
├── requirements.txt # Lista zależności
└── README.md # Ten plik

---

## 🚀 Jak uruchomić

1. **Zainstaluj wymagane biblioteki**:
```bash
pip install -r requirements.txt
```

Upewnij się, że masz zainstalowany ffmpeg (dodany do PATH).

Uruchom skrypt:
```
python main.py
```

Efekt końcowy: plik final_XXXXXX.mp4 zawierający:

Wideo

Głos narratora

(opcjonalnie) napisy

## 📄 Licencja

## Licencje używanych modeli i bibliotek

- Model `distilgpt2` – licencja MIT – https://huggingface.co/distilgpt2
- Model `Bark` – licencja MIT – https://github.com/suno-ai/bark
- Biblioteki MoviePy, pydub – licencja MIT
- pysrt – licencja BSD (zgodna z MIT)

