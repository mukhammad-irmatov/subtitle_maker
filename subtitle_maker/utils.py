from pytube import YouTube


def parse_srt_file(srt_data):
    # Split the SRT file into individual subtitles
    srt_subtitles = srt_data.split('\n\n')
    # Iterate through each subtitle and extract its metadata and content
    subtitles = []
    for srt_subtitle in srt_subtitles:
        lines = srt_subtitle.split('\n')
        subtitle_num = lines[0]
        if len(lines)>1:
            subtitle_times = lines[1]
            start, end = subtitle_times.split(' --> ')
            subtitle_text = ' '.join(lines[2:])
            subtitles.append((subtitle_num, start, end, subtitle_text))

    return subtitles


def download_video(link):
    yt = YouTube(link)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    try:
        video_file = yt.download(output_path='media/videos', filename='output.mp4')
    except:
        print("An error has occurred")
    return video_file