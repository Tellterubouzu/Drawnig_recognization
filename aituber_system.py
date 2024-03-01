import random
from obs_adapter import OBSAdapter
from voicevox_adapter import VoicevoxAdapter
from openai_adapter import OpenAIAdapter
from Gemini_adapter import GeminiproAdapter
from youtube_comment_adapter import YoutubeCommentAdapter
from play_sound import PlaySound
#add
from ShimoGuardrails import GuardRails_Adapter
from RAGfrom_GSE import RAG_from_GSE_Adapter


from dotenv import load_dotenv
load_dotenv()
import os

class AITuberSystem:
    def __init__(self) ->None:
        #video_id = os.getenv("YOUTUBE_VIDEO_ID")
        video_id= "DR6XRAGFlYc"
        print(video_id)
        self.youtube_comment_adapter = YoutubeCommentAdapter(video_id)
        self.openai_adapter = OpenAIAdapter()
        self.gemini_adapter = GeminiproAdapter()
        self.voice_adapter = VoicevoxAdapter()
        self.obs_adapter = OBSAdapter()
        self.play_sound = PlaySound(output_device_name = "CABLE Input")
        self.guardrail_adapter = GuardRails_Adapter()
        self.RAG_from_GSE_Adapter = RAG_from_GSE_Adapter()
        pass
    def TTSandStreaming(self,text):
            data,rate = self.voice_adapter.get_voice(text)
            self.obs_adapter.set_answer(text)
            self.play_sound.play_sound(data,rate)

    def talk_with_comment(self,Mode) ->bool:
        print("Load comment")
        comment = self.youtube_comment_adapter.get_comment()
        if comment == None:
            print("There is NO comment")
            return False
        self.obs_adapter.set_question(comment)
        print("set_obs_question")
        if Mode == 1:
            print("OPENAI")
            response_text = self.openai_adapter.create_chat(comment)
            self.TTSandStreaming(response_text)
            
            
        elif Mode == 2:
            print("GEMINI")
            response_text = self.gemini_adapter.create_chat(comment)
            self.TTSandStreaming(response_text)
        elif Mode == 3:
            if self.guardrail_adapter.classify_chat(comment)==1:
                    print("UsingRAG")
                    response_text = self.RAG_from_GSE_Adapter.RAGfrom_GSE_GEMINI(comment)
                    self.TTSandStreaming(response_text)
            else:
                print("GEMINI")
                response_text = self.gemini_adapter.create_chat(comment)
                self.TTSandStreaming(response_text)
        elif Mode == 4:
            Guarded_text=[
                      "あー、それはこたえられないわ。",
                      "ごめん、わかんない",
                      "ごめんね、その質問はパスさせてほしい",
                      "うーん、この質問にはノーコメントにしとくね",
                      "ん－、ちょっと難しいかもしれない",
                      "答えたいんだけど、ちょっと無理！"
            ]
            print("inputrails")
            if self.guardrail_adapter.Inputrails(comment)==0:
                print("Classify")
                if self.guardrail_adapter.classify_chat(comment)==1:
                    #self.TTSandStreaming(Use_net_text[random.randint(0,5)])
                    print("RAG")
                    response_text = self.RAG_from_GSE_Adapter.RAGfrom_GSE_GEMINI(comment)
                    if self.guardrail_adapter.Outputrails==1:
                        response_text=Guarded_text[random.randint(0,5)]
                        self.TTSandStreaming(response_text)
                    else:
                        self.TTSandStreaming(response_text)
                else:
                    response_text = self.gemini_adapter.create_chat(comment)
                    self.TTSandStreaming(response_text)
            else:
                response_text=Guarded_text[random.randint(0,5)]
                self.TTSandStreaming(response_text)
        elif Mode ==5:
            print("OnlyRAG")
            response_text = self.RAG_from_GSE_Adapter.RAGfrom_GSE_GEMINI(comment)
            self.TTSandStreaming(response_text)
        return True
    def talk_with_self_user(self,Mode) ->bool:
        if Mode == 0:
            print("Introduce")
            comment = "自己紹介して!"
            self.obs_adapter.set_question(comment)
            print("GEMINI")
            response_text = self.gemini_adapter.create_chat(comment)
            self.TTSandStreaming(response_text)
        elif Mode ==9:
            print("Introduce")
            comment = str(input())
            self.obs_adapter.set_question(comment)
            print("GEMINI")
            response_text = self.gemini_adapter.create_chat(comment)
            self.TTSandStreaming(response_text)

        return True


if __name__ == "__main__":
    """
Mode CONFIG
LLM config
1 == Openai API
2 == Geminipro
3 == Geminipro + RAG 
4 == Geminipro + RAG + Guardrails
Default mode = 2
"""
    adapter = AITuberSystem()


    adapter.talk_with_self_user(0)
