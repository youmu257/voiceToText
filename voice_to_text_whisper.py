from split_mp3 import split_mp3_ffmpeg
from srt_tool import combine_srt, write_srt
from datetime import datetime
import whisper
import sys
import torch
import os
import uuid
import shutil

# 字幕資料夾
dir_path = os.path.join("output", str(uuid.uuid1()))
# 幾分鐘切割一個音訊檔案
every_part_time_len = 10
device = "cuda"
# 模型，包含 tiny、base、small、medium、large
mode = "medium"

def generate_srt(input_file_name, file_name_list):
    destination_path = os.path.dirname(input_file_name)
    input_file_name = os.path.basename(input_file_name)
    # Cuda allows for the GPU to be used which is more optimized than the cpu
    torch.cuda.init()

    # 加載 Whisper 模型 
    model = whisper.load_model(mode).to(device)
    print(f"加載模型完成 {datetime.now()}")
    for file_name in file_name_list:
        if not os.path.exists(file_name):
            print(f"找不到檔案 {file_name}")
            continue
        # 轉換 MP3 文件為音頻數據
        audio = whisper.load_audio(file_name)
        # 將音頻轉換為文字
        result = model.transcribe(audio)
        # 將轉錄結果寫入 SRT 文件
        output_path = os.path.join(dir_path, f"{os.path.basename(file_name)[:-4]}.srt")
        write_srt(result, output_path)
        print(f"已轉換完成：{output_path} {datetime.now()}")
        # 移除切割音檔
        os.remove(file_name)
    combine_srt(
        dir_path, input_file_name[:-4], len(file_name_list), every_part_time_len
    )
    # 移動字幕檔案
    combine_srt_path = os.path.join(dir_path, f"{input_file_name[:-4]}.srt")
    destination_srt_path = os.path.join(destination_path, f"{input_file_name[:-4]}.srt")
    print(combine_srt_path)
    print(destination_srt_path)
    shutil.move(combine_srt_path, destination_srt_path)


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file_name>")
        sys.exit(1)

    # 檢查資料夾是否存在，如果不存在則創建它
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    input_file_name = sys.argv[1]
    print(f"開始時間 {datetime.now()}")
    # 切割檔案
    file_name_list = split_mp3_ffmpeg(input_file_name, every_part_time_len * 60)
    # file_name_list = ["chilla_part1.mp3", "chilla_part2.mp3"]
    print(f"切割檔案完成 {datetime.now()}")
    print(f"檔案數量 = {len(file_name_list)}")
    if len(file_name_list) > 0:
        # 把切割檔案轉換成 SRT 字幕檔
        generate_srt(input_file_name, file_name_list)
    print(f"完成時間 {datetime.now()}")


if __name__ == "__main__":
    main()
