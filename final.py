import streamlit as st
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

def check_valid_email(email):
    # write a function to check if the email is valid
    # example: return '@' in email and '.com' in email
    return '@' in email and '.com' in email

def run_mashup(singerName, numVideos, audioDuration, email):
    outputFileName="mashup.mp3"
    searchResults = ys.YoutubeSearch(singerName, numVideos).to_dict()

    with open("urls.txt", "w") as f:
        for i in range(min(numVideos,len(searchResults))):
            f.write("https://youtube.com"+searchResults[i]['url_suffix']+"\n")

    print("urls obtained")

    with open("urls.txt") as f:
        content_list = f.readlines()

    url_list = [x.strip() for x in content_list]

    for i in range(len(url_list)):
        link=url_list[i]
        youtubeObject = YouTube(link)
        youtubeObject.streams.first().download( filename='video_'+str(i)+".mp4")

    print("Download is completed successfully")

    for i in range(len(url_list)):
        video_file="video_"+str(i)+".mp4"
        audio_file="audio_"+str(i)+".mp3"
        sound = AudioSegment.from_file(video_file, format="mp4")
        sound = sound[10*1000:(audioDuration+10) * 1000]
        sound.export(audio_file, format="mp3")

    print("audio files exported")

    combined_audio=AudioSegment.from_file("default.wav")
    for i in range(len(url_list)):
        audio_file="audio_"+str(i)+".mp3"
        file = AudioSegment.from_file(audio_file)
        combined_audio+=file
        combined_audio+=AudioSegment.from_file("default.wav")

    combined_audio.export(outputFileName, format="mp3")

    print("Mashup Created")

    zip_file_name = "mashup.zip"
    with zipfile.ZipFile(zip_file_name, 'w') as myzip:
        myzip.write(outputFileName)

    print("Output file zipped successfully")

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
    print("Email sent successfully")


def main():
    st.title("Audio Mashup Generator")
    singerName = st.text_input("Singer Name", value="")
    numVideos = st.number_input("Number of Videos", value=10, min_value=10)
    audioDuration = st.number_input("Audio Duration (in seconds)", value=20, min_value=20)
    email = st.text_input("Email", value="")

    if not singerName or not email :
        st.error("Please fill in all the fields")
    elif not check_valid_email(email):
        st.error("Invalid email address")
    else:
        st.success("Thanks for registering")

    if st.button("Submit"):
        run_mashup(singerName, numVideos, audioDuration, email)
        st.success("Mashup created and sent to " + email)

if __name__ == '__main__':
    main()
