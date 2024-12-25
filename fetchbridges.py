import requests
import ollama

def fetch_bridge_captcha(save_raw_captcha=False):
    request_session = requests.Session()
    bridge_captcha_request = request_session.get("https://bridges.torproject.org/moat/fetch").json()
    img_b64 = bridge_captcha_request["data"][0]["image"]
    if save_raw_captcha:
        import io, base64
        from PIL import Image
        img_bytes = base64.b64decode(img_b64)
        img = Image.open(io.BytesIO(img_bytes))
        img.save("bridge_captcha.png")
    return {
        "img_b64": img_b64,
        "captcha_id": bridge_captcha_request["data"][0]["id"],
        "request_session": request_session
    }

def solve_bridge_captcha(img_b64):
    get_captcha_text = ollama.chat(
            model='llama3.2-vision',
            messages=[{
                'role': 'user',
                'content': 'I am trying to read this text from this image. Please write the letters in the image. Only output the letters, no other text.',
                'images': [img_b64]
            }]
        )
    return {
        "text": get_captcha_text.message.content.replace('-', '')
    }


def submit_bridge_captcha(captcha_id, captcha_text, request_session):
    headers = {
        'Content-Type': 'application/vnd.api+json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    
    submit_bridge_captcha_request = request_session.post(
        "https://bridges.torproject.org/moat/check",
        headers=headers,
        json={
            "data": [
                {
                    "challenge": "obfs4",
                    "id": captcha_id,
                    "qrcode": "false",
                    "solution": captcha_text,
                    "transport": "obfs4",
                    "type": "moat-solution",
                    "version": "0.1.0"
                }
            ]
        }
    ).json()
    return submit_bridge_captcha_request["data"][0]["bridges"]


def solve_bridges():
    img_resp = fetch_bridge_captcha(save_raw_captcha=True)
    text_resp = solve_bridge_captcha(img_resp["img_b64"])["text"]
    res = submit_bridge_captcha(img_resp["captcha_id"], text_resp, img_resp["request_session"])
    return res

if __name__ == "__main__":
    print(solve_bridges())
