import os
from yt_dlp import YoutubeDL

def download_youtube_content(url, download_type="mp3", output_folder=r"D:\\User\\Downloads"):
    """
    下載 YouTube 影片/播放清單，並依需求儲存為 MP3 或 MP4 格式。
    
    :param url: YouTube 影片或播放清單網址
    :param download_type: 下載類型 ('mp3' 或 'mp4')
    :param output_folder: 下載儲存的目標資料夾
    """
    # 確保輸出目錄存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 基礎設定
    ydl_opts = {
        # 檔名格式：如有播放清單索引則顯示，沒有則僅顯示標題
        'outtmpl': os.path.join(output_folder, '%(playlist_index|000)s - %(title)s.%(ext)s'),
        'ignoreerrors': True,  # 遇到單一錯誤影片時繼續下載下一首
        'quiet': False,
    }

    # 根據選擇調整設定
    if download_type == "mp3":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',  # 音質位元率 (kbps)
                },
                {
                    'key': 'FFmpegMetadata',  # 寫入 ID3 標籤 metadata
                },
            ],
        })
    elif download_type == "mp4":
        ydl_opts.update({
            # 優先下載最佳 MP4 視訊 + 最佳 MP4 音訊，若無則自動合併為 mp4
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            'postprocessors': [
                {
                    'key': 'FFmpegMetadata',
                },
            ],
        })

    print(f"\n開始下載 ({download_type.upper()})：{url}")
    
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        
    print(f"\n下載完成！檔案已儲存至：{output_folder}")


if __name__ == "__main__":
    print("=== YouTube MP3 / MP4 下載工具 ===")
    
    # 1. 輸入網址
    target_url = input("請輸入 YouTube 影片或播放清單網址: ").strip()
    
    if not target_url:
        print("未輸入有效網址，程式結束。")
        exit()

    # 2. 選擇格式
    while True:
        choice = input("請選擇下載格式 (1: MP3 音訊, 2: MP4 影片) [預設 1]: ").strip()
        if choice in ["", "1"]:
            fmt = "mp3"
            break
        elif choice == "2":
            fmt = "mp4"
            break
        else:
            print("輸入無效，請輸入 1 或 2。")

    # 3. 執行下載
    download_youtube_content(target_url, download_type=fmt)






