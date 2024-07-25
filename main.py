# @title Launch the demo
import gradio as gr
from vlm import vlm
vlm = vlm()
def vlm_predict(image,prompt):
    return vlm.predict(image,prompt)

interface = gr.Interface(
    fn=vlm_predict,
    inputs=[
        gr.Image(type="pil", label="画像をアップロード"),
        gr.Textbox(lines=2, placeholder="プロンプトを入力（省略可）", label="プロンプト")
    ],
    outputs=gr.Textbox(label="生成された説明"),
    title="VLM 日本語キャプション生成",
    description="画像をアップロードして、プロンプトに応じた日本語のキャプションを生成します。"
)

if __name__ == "__main__":
    # demo.launch(share=True, debug=True, show_error=True)
    interface.launch()