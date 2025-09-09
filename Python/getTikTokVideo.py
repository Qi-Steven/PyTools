import re
import requests
import html

def clean_url(raw_url: str) -> str:
    # 替换掉转义符，解码成真正的 https 链接
    url = raw_url.replace("\\u002F", "/").replace("\\/", "/").replace("\\u0026", "&")
    url = html.unescape(url)  # 进一步解码 %3D %2F 之类
    return url

def get_tiktok_video(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    # 1. 获取 TikTok 页面 HTML
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("无法获取页面，状态码: " + str(response.status_code))

    html_text = response.text

    # 2. 提取无水印视频链接（playAddr）
    play_addr = re.search(r'"playAddr":"(.*?)"', html_text)
    if not play_addr:
        raise Exception("未找到视频地址，可能需要更新正则或增加 headers")
    
    video_url = clean_url(play_addr.group(1))

    # 3. 提取封面
    cover = re.search(r'"cover":"(.*?)"', html_text)
    cover_url = clean_url(cover.group(1)) if cover else None

    # 4. 提取标题
    title = re.search(r'"desc":"(.*?)"', html_text)
    title_text = title.group(1) if title else "无标题"

    return {
        "title": title_text,
        "video_url": video_url,
        "cover_url": cover_url
    }

def download_video(video_url, filename="tiktok.mp4"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    with requests.get(video_url, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"✅ 视频已保存为 {filename}")


if __name__ == "__main__":
    tiktok_url = "https://www.tiktok.com/@kokory03/video/7528349080473308423"  # 示例
    data = get_tiktok_video(tiktok_url)
    print("标题:", data["title"])
    print("封面:", data["cover_url"])
    print("无水印视频链接:", data["video_url"])

    # 下载视频
    download_video(data["video_url"], "demo.mp4")
