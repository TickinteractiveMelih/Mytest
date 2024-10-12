from django.shortcuts import render

from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


# Create your views here.
def index(request):
    return render(request, 'three.js-dev\examples\index.html')
    #return render(request, 'index copy.html')


def send_message_to_all(request):
    message1 = request.GET.get('message')  # Web sayfasından mesajı al
    message = {
        'mes': message1,
        'note': 'mtb',
    }
    channel_layer = get_channel_layer()

    # "unity_clients" grubuna mesaj gönder
    async_to_sync(channel_layer.group_send)(
        "unity_clients",  # Tüm client'ların yer aldığı grup ismi
        {
            'type': 'chat_message',
            'message': message,
        }
    )

    return JsonResponse({"status": "Message sent to all Unity clients"})