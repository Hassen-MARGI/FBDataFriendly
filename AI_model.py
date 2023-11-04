import base64
import requests
def ai_model(image):
    with open(image, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")
    url = "http://127.0.0.1:7860"
    payload = {
        "image": image_data,
        "mode": "fast"
    }
    response = requests.post(url=f'{url}/interrogator/prompt', json=payload)
    r = response.json()
    items = r['prompt'].split(',')
    text = ', '.join(items[:4])
    return text