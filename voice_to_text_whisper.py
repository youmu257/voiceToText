import os
import sys
import whisper
import torch
import uuid
import shutil
from split_mp3 import split_mp3_ffmpeg
from srt_tool import combine_srt, write_srt
from datetime import datetime
from pydub import AudioSegment, silence
import tensorflow as tf
tf.compat.v1.disable_v2_behavior()
current_dir = os.path.dirname(os.path.abspath(__file__))
uvr_dir = os.path.join(current_dir, 'uvr5', 'ultimatevocalremovergui')
sys.path.append(uvr_dir)
from uvr5.uvr_cli import uvr_separate

# 幾分鐘切割一個音訊檔案
every_part_time_len = 10
device = "cuda" if torch.cuda.is_available() else "cpu"
# 模型，包含 tiny、base、small、medium、large
mode = "medium"
# 設定靜音閾值 (-40dBFS) & 最小靜音長度 (500ms)
VOLUME_THRESHOLD = -40
MIN_SILENCE_LEN = 500  # 500 毫秒

def generate_srt(input_file_name, file_name_list, new_srt_name=''):
    # 字幕資料夾
    dir_path = os.path.join("output", str(uuid.uuid1()))
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    destination_path = os.path.dirname(input_file_name)
    input_file_name = os.path.basename(input_file_name)

    # 啟用 CUDA 來使用 GPU
    torch.cuda.init()

    # 加載 Whisper 模型
    model = whisper.load_model("medium").to("cuda" if torch.cuda.is_available() else "cpu")
    print(f"加載模型完成 {datetime.now()}")

    for file_name in file_name_list:
        if not os.path.exists(file_name):
            print(f"找不到檔案 {file_name}")
            continue

        # 讀取音訊
        audio = AudioSegment.from_file(file_name)

        silent_ranges = silence.detect_silence(audio, min_silence_len=MIN_SILENCE_LEN, silence_thresh=VOLUME_THRESHOLD)

        # 轉換時間單位為秒
        silent_ranges = [(start / 1000, end / 1000) for start, end in silent_ranges]

        # 轉錄音檔
        result = model.transcribe(file_name, language="zh", word_timestamps=True)

        # 過濾靜音區段，確保時間正確
        filtered_segments = []
        for segment in result["segments"]:
            start_time, end_time = segment["start"], segment["end"]
            is_silent = any(start_time >= s[0] and end_time <= s[1] for s in silent_ranges)
            # 如果單一字幕長度超過120或空字串當作誤判
            srt_len = len(segment["text"])
            if not is_silent and srt_len < 120 and srt_len > 0:
                filtered_segments.append(segment)
        # 產生 SRT 字幕檔
        output_path = os.path.join(dir_path, f"{os.path.basename(file_name).replace('_(Vocals)', '')[:-4]}.srt")
        write_srt(filtered_segments, output_path)  # 確保 `write_srt()` 支援 segments 格式
        print(f"已轉換完成：{output_path} {datetime.now()}")
        # 移除臨時音檔
        os.remove(file_name)
    print("開始合併SRT")
    # 合併 SRT
    combine_srt(dir_path, input_file_name[:-4], len(file_name_list), every_part_time_len)
    print("開始移動字幕檔案")
    # 移動字幕檔案
    combine_srt_path = os.path.join(dir_path, f"{input_file_name[:-4]}.srt")
    destination_srt_path = os.path.join(destination_path, f"{input_file_name[:-4] if new_srt_name == '' else new_srt_name[:-4]}.srt")
    shutil.move(combine_srt_path, destination_srt_path)

    # 移除字幕資料夾
    os.rmdir(dir_path)

def remove_bgm(file_name_list, export_path="output"):
    convert_file_name_list = []
    for filename in file_name_list:
        # 分離音訊
        vocal_stem, instrumental_stem = uvr_separate(filename, export_path)
        convert_file_name_list.append(vocal_stem)
        os.remove(filename)
    return convert_file_name_list

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_file_name>")
        sys.exit(1)
    for index in range(1, len(sys.argv)):
        try:
            input_file_name = sys.argv[index]
            start_time = datetime.now()
            print(f"開始時間 {start_time}")
            file_dir = os.path.dirname(input_file_name)
            copy_file = os.path.join(file_dir, 'tmp.mp3')
            shutil.copy(input_file_name, copy_file)
            print("------------------1------------------------")
            # 切割檔案
            file_name_list = split_mp3_ffmpeg(copy_file, every_part_time_len * 60)
            print(f"切割檔案完成 {datetime.now()}")
            print(f"檔案數量 = {len(file_name_list)}")
            print("------------------2------------------------")
            if len(file_name_list) > 0:
                # 去除BGM
                vocals_file_name_list = remove_bgm(file_name_list, file_dir)
                print("------------------3------------------------")
                # 把切割檔案轉換成 SRT 字幕檔
                generate_srt(copy_file, vocals_file_name_list, input_file_name)
            print(f"花費時間 {datetime.now() - start_time}")
            # 移除 vocals.mp3
            os.remove(copy_file)
        except Exception as e:
            print(f"發生錯誤：{e}")
            continue

if __name__ == "__main__":
    main()
