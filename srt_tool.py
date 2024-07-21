from datetime import timedelta
import srt
import os
import zhconv


# 將文字轉換為 SRT 字幕
def write_srt(transcription, output_srt):
    def format_timestamp(seconds):
        ms = int(seconds * 1000)
        hours = ms // (1000 * 60 * 60)
        ms %= 1000 * 60 * 60
        minutes = ms // (1000 * 60)
        ms %= 1000 * 60
        seconds = ms // 1000
        ms %= 1000
        return f"{hours:02}:{minutes:02}:{seconds:02},{ms:03}"

    with open(output_srt, "w", encoding="utf-8") as srt_file:
        for i, segment in enumerate(transcription["segments"]):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()
            srt_file.write(f"{i + 1}\n{start} --> {end}\n{text}\n\n")


# 把 SRT 字幕黨合併，並調整時間和轉換簡中成繁中
def combine_srt(dir_path, file_name, max_file, every_part_time_len):
    i = 1
    while i <= max_file:
        part_file_name = os.path.join(dir_path, file_name + "_part" + str(i) + ".srt")
        if not os.path.exists(part_file_name):
            print(f"找不到檔案 {part_file_name}")
            i += 1
            continue
        # 讀取 SRT 文件
        with open(part_file_name, "r", encoding="utf-8") as f:
            srt_content = f.read()

        # 解析 SRT 字幕
        subs = list(srt.parse(srt_content))
        add_hour = timedelta(minutes=every_part_time_len * (i - 1))
        # 調整字幕時間
        for sub in subs:
            sub.start = sub.start + add_hour
            sub.end = sub.end + add_hour
            # 簡中轉繁中
            sub.content = zhconv.convert(sub.content, "zh-tw")
            # print(f"Start: {sub.start}, End: {sub.end}, Text: {sub.content}")

        # 保存編輯後的 SRT 文件
        with open(
            os.path.join(dir_path, file_name + ".srt"), "a", encoding="utf-8"
        ) as f:
            f.write(srt.compose(subs))
        # 移除轉換完成的字幕檔
        os.remove(part_file_name)
        i += 1
    print("組合字幕檔完成")


def main():
    combine_srt(
        "srt_946aa38a-4509-11ef-887e-0c9d92620f18",
        "20210414_棉花糖雜談裡面到底是什麼鬼",
        4,
    )


if __name__ == "__main__":
    main()
