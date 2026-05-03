from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import json
import re
import random
import os

def home(request):
    return render(request, 'Home.html')

def register(request):
    if request.method == 'POST':
        First_Name = request.POST['name']
        Email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirmation_password = request.POST['cnfm_password']
        if password == confirmation_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists, please choose a different one.')
                return redirect('register')
            else:
                if User.objects.filter(email=Email).exists():
                    messages.error(request, 'Email already exists, please choose a different one.')
                    return redirect('register')
                else:
                    user = User.objects.create_user(
                        username=username,
                        password=password,
                        email=Email,
                        first_name=First_Name,
                    )
                    user.save()
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
        return render(request, 'register.html')
    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.check_password(password):
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Login successful')
                    return redirect('/')
                else:
                    messages.error(request, 'Please check the password properly')
                    return redirect('login')
            else:
                messages.error(request, 'Please check the password properly')
                return redirect('login')
        else:
            messages.error(request, "Username doesn't exist")
            return redirect('login')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# Load NLP model and data at startup
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    from tensorflow.keras.models import Sequential, load_model
    from tensorflow.keras.layers import Input, Embedding, LSTM, LayerNormalization, Dense, Dropout
    from sklearn.preprocessing import LabelEncoder

    with open('static/Dataset/intents.json', 'r') as f:
        data = json.load(f)
    df_intents = pd.DataFrame(data['intents'])
    dic = {"tag": [], "patterns": [], "responses": []}
    for i in range(len(df_intents)):
        ptrns = df_intents[df_intents.index == i]['patterns'].values[0]
        rspns = df_intents[df_intents.index == i]['responses'].values[0]
        tag = df_intents[df_intents.index == i]['tag'].values[0]
        for j in range(len(ptrns)):
            dic['tag'].append(tag)
            dic['patterns'].append(ptrns[j])
            dic['responses'].append(rspns)
    df = pd.DataFrame.from_dict(dic)

    tokenizer = Tokenizer(lower=True, split=' ')
    tokenizer.fit_on_texts(df['patterns'])
    vacab_size = len(tokenizer.word_index)

    ptrn2seq = tokenizer.texts_to_sequences(df['patterns'])
    X = pad_sequences(ptrn2seq, padding='post')

    lbl_enc = LabelEncoder()
    y = lbl_enc.fit_transform(df['tag'])

    MODEL_PATH = 'static/model/model.h5'
    if os.path.exists(MODEL_PATH):
        import tensorflow as tf
        model = tf.keras.models.load_model(MODEL_PATH, compile=False, safe_mode=False)
    else:
        model = Sequential()
        model.add(Input(shape=(X.shape[1])))
        model.add(Embedding(input_dim=vacab_size+1, output_dim=100, mask_zero=True))
        model.add(LSTM(32, return_sequences=True))
        model.add(LayerNormalization())
        model.add(LSTM(32, return_sequences=True))
        model.add(LayerNormalization())
        model.add(LSTM(32))
        model.add(LayerNormalization())
        model.add(Dense(128, activation="relu"))
        model.add(LayerNormalization())
        model.add(Dropout(0.2))
        model.add(Dense(128, activation="relu"))
        model.add(LayerNormalization())
        model.add(Dropout(0.2))
        model.add(Dense(len(np.unique(y)), activation="softmax"))
        model.compile(optimizer='adam', loss="sparse_categorical_crossentropy", metrics=['accuracy'])
        model.fit(x=X, y=y, batch_size=10, epochs=50,
                  callbacks=[tf.keras.callbacks.EarlyStopping(monitor='accuracy', patience=3)])
        model.save(MODEL_PATH)

    NLP_READY = True
except Exception as e:
    NLP_READY = False
    print(f"NLP model not loaded: {e}")

def generate_answer(pattern):
    if not NLP_READY:
        return "Sorry, the AI model is not available right now."
    text = []
    txt = re.sub('[^a-zA-Z\']', ' ', pattern)
    txt = txt.lower().split()
    txt = " ".join(txt)
    text.append(txt)
    x_test = tokenizer.texts_to_sequences(text)
    x_test = np.array(x_test).squeeze()
    x_test = pad_sequences([x_test], padding='post', maxlen=X.shape[1])
    y_pred = model.predict(x_test)
    y_pred = y_pred.argmax()
    tag = lbl_enc.inverse_transform([y_pred])[0]
    responses = df[df['tag'] == tag]['responses'].values[0]
    return random.choice(responses)

@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        bot_response = generate_answer(user_message)
        return JsonResponse({'response': bot_response})
    return render(request, 'chatbot.html')
