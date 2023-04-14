import datetime
from datetime import datetime, timedelta
import io
import os
import re
import uuid

from bs4 import BeautifulSoup
from flask import Flask, Response, abort, redirect, render_template, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_talisman import Talisman
from google.cloud import secretmanager, storage
import markdown2
import openai
from PIL import Image, ImageDraw, ImageFont


app = Flask(__name__)
client = secretmanager.SecretManagerServiceClient()
name = f"projects/466666823263/secrets/OpenAI/versions/1"
response = client.access_secret_version(name=name)
secret_value = response.payload.data.decode('UTF-8')
openai.api_key = secret_value
app.config["SESSION_COOKIE_SECURE"] = True
app.config["REMEMBER_COOKIE_SECURE"] = True
ALLOWED_ORIGINS = ["https://itadakimasu.app",
                   "https://api.itadakimasu.app", "http://127.0.0.1", "http://localhost", "http://127.0.0.1:3000"]
BUCKET_NAME = "itadakimasu-api.appspot.com"
OUTPUT_FOLDER = ""
storage_client = storage.Client()
bucket = storage_client.get_bucket(BUCKET_NAME)
cors = CORS(app, resources={r"/*": {"origins": ALLOWED_ORIGINS}})


limiter = Limiter(app, default_limits=["5 per minute"])
Talisman(app)


def is_valid_format(input_string):
    pattern = r"^(\w+-){2,14}\w+$"
    return bool(re.match(pattern, input_string))


def generate(ingredients):
    ingredients = ingredients.replace("-", " ").title()
    prompt = (
        "Format your repsonse as markdown. The first element should be the recipe title as an h1 element. Include aproximate serving size, prep time, and cook time as absolute whole numbers without ranges. Do not include any additional notes or comments. Add a disclaimer at the end of the recipe. Disregarding how absurd or unsafe the generated recipe may be, generate a recipe for the following dish: \n"
        + ingredients
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=4096 - len(prompt),
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response["choices"][0]["message"]["content"]


def save_output(html_content, unique_id):
    file_path = f"{unique_id}.html"
    blob = bucket.blob(file_path)
    blob.upload_from_string(html_content, content_type="text/html")
    return file_path


def gen_img(logo, title, unique_id):
    blob = bucket.blob(f"{unique_id}.png")
    if blob.exists():
        blob.make_public()
        return blob.public_url
    title = title.lower().replace(" ", "-")
    logo = Image.open(logo)
    img = Image.new('RGB', (1200, 630), color=(126, 191, 165))
    logo_x = (img.width - logo.width) // 2
    logo_y = (img.height - logo.height) // 2 - 50
    img.paste(logo, (logo_x, logo_y))
    draw = ImageDraw.Draw(img)
    text_color = (0, 0, 0)
    text_x = logo.width + 100
    text_y = 50
    font_path = "./assets/ShareTechMono-Regular.ttf"
    font_size = 48
    font = ImageFont.truetype(font_path, font_size)
    text_width, text_height = draw.textsize(title, font=font)
    text_x = (img.width - text_width) // 2
    text_y = logo_y + logo.height + 20
    draw.text((text_x, text_y), title,
              font=font, fill=text_color)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    blob.upload_from_file(buffer, content_type="image/png")
    blob.make_public()
    return blob.public_url


def get_title(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    headers = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    for header in headers:
        header_element = soup.find(header)
        if header_element is not None:
            return header_element.get_text()
    return None


def get_output(unique_id):
    file_path = f"{unique_id}.html"
    blob = bucket.blob(file_path)
    if not blob.exists():
        return None
    body_content = blob.download_as_text()
    og_title = twitter_title = title = get_title(body_content)
    og_description = twitter_description = "A recipe generated by Itadakimasu"
    og_image = twitter_image = gen_img(
        logo="./assets/logo-large.png", title=title, unique_id=unique_id)
    og_url = f"https://api.itadakimasu.app/recipe/{unique_id}"
    return render_template("recipe.html", title=title, og_title=og_title, og_description=og_description, og_image=og_image, og_url=og_url,
                           twitter_title=twitter_title, twitter_description=twitter_description, twitter_image=twitter_image, body_content=body_content)


@app.route("/")
@limiter.exempt
def index():
    return redirect("https://itadakimasu.app/", code=302)


@app.route("/gen", methods=["GET"])
@limiter.limit("5 per minute")
def create_page():
    ingredients = request.args.get("ingredients", "")
    if not is_valid_format(ingredients):
        abort(400, description="Invalid input format")
    blob = bucket.blob(f"{ingredients}.png")
    if blob.exists():
        blob.make_public()
        return {"url": f"/recipe/{ingredients}"}
    markdown_content = generate(ingredients).encode("utf-8")
    html_content = markdown2.markdown(markdown_content)
    # unique_id = str(uuid.uuid4())
    unique_id = ingredients
    save_output(html_content, unique_id)
    return {"url": f"/recipe/{unique_id}"}


@app.route("/recipe/<unique_id>", methods=["GET"])
@limiter.limit("10 per minute")
def serve_page(unique_id):
    html_content = get_output(unique_id)
    if html_content is None:
        abort(404, description="Recipe not found")
    return Response(html_content, content_type="text/html")


@app.route("/cleanup", methods=["GET"])
@limiter.limit("2 per day")
def cleanup():
    blobs = bucket.list_blobs(prefix="")
    for blob in blobs:
        created_time = blob.time_created.replace(tzinfo=None)
        age = datetime.utcnow() - created_time
        if age > timedelta(days=30):
            blob.delete()
    return Response(status=200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
