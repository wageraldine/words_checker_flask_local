from flask import Flask, render_template, request
#we are importing the function that makes predictions.
import os
from gtts import gTTS
from speech_to_text import record_voice, sentiment_classification


app = Flask(__name__)
app.config["DEBUG"] = False

app.config['SECRET_KEY'] = 'super secret key'

@app.route("/", methods=['GET','POST'])
def upload_file():
    #initial webpage load
    if request.method == 'GET':
        return render_template('index.html')
    else: # if request method == 'POST'
        text = record_voice()
        respon, result = sentiment_classification(text)
       
        results = []       
        
        if result == "Negative":    
            answer = "<br><br><div class='col text-center'>"+respon+" !</div>"
            results.append(answer)
            answer = "<div class='col text-center' style='color: red'>Ucapan : "+text+"</div>"
            results.append(answer)
        else:
            answer = "<br><br><div class='col text-center'>"+respon+"</div>"
            results.append(answer)
            answer = "<div class='col text-center'>Ucapan : "+text+"</div>"
            results.append(answer)

        language = 'id'
        myobj = gTTS(text=respon, lang=language, slow=False)         
        os.remove('static/result.mp3')
        myobj.save("static/result.mp3")         

        return render_template('index.html', len=len(results), results=results)    

# Create a running list of result
results = []

# Launch Everyting
if __name__ == '__main__':
    app.run()
