from transformers import AutoProcessor, PaliGemmaForConditionalGeneration,BitsAndBytesConfig
from PIL import Image
import requests
import torch
import time
from voicevox_adapter import VoicevoxAdapter
from play_sound import PlaySound
class vlm():
    def __init__(self):
        model_id = "./paligemma"
        quantization_config = BitsAndBytesConfig(load_in_4bit=True)
        self.model = PaliGemmaForConditionalGeneration.from_pretrained(
            model_id, quantization_config=quantization_config
        ).eval()
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.tts_model= VoicevoxAdapter()
        self.tts("初期設定完了です。、コマンドラインに表示されているローカルのアドレスにアクセスしてね")
    def predict(self,image,prompt):
        model = self.model
        device = "cuda:0"
        # Instruct the model to create a caption in japanese
        if prompt == "":
            prompt = "この画像について詳しく日本語で説明してください"
        model_inputs = self.processor(text=prompt, images=image, return_tensors="pt").to(model.device)
        input_len = model_inputs["input_ids"].shape[-1]

        with torch.inference_mode():
            generation = model.generate(**model_inputs, max_new_tokens=200, do_sample=False)
            generation = generation[0][input_len:]
            decoded = str(self.processor.decode(generation, skip_special_tokens=True))
            print(decoded)
            self.tts(decoded)
        return decoded

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


