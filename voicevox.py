import requests
import json
import time
import re
import simpleaudio

host = "127.0.0.1"  # "localhost"でも可能だが、処理が遅くなる
port = 50021
sleep_time = 0.5    # 文節毎の間隔

def audio_query(text, speaker, max_retry):
    # 音声合成用のクエリを作成する
    query_payload = {"text": text, "speaker": speaker}
    for query_i in range(max_retry):
        r = requests.post(f"http://{host}:{port}/audio_query", 
                        params=query_payload, timeout=(10.0, 300.0))
        if r.status_code == 200:
            query_data = r.json()
            break
        time.sleep(1)
    else:
        raise ConnectionError("リトライ回数が上限に到達しました。 audio_query : ", "/", text[:30], r.text)
    return query_data
    
def synthesis(speaker, query_data,max_retry):
    synth_payload = {"speaker": speaker}
    for synth_i in range(max_retry):
        r = requests.post(f"http://{host}:{port}/synthesis", params=synth_payload, 
                          data=json.dumps(query_data), timeout=(10.0, 300.0))
        if r.status_code == 200:
            #音声ファイルを返す
            return r.content
        time.sleep(1)
    else:
        raise ConnectionError("音声エラー：リトライ回数が上限に到達しました。 synthesis : ", r)

def text_to_speech(texts, speaker=8, max_retry=20):
    if texts==False:
        texts="ちょっと、通信状態悪いかも？"
    texts=re.split("(?<=！|。|？)",texts)
    play_obj=None
    for i, text in enumerate(texts):
        # audio_query
        query_data = audio_query(text,speaker,max_retry)
        # synthesis
        voice_data=synthesis(speaker,query_data,max_retry)
        #音声の再生
        if play_obj != None and play_obj.is_playing():
            play_obj.wait_done()
        wave_obj=simpleaudio.WaveObject(voice_data,1,2,24000)
        if i != 0:
            time.sleep(sleep_time)
        play_obj=wave_obj.play()