from django.contrib import admin
from django.urls import path, include

from django.shortcuts import render

def index(request):
    #return render(request, 'index.html')
    return render(request, 'three.js-dev\examples\webgpu_water.html')

from django.http import JsonResponse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def send_message_view(request):
    if request.method == 'POST':
        # WebSocket üzerinden gönderilecek mesaj
        message = {'scene': 'new_scene_name'}  # Göndermek istediğiniz mesaj
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'scene_change_group',  # Bu grup adı consumer'da tanımlı olmalı
            {
                'type': 'send_scene_change',  # Consumer'daki mesaj işleyici metodu
                'message': message,
            }
        )
        return JsonResponse({'status': 'Message sent'})
    return JsonResponse({'status': 'Invalid request'}, status=400)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mytest.urls')),
    path('', index, name='index'),
    path('send-message/', send_message_view, name='send-message'),

    path('api/', include('shop.urls')),  # 'shop' uygulamasının URL'lerini dahil ediyorsunuz
]
