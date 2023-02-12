import youtube_search as ys
from pydub import AudioSegment
from pytube import YouTube
import sys
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

if len(sys.argv) != 5:
    print("Usage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
    sys.exit()
elif int(sys.argv[3])>=20 and int(sys.argv[2])>=10:
    singerName = sys.argv[1]
    numVideos = int(sys.argv[2])
    audioDuration = int(sys.argv[3])
    email = sys.argv[4]
else:
    print("Number of videos should be greater or equal to 10 and Audio Duration should be greater or equal to 20 seconds")
    sys.exit()

outputFileName="mashup.mp3"
searchResults = ys.YoutubeSearch(singerName, numVideos*2).to_dict()
count=0


with open("urls.txt", "w") as f:
    for i in range(min(numVideos,len(searchResults))):
        duration = searchResults[i]['duration']
        minutes, seconds = map(int, duration.split(':'))
        total_seconds = minutes * 60 + seconds
        if total_seconds<=600 and count <= numVideos:
            f.write("https://youtube.com"+searchResults[i]['url_suffix']+"\n")
            count+=1

print("urls obtained")

with open("urls.txt") as f:
    content_list = f.readlines()

url_list = [x.strip() for x in content_list]
combined_audio=AudioSegment.from_file("default.wav")

for i in range(len(url_list)):
    link=url_list[i]
    youtubeObject = YouTube(link)
    youtubeObject.streams.first().download( filename='video_'+str(i)+".mp4")
    video_file="video_"+str(i)+".mp4"
    audio_file="audio_"+str(i)+".mp3"
    sound = AudioSegment.from_file(video_file, format="mp4")
    sound = sound[10*1000:(audioDuration+10) * 1000]
    sound.export(audio_file, format="mp3")
    os.remove("video_"+str(i)+".mp4")
    file = AudioSegment.from_file(audio_file)
    combined_audio+=file
    combined_audio=combined_audio.append(file, crossfade=1000)
    os.remove("audio_"+str(i)+".mp3")

print("Download is completed successfully")

print("audio files exported")

combined_audio.export(outputFileName, format="mp3")

print("Mashup Created")

zip_file_name = "mashup.zip"
with zipfile.ZipFile(zip_file_name, 'w') as myzip:
    myzip.write(outputFileName)

print("Output file zipped successfully")
os.remove(outputFileName)

# Email the zipped file to the recipient
msg = MIMEMultipart()
msg['From'] = "uselessmail122@gmail.com"
msg['To'] = email
msg['Subject'] = "Mashup Output File"
part = MIMEBase('application', "octet-stream")
part.set_payload(open(zip_file_name, "rb").read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment', filename=zip_file_name)
msg.attach(part)

# Login to email account and send email
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("uselessmail122@gmail.com", "lkawsjsrpatufori")
server.sendmail("uselessmail122@gmail.com", email, msg.as_string())
server.quit()
os.remove(zip_file_name)

print("Email sent successfully")
