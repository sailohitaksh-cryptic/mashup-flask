from flask import Flask, request
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


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        singerName = request.form.get("singerName")
        numVideos = int(request.form.get("numVideos"))
        audioDuration = int(request.form.get("audioDuration"))
        email = request.form.get("email")

        run_mashup(singerName, numVideos, audioDuration, email)

        return "Mashup created and sent to " + email
    return '''
        <html>
    <head>
        <style>
            form {
                width: 500px;
                margin: auto;
                padding: 20px;
                background-color: lightgray;
                border-radius: 10px;
                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
            }
            label {
                display: block;
                margin-bottom: 10px;
                font-weight: bold;
                font-size: 16px;
            }
            input[type="text"], input[type="email"] {
                width: 100%;
                padding: 10px;
                margin-bottom: 20px;
                font-size: 16px;
                border-radius: 5px;
                border: none;
                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            }
            input[type="submit"] {
                width: 100%;
                padding: 10px;
                background-color: green;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
            }
            .error {
                color: red;
                font-size: 14px;
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <form onsubmit="return validateForm()" method="post">
            <label>Singer Name:</label>
            <input type="text" name="singerName" id="singerName">
            <div class="error" id="singerNameError"></div>
            <label>Number of Videos:</label>
            <input type="text" name="numVideos" id="numVideos">
            <div class="error" id="numVideosError"></div>
            <label>Audio Duration (in seconds):</label>
            <input type="text" name="audioDuration" id="audioDuration">
            <div class="error" id="audioDurationError"></div>
            <label>Email:</label>
            <input type="email" name="email" id="email">
            <div class="error" id="emailError"></div>
            <input type="submit" value="Submit">
        </form>
    </body>
    <script>
        function validateForm() {
            var singerName = document.getElementById("singerName").value;
            var numVideos = document.getElementById("numVideos").value;
            var audioDuration = document.getElementById("audioDuration").value;
            var email = document.getElementById("email").value;
            var isValid = true;

            if (!singerName) {
                document.getElementById("singerNameError").innerHTML = "Singer name is required";
                isValid = false;
            } else {
                document.getElementById("singerNameError").innerHTML = "";
            }

            if (!numVideos || numVideos < 10) {
                document.getElementById("numVideosError").innerHTML ="Number of videos must be at least 10";
isValid = false;
} else {
document.getElementById("numVideosError").innerHTML = "";
}
        if (!audioDuration || audioDuration < 20) {
            document.getElementById("audioDurationError").innerHTML =
                "Audio duration of each clip must be at least 20 seconds";
            isValid = false;
        } else {
            document.getElementById("audioDurationError").innerHTML = "";
        }

        if (!email) {
            document.getElementById("emailError").innerHTML = "Email is required";
            isValid = false;
        } else {
            document.getElementById("emailError").innerHTML = "";
        }

        return isValid;
    }
</script>
</html>            
    '''

def run_mashup(singerName, numVideos, audioDuration, email):
    outputFileName="mashup.mp3"
    searchResults = ys.YoutubeSearch(singerName, numVideos*2).to_dict()
    

    with open("urls.txt", "w") as f:
        for i in range(min(numVideos,len(searchResults))):
            duration = searchResults[i]['duration']
            minutes, seconds = map(int, duration.split(':'))
            total_seconds = minutes * 60 + seconds
            if total_seconds<=600:
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

if __name__ == "main":
    app.run(debug=True)
