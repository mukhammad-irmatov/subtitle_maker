import os
import time
import subprocess
import srt
from django.conf import settings
from django.http import Http404, FileResponse
from django.shortcuts import render, redirect
import requests
from moviepy.video.io.VideoFileClip import VideoFileClip

from subtitle_maker.utils import parse_srt_file, download_video
from subtitleapp.models import Subtitle


def homePageView(request):
    if request.method == 'POST':
        # Get the YouTube video URL from the user input
        youtube_url = request.POST['url']
        url = settings.API_URL
        print(url)
        data = {
            "data":
                [youtube_url]
                }
        if not Subtitle.objects.filter(name=youtube_url).exists():
            response = requests.post(url, json=data)
            print(response.status_code)
            result = response.json()
            Subtitle.objects.create(
                name=youtube_url,
                output_text=result['data'][0]
            )
            request.session['youtube_link'] = youtube_url
            return redirect("resultpage")
        else:
            request.session['youtube_link'] = youtube_url
            time.sleep(5)
            return redirect("resultpage")

    # Render the template for the user to enter the YouTube URL
    return render(request, 'index.html')


def videopage(request):
    if request.method == "GET":
        # youtube_link = request.session.get('youtube_link', '')
        youtube_link = "https://www.youtube.com/shorts/XXlA7Ka1L5s"
        output_text = Subtitle.objects.filter(name=youtube_link).values_list('output_text', flat=True).first()
        if output_text:
            try:
                result = parse_srt_file(output_text)
            except Exception as e:
                result = None
                print(f"Error parsing subtitle file: {e}")
        else:
            result = None

        video_file = download_video(youtube_link)
        # Write the subtitles to a file in SRT format
        subtitles = [srt.Subtitle(index=x[0], start=srt.srt_timestamp_to_timedelta(x[1]),
                                  end=srt.srt_timestamp_to_timedelta(x[2]), content=x[3]) for x in result]
        with open('media/srt_files/subtitles.srt', 'w') as f:
            f.write(srt.compose(subtitles))
        video_clip = VideoFileClip(video_file)
        subtitles = 'media/srt_files/subtitles.srt'

        # Run FFmpeg command to add subtitle to video
        cmd = f'ffmpeg -i {video_clip} -i {subtitles} -c:s mov_text -c:v copy -c:a copy -map 0:v:0 -map 0:a:0 -map 1:s:0'
        subprocess.call(cmd, shell=True)
        current_host = request.get_host()
        video_file_path = f"{current_host}/media/videos/output.mp4"
        context = {
            'youtube_link': youtube_link,
            'result': result,
            "video": video_file_path
        }
        return render(request, 'video.html', context=context)

    elif request.method == "POST":
        youtube_link = request.session.get('youtube_link', '')
        new_text = request.POST.get('new_text')
        subtitle, created = Subtitle.objects.get_or_create(name=youtube_link)
        subtitle.output_text = new_text
        subtitle.save()
        return redirect('resultpage')

    else:
        # handle unsupported request methods
        raise Http404("Unsupported request method")