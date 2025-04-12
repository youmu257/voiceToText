import srt
import os

def reindex_srt_file(dir_path, file_name):
    file_path = os.path.join(dir_path, file_name)
    if not os.path.exists(file_path):
        print(f"找不到檔案 {file_path}")
        return
    # 讀取 SRT 文件
    with open(file_path, "r", encoding="utf-8") as f:
        srt_content = f.read()

    # 解析 SRT 字幕
    subs = list(srt.parse(srt_content))

    # 保存編輯後的 SRT 文件
    with open(
        os.path.join(dir_path + "_new", file_name), "a", encoding="utf-8"
    ) as f:
        f.write(srt.compose(subs, reindex = True))
    print("轉換字幕檔完成")

def reindex_srt_files_in_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.srt'):
                file_path = os.path.join(root, file)
                print(f"Reindexing file: {file_path}")
                reindex_srt_file(folder_path, file)
def main():
    reindex_srt_files_in_folder("tmp")


if __name__ == "__main__":
    main()