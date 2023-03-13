'''
Code came from ChatGPT. Requested help in spoofing `request.META['REMOTE_ADDR']`
Created a custom middleware class to feed spoofed IP addresses in for local testing
'''

class CustomRemoteAddrMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.custom_ip = '91.193.232.3'  # replace with your custom IP address

    def __call__(self, request):
        request.META['REMOTE_ADDR'] = self.custom_ip
        return self.get_response(request)

# ATL 91.193.232.3
# east moline  173.25.86.53