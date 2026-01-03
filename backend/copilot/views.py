# Create your views here.
import json
import traceback

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from model.rag_service import run_model


@csrf_exempt
def analyze_ingredients(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

    try:
        body = json.loads(request.body)
        query = body.get("query", "").strip()
        parent_query = body.get("parent_query", "").strip()
        print("🔍 Received query:", query)
        result = run_model(query=query, parent_query=parent_query)
        print("Model Result: ", result)

        return JsonResponse(result)

    except Exception as e:
        print("ERROR IN analyze_ingredients")
        traceback.print_exc()

        return JsonResponse({"error": str(e)}, status=500)
