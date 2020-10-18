class ClientInfo:
    def __init__(self,request):
        self.request = request

    def __getClientIP(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


    def __getClientBrowser(self):
        return self.request.META['HTTP_USER_AGENT']


    def getData(self):
        return {
            'IpAddr': self.__getClientIP(),
            'browserType': self.__getClientBrowser()
        }
