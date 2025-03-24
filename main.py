import os
import subprocess
import whisper
import argparse
from pathlib import Path

def extract_audio(video_path, audio_path):
    command = f'ffmpeg -i "{video_path}" -ac 1 -ar 16000 "{audio_path}" -y'
    subprocess.run(command, shell=True, check=True)
    print("[INFO] Audio extracted successfully.")

def transcribe_audio(audio_path, srt_output, model_size="medium", source_language=None):
    model = whisper.load_model(model_size)
    kwargs = {"task": "translate"}
    if source_language:
        kwargs["language"] = source_language
    
    result = model.transcribe(audio_path, **kwargs)
    
    # Print detected language for user feedback
    detected_lang = result.get("language", "unknown")
    print(f"[INFO] Detected language: {detected_lang}")

    with open(srt_output, "w", encoding="utf-8") as f:
        for i, segment in enumerate(result["segments"]):
            start_time = segment["start"]
            end_time = segment["end"]
            text = segment["text"]
            
            f.write(f"{i+1}\n")
            f.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
            f.write(f"{text}\n\n")
    
    print("[INFO] Transcription and translation completed.")

def format_time(seconds):
    millis = int((seconds - int(seconds)) * 1000)
    return f"{int(seconds//3600):02}:{int((seconds%3600)//60):02}:{int(seconds%60):02},{millis:03}"

def add_subtitles(video_path, srt_path, output_path):
    command = f'ffmpeg -i "{video_path}" -vf "subtitles={srt_path}" "{output_path}" -y'
    subprocess.run(command, shell=True, check=True)
    print("[INFO] Subtitles embedded into video.")

def process_video(input_video, output_video=None, model_size="medium", source_language=None, temp_dir="temp"):
    # Create temp directory if it doesn't exist
    os.makedirs(temp_dir, exist_ok=True)
    
    # Generate paths
    input_path = Path(input_video)
    if output_video is None:
        output_video = input_path.parent / f"{input_path.stem}_with_subs{input_path.suffix}"
    
    audio_file = Path(temp_dir) / "temp_audio.wav"
    srt_file = Path(temp_dir) / "output_subtitles.srt"
    
    try:
        # Run the pipeline
        extract_audio(str(input_path), str(audio_file))
        transcribe_audio(str(audio_file), str(srt_file), model_size, source_language)
        add_subtitles(str(input_path), str(srt_file), str(output_video))
        print("[INFO] Process completed. Output saved as:", output_video)
    finally:
        # Clean up temporary files
        if audio_file.exists():
            audio_file.unlink()
        if srt_file.exists():
            srt_file.unlink()

def main():
    parser = argparse.ArgumentParser(description="Transcribe and translate video subtitles using Whisper")
    parser.add_argument("input_video", help="Path to the input video file")
    parser.add_argument("-o", "--output", help="Path to the output video file (default: input_video_with_subs.mp4)")
    parser.add_argument("-m", "--model", choices=["small", "medium", "large"], 
                        default="medium", help="Whisper model size (default: medium)")
    parser.add_argument("-l", "--language", 
                        help="Source language code (optional, will auto-detect if not specified)")
    parser.add_argument("-t", "--temp-dir", default="temp",
                        help="Directory for temporary files (default: temp)")
    
    args = parser.parse_args()
    
    process_video(
        args.input_video,
        args.output,
        args.model,
        args.language,
        args.temp_dir
    )

if __name__ == "__main__":
    main() 