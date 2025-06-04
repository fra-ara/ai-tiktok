# 🔧 Importy
import os
import shlex
import uuid
import tempfile
import subprocess
import pysrt
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from transformers import pipeline
from pydub import AudioSegment
from pydub.playback import play

from bark import SAMPLE_RATE, generate_audio
from scipy.io.wavfile import write as write_wav

os.environ["TOKENIZERS_PARALLELISM"] = "false"
# Wyłączenie ostrzeżeń tokenizera HuggingFace

# 🔪 Pomocnicza funkcja do dzielenia tekstu
# Dzielimy tekst na mniejsze fragmenty (chunks)
#   robimy to aby generowac audio w kawałkach (Bark działa lepiej z krótkimi tekstami)
def split_text(text, max_words=40):
    words = text.split()
    return [' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

# 🧠 Klasa do przetwarzania filmu krok po kroku
class TikTokStoryCreator:
    def __init__(self, video_path: str, prompt: str):
        self.video_path = video_path
        self.prompt = prompt
        self.story_text = ""
        self.audio_path = ""
        self.subtitles_path = ""
        self.output_path = ""

        self.generator = pipeline("text-generation", model="distilgpt2")
        # Ładuje model do generowania tekstu

    def generate_story(self) -> str:
        """1️⃣ Generowanie historii z prompta"""
        result = self.generator(
            self.prompt,
            max_new_tokens=500,
            temperature=0.9,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            num_return_sequences=1
        )
        full_text = result[0]['generated_text']
        self.story_text = full_text[len(self.prompt):].strip()
        print("📜 Story generated:")
        print(self.story_text)
        return self.story_text

    def synthesize_audio(self, text: str) -> str:
        # Tworzy plik .wav w folderze tymczasowym. Dzieli historię na fragmenty.
        #   Dla każdego fragmentu: generuje audio za pomocą Bark, zapisuje jako .wav, dodaje do całości + 0.5s ciszy między segmentami.
        # Zapisuje finalne audio i odtwarza je.

        """2️⃣ Konwersja historii na głos (TTS z Bark) — z dzieleniem"""
        tmp_audio_path = tempfile.mktemp(suffix=".wav")
        print("🎤 Generating audio with Bark...")

        chunks = split_text(text, max_words=40)
        combined_audio = AudioSegment.silent(duration=0)

        for idx, chunk in enumerate(chunks):
            print(f"🧩 Generating chunk {idx + 1}/{len(chunks)}...")
            audio_array = generate_audio(chunk)
            chunk_path = tempfile.mktemp(suffix=".wav")
            write_wav(chunk_path, SAMPLE_RATE, audio_array)
            segment = AudioSegment.from_wav(chunk_path)
            combined_audio += segment + AudioSegment.silent(duration=500)

        combined_audio.export(tmp_audio_path, format="wav")
        self.audio_path = tmp_audio_path
        print(f"🔊 Audio saved to: {self.audio_path}")

        try:
            play(combined_audio)
        except Exception as e:
            print(f"⚠️ Could not play audio automatically: {e}")

        return self.audio_path

    # TO DO: finish

    # def generate_subtitles(self, text: str, audio_path: str) -> str:
    # Tworzy plik .srt na podstawie długości audio i ilości zdań.
    # W przyszłości: zsynchronizowane napisy.

    #     """3️⃣ Generowanie napisów SRT na podstawie długości audio"""
    #     tmp_srt_path = tempfile.mktemp(suffix=".srt")
    #     sentences = [s.strip() for s in text.split('.') if s.strip()]
    #     subs = pysrt.SubRipFile()
    #     clip = AudioFileClip(audio_path)
    #     total_duration = clip.duration
    #     duration_per_sentence = total_duration / len(sentences)
    #
    #     for i, sentence in enumerate(sentences):
    #         start_time = i * duration_per_sentence
    #         end_time = start_time + duration_per_sentence
    #         subs.append(
    #             pysrt.SubRipItem(
    #                 index=i + 1,
    #                 start=pysrt.SubRipTime(seconds=start_time),
    #                 end=pysrt.SubRipTime(seconds=end_time),
    #                 text=sentence
    #             )
    #         )
    #     subs.save(tmp_srt_path, encoding='utf-8')
    #     self.subtitles_path = tmp_srt_path
    #     print(f"📝 Subtitles saved to: {self.subtitles_path}")
    #     return self.subtitles_path
    #

    # TO DO: finish

    # Łączy oryginalny film z nowym audio.
    # Nakłada napisy z .srt za pomocą ffmpeg.

    # def merge_video_audio_subtitles(self, audio_path: str, subtitles_path: str) -> str:
    #     """4️⃣ Łączenie video, audio i napisów w finalny plik MP4"""
    #     output_path = f"final_{uuid.uuid4().hex[:8]}.mp4"
    #
    #     video = VideoFileClip(self.video_path)
    #     audio = AudioFileClip(audio_path)
    #     final = video.with_audio(audio)
    #     final.write_videofile("temp_video_with_audio.mp4", codec='libx264', audio_codec='aac')
    #
    #     subs_filter = f'subtitles={shlex.quote(subtitles_path)}'
    #
    #     command = [
    #         "ffmpeg",
    #         "-i", "temp_video_with_audio.mp4",
    #         "-vf", subs_filter,
    #         "-c:a", "copy",
    #         output_path
    #     ]
    #
    #     subprocess.run(command, check=True)
    #     self.output_path = output_path
    #     print(f"✅ Final video saved to: {self.output_path}")
    #     return self.output_path

    # ⚠️ UWAGA:
    # Funkcje generate_subtitles() i merge_video_audio_subtitles() są obecnie zakomentowane.
    # Powód: możliwe problemy z dokładnym timingiem napisów lub niedokończona implementacja FFmpeg.
    # W przyszłości planowane:
    # ✅ Synchronizacja napisów z audio na podstawie timestampów
    # ✅ Pełne renderowanie finalnego wideo z głosem + napisami

    def run_all(self):
        """🚀 Wykonuje wszystkie kroki po kolei"""
        story = self.generate_story()
        audio = self.synthesize_audio(story)
        # subs = self.generate_subtitles(story, audio)
        # final = self.merge_video_audio_subtitles(audio, subs)
        return audio

# 📝 Przykład użycia
prompt = "Imagine you are a writer, write me a story about a wooden boy in todays era, make it long enoght to read it in like 1:30 min +-"
video_path = "1.mp4"

creator = TikTokStoryCreator(video_path=video_path, prompt=prompt)
final_video = creator.run_all()
