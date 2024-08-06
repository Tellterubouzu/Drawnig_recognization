import gradio as gr
import csv
import time
from vlm import vlm

# モデルの初期化
vlm = vlm()

def vlm_predict(image, prompt):
    response = vlm.predict(image, prompt)
    return response

def save_feedback(image, prompt, response, feedback, expected):
    timestamp = int(time.time())
    image_path = f"Pastdata/images/{timestamp}.jpg"
    image.save(image_path)  # PIL形式の画像を保存

    csv_file = 'Pastdata/responses.csv'
    header = ['image', 'input', 'output', 'feedback', 'expected']
    row = [image_path, prompt, response, feedback, expected]

    # ファイルが存在しない場合、ヘッダーを書き込む
    with open(csv_file, 'a', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(header)
        writer.writerow(row)

    return "フィードバックが保存されました"

# レイアウトの調整
with gr.Blocks() as demo:
    gr.Markdown("# VLM 日本語キャプション生成\n画像をアップロードして、プロンプトに応じた日本語のキャプションを生成します。")

    with gr.Row():
        with gr.Column(scale=5):
            image_input = gr.Image(type="pil", label="画像をアップロード")
        with gr.Column(scale=3, min_width=300):
            prompt_input = gr.Textbox(lines=2, placeholder="プロンプトを入力（省略可）", label="プロンプト")
            submit_btn = gr.Button("Submit")
            clear_btn = gr.Button("Clear")
            output_text = gr.Textbox(lines=2, label="生成された説明")
            feedback_input = gr.Radio(["good", "bad"], label="フィードバック", visible=False)
            expected_input = gr.Textbox(lines=2, placeholder="期待した回答を入力してください", label="期待した回答", visible=False)
            save_feedback_btn = gr.Button("フィードバックを保存", visible=False)

    gr.Row(submit_btn, clear_btn)

    def on_submit(image, prompt):
        response = vlm_predict(image, prompt)
        return response, gr.update(visible=True), gr.update(visible=True, value=None), gr.update(visible=False)

    def on_feedback(feedback):
        if feedback == "bad":
            return gr.update(visible=True), gr.update(visible=True)
        else:
            return gr.update(visible=False), gr.update(visible=False)

    def on_clear():
        return [None, "", "", gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)]

    def on_save_feedback(image, prompt, response, feedback, expected):
        return save_feedback(image, prompt, response, feedback, expected)

    submit_btn.click(on_submit, inputs=[image_input, prompt_input], outputs=[output_text, feedback_input, expected_input, save_feedback_btn])
    feedback_input.change(on_feedback, inputs=[feedback_input], outputs=[expected_input, save_feedback_btn])
    clear_btn.click(on_clear, inputs=None, outputs=[image_input, prompt_input, output_text, feedback_input, expected_input, save_feedback_btn])
    save_feedback_btn.click(on_save_feedback, inputs=[image_input, prompt_input, output_text, feedback_input, expected_input], outputs=[])

if __name__ == "__main__":
    demo.launch()