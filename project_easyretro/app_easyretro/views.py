from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

# Armazenamento em memória para os formulários (exemplo)
form_storage = {}
next_id = 1

def api_test(request):
    return JsonResponse({"message": "Olá do Django!"})

@csrf_exempt
def create_formulario(request):
    global next_id
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)

        form_id = next_id
        next_id += 1
        form_storage[form_id] = data
        return JsonResponse({'id': form_id, 'data': data}, status=201)
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def get_formulario(request, id):
    if request.method == 'GET':
        try:
            form_id = int(id)
        except ValueError:
            return JsonResponse({'error': 'ID inválido'}, status=400)

        form_data = form_storage.get(form_id)
        if form_data is None:
            return JsonResponse({'error': 'Formulário não encontrado'}, status=404)
        return JsonResponse({'id': form_id, 'data': form_data})
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)