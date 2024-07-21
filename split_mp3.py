from pydub import AudioSegment
import math


def split_mp3(file_path, chunk_length=30 * 60 * 1000):
    # 讀取 MP3 文件
    audio = AudioSegment.from_mp3(file_path)

    # 計算需要的分段數量
    total_length = len(audio)
    num_chunks = math.ceil(total_length / chunk_length)

    # 分割並輸出
    fileNameList = []
    for i in range(num_chunks):
        start_time = i * chunk_length
        end_time = start_time + chunk_length

        # 切割音頻
        chunk = audio[start_time:end_time]

        # 輸出切割後的音頻文件
        output_path = f"{file_path[:-4]}_part{i+1}.mp3"
        chunk.export(output_path, format="mp3")
        fileNameList.append(output_path)
        # print(f"已輸出：{output_path}")
    return fileNameList


def main():
    split_mp3(
        "20210414_棉花糖雜談裡面到底是什麼鬼打開時我真是害怕極了祈菈．貝希毛絲.mp3",
        10 * 60 * 1000,
    )


if __name__ == "__main__":
    main()
