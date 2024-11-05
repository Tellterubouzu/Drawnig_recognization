import torch
from PIL import Image
from transformers import AutoModel ,AutoTokenizer, BitsAndBytesConfig
import requests
import time
from voicevox_adapter import VoicevoxAdapter
from play_sound import PlaySound
class vlm():
    def __init__(self):
        model_id = "openbmb/MiniCPM-V-2_6"
        quantization_config = BitsAndBytesConfig(load_in_4bit=True)
        self.model = AutoModel.from_pretrained(model_id, trust_remote_code=True,
            attn_implementation='sdpa', torch_dtype=torch.bfloat16,quantization_config = quantization_config).eval().cuda()
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.tts_model= VoicevoxAdapter()
        self.tts("初期設定完了です。、コマンドラインに表示されているローカルのアドレスにアクセスしてね")
        self.msgs = []
    def create_chat(self,role:str,image=None,question=str):
        # formating chat to msgs = [{'role': 'user', 'content': [image, question]}]
        self.msgs.append({'role': 'user', 'content': [image, question]})

    
    def predict(self,image,prompt):
        # Instruct the model to create a caption in japanese
        if prompt == "" or prompt == None:
            prompt = "この画像について詳しく日本語で説明してください"
        self.create_chat('role',image,prompt)
        res = self.model.chat(
            image = None,
            msgs =self.msgs,
            tokenizer = self.tokenizer
        )
        self.msgs = []
        self.tts(res)
        return res

    def tts(self,text):
        text = text.replace(" ", "")
        play_sound = PlaySound("スピーカー")
        data,rate = self.tts_model.get_voice(text)
        play_sound.play_sound(data,rate)           


if __name__=="__main__":
    url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg?download=true"
    image = Image.open(requests.get(url, stream=True).raw)
    prompt = ""
    vlm = vlm()
    vlm.predict(image,prompt)
    prompt = "車のほかには何が写っていますか？"
    vlm.predict(image,prompt)


