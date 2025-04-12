from pydub import AudioSegment
import math
import os
import subprocess
import shutil

tmp_dir = ".\\tmp"
if os.path.exists(tmp_dir):
    shutil.rmtree(tmp_dir, ignore_errors=True)
os.makedirs(tmp_dir, exist_ok=True)

def split_mp3(file_path, chunk_length=30 * 60):
    # 讀取 MP3 文件
    audio = AudioSegment.from_mp3(file_path)
    # 轉換成豪秒
    chunk_length = chunk_length * 1000

    # 計算需要的分段數量
    total_length = len(audio)
    num_chunks = math.ceil(total_length / chunk_length)

    # 分割並輸出
    file_name_list = []
    for i in range(num_chunks):
        start_time = i * chunk_length
        end_time = start_time + chunk_length

        # 切割音頻
        chunk = audio[start_time:end_time]

        # 輸出切割後的音頻文件
        output_path = f"{file_path[:-4]}_part{i+1}.mp3"
        chunk.export(output_path, format="mp3")
        file_name_list.append(output_path)
        # print(f"已輸出：{output_path}")
    return file_name_list

# 用 ffmpeg 快很多
def split_mp3_ffmpeg(file_path, chunk_length=30 * 60):
    file_name = os.path.basename(file_path)
    # 設定 FFmpeg 切割命令
    command = [
        "ffmpeg", "-i", file_path,
        "-f", "segment", "-segment_time", str(chunk_length),
        "-segment_start_number", "1",
        "-c", "copy", os.path.join(tmp_dir, f"{file_name[:-4]}_part%d.mp3")
    ]
    try:
        # 執行 FFmpeg 命令
        subprocess.run(command, check=True)
        print("音訊檔切割成功！")
    except subprocess.CalledProcessError as e:
        print(f"切割失敗: {e}")
    destination_dir = os.path.dirname(file_path)
    file_name_list = list_files_and_move(tmp_dir, destination_dir)
    return file_name_list

def list_files_and_move(directory, destination_dir):
    # 獲取目錄下所有檔案
    temp_file_name_list = os.listdir(directory)
    # 回傳目標路徑下的檔案列表
    file_name_list = []
    for file_name in temp_file_name_list:
        # 確保只處理檔案，不處理資料夾
        source_file = os.path.join(directory, file_name)
        destination_file = os.path.join(destination_dir, file_name)
        
        if os.path.isfile(source_file) and is_audio_file_more_than_one_second(source_file):
            # 移動檔案
            shutil.move(source_file, destination_file)
            file_name_list.append(destination_file)
            print(f"已移動檔案: {file_name}")
        else:
            print(f"跳過非檔案: {file_name}")
    return file_name_list

def is_audio_file_more_than_one_second(file_path):
    """
    檢查音頻檔案的長度是否小於 1 秒。
    
    :param file_path: 音頻檔案的路徑
    :return: 如果檔案長度小於 1 秒，則返回 True，否則返回 False
    """
    try:
        # 使用 ffmpeg 查詢音檔的長度
        result = subprocess.run(
            ['ffmpeg', '-i', file_path], 
            stderr=subprocess.PIPE, stdout=subprocess.PIPE
        )
        output = result.stderr.decode()

        # 提取 Duration 行
        duration_line = [line for line in output.splitlines() if 'Duration' in line]

        if not duration_line:
            raise ValueError("檔案無效或無法讀取時長")

        # 解析時長，格式如 00:00:10.12
        duration_str = duration_line[0].split()[1]
        duration_parts = duration_str.split(":")

        # 將時長轉換為秒
        total_seconds = int(duration_parts[0]) * 3600 + int(duration_parts[1]) * 60 + float(duration_parts[2].replace(",", ""))
        # 檢查是否小於 1 秒
        return total_seconds > 1
    
    except Exception as e:
        print(f"錯誤：{e}")
        return False

def main():
    split_mp3_ffmpeg(
        "voice\\20210414_棉花糖雜談裡面到底是什麼鬼打開時我真是害怕極了祈菈．貝希毛絲.mp3",
        10 * 60 ,
    )


if __name__ == "__main__":
    main()
