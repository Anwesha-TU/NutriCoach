# Create your views here.
import json
import traceback

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from model.rag_service import run_model
from model.ocr import extract_text_from_image


@csrf_exempt
def analyze_ingredients(request):
    try:
        body = json.loads(request.body)
        query = body.get("query", "").strip()
        image_path = body.get("image_path")

        # OCR path
        if image_path:
            ocr_text = extract_text_from_image(image_path)
            query = ocr_text

        if not query:
            return JsonResponse({"error": "No input provided"}, status=400)

        result = run_model(query)
        return JsonResponse(result)

    except Exception as e:
        print("ERROR:", e)
        return JsonResponse({"error": str(e)}, status=500)
