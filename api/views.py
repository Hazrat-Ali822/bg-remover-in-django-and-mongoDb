import os
import uuid
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from pymongo import MongoClient
from dotenv import load_dotenv
from rembg import remove
from PIL import Image

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGODB_URI")

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client["image_api_db"]
collection = db["user_names"]

# Upload directory
UPLOAD_DIR = "media"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_image(request):
    """Upload an image, remove background, save to MongoDB & return URL."""
    print("=== DEBUG START ===")
    print("DATA:", request.data)
    print("FILES:", request.FILES)
    print("=== DEBUG END ===")

    name = request.data.get("name")
    image_file = request.FILES.get("image") or request.FILES.get("file")  # Accept 'image' or 'file'

    if not name or not image_file:
        return JsonResponse({"error": "Both name and image are required"}, status=400)

    # Remove background from image
    input_image = Image.open(image_file)
    output_image = remove(input_image)

    # Save processed image
    filename = f"{uuid.uuid4()}.png"
    output_path = os.path.join(UPLOAD_DIR, filename)
    output_image.save(output_path, format="PNG")

    # Create public URL
    image_url = f"http://127.0.0.1:8000/media/{filename}"

    # Save to MongoDB
    collection.insert_one({"name": name, "image_url": image_url})

    return JsonResponse({"name": name, "image_url": image_url})


@api_view(['GET'])
def get_all_images(request):
    """Get all saved names & images from MongoDB."""
    documents = list(collection.find({}, {"_id": 0}))  # exclude _id field
    return JsonResponse({"data": documents}, safe=False)
