from django.shortcuts import render

# Create your views here.
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from model.rag_service import run_model


@csrf_exempt
@require_POST
def analyze_ingredients(request):
    """
    API endpoint for ingredient analysis
    """
    try:
        body = json.loads(request.body.decode("utf-8"))
        user_query = body.get("query", "").strip()

        if not user_query:
            return JsonResponse(
                {"error": "Query is required"},
                status=400
            )

        result = run_model(user_query)

        return JsonResponse({
            "summary": result["summary"],
            "details": result["details"],
            "uncertainty": result["uncertainty"]
        })

    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=500
        )
