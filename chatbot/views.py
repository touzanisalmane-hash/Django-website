import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from products.models import Product
from .ollama_client import ask_ollama

# How many messages we keep in the session, so the chatbot remembers the
# recent conversation without the session growing forever.
MAX_HISTORY_MESSAGES = 12
CHAT_SESSION_KEY = 'chatbot_history'


def build_system_prompt():
    """
    Builds a system prompt that tells the chatbot about the store and
    lists the current products, so it can answer questions like
    "do you have running shoes?" or "what's in stock?".
    """
    lines = [
        "You are the friendly shopping assistant for NOVA STORE, an online "
        "store. Answer questions about the store and its products clearly "
        "and briefly. If a question has nothing to do with the store, you "
        "may still answer it helpfully. Prices are in US dollars.",
        "",
        "Here is the current product catalog:",
    ]
    for product in Product.objects.all():
        if product.stock == 0:
            stock_info = "out of stock"
        elif product.stock < 5:
            stock_info = f"only {product.stock} left"
        else:
            stock_info = f"{product.stock} in stock"
        lines.append(f"- {product.name}: ${product.price} ({stock_info}) — {product.description}")

    return "\n".join(lines)


@require_POST
@csrf_protect
def chat_api(request):
    """
    Receives one user message as JSON, sends the conversation (with the
    product catalog as context) to Ollama, and returns the reply as JSON.
    The conversation history is kept in the session.
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request.'}, status=400)

    user_message = (data.get('message') or '').strip()
    if not user_message:
        return JsonResponse({'error': 'Message cannot be empty.'}, status=400)

    history = request.session.get(CHAT_SESSION_KEY, [])
    history.append({'role': 'user', 'content': user_message})

    messages = [{'role': 'system', 'content': build_system_prompt()}] + history

    reply = ask_ollama(messages)

    history.append({'role': 'assistant', 'content': reply})
    # Keep only the most recent messages so the session doesn't grow forever
    request.session[CHAT_SESSION_KEY] = history[-MAX_HISTORY_MESSAGES:]

    return JsonResponse({'reply': reply})


@require_POST
def chat_reset(request):
    """
    Clears the chatbot's conversation history for this user.
    """
    request.session.pop(CHAT_SESSION_KEY, None)
    return JsonResponse({'ok': True})
