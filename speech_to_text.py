import speech_recognition as sr
import pyaudio
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

r= sr.Recognizer()
print("Running")

p = pyaudio.PyAudio()

def record_voice():
    with sr.Microphone() as source:
        r.record(source, duration=5)  # Adjust for ambient
        print("Say something!")
        audio=r.listen(source)
    print("Runnnnnn")
    try:
        text = r.recognize_google(audio, language='id')
        print("Analyzing voice data  "+text)
        return text
    except Exception:
        print("Something went wrong")

def sentiment_classification(text):        
    modelname = 'model_cyberbulying_classification.sav'
    loaded_model = pickle.load(open(modelname, 'rb'))
    vec_path = 'vectorizer_cyberbulying.pickle'
    tfidf_file = open(vec_path, 'rb')
    tfidfconverter = pickle.load(tfidf_file)
    tfidf_file.close()

    text_vector = tfidfconverter.transform([text]).toarray()
    pred_text = loaded_model.predict(text_vector)  
            
    pkl_file = open('encoder_cyberbulying.pkl', 'rb')
    le = pickle.load(pkl_file) 
    pkl_file.close()
            
    pred_text = le.inverse_transform(pred_text)
    score = round(max(loaded_model.predict_proba(text_vector)[0])*100,2)
    result = str(pred_text[0].capitalize())

    if result == "Negative":
        respons = "Sebanyak " + str(score) + "% dari ucapan tersebut mengandung Ucapan Kasar"
    else:
        respons = "Ucapan tersebut tidak mengandung indikasi Ucapan Kasar"

    return respons, result