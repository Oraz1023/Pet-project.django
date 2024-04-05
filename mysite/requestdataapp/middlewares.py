from django.http import HttpRequest


def setup_useragent_on_request_middleware(get_response):
    print('initial call')

    def middleware(request: HttpRequest):
        print('before get response: ', request)
        # request.user_agent = request.META['HTTP_USER_AGENT']
        # Access 'HTTP_USER_AGENT' safely using get() method
        user_agent = request.META.get('HTTP_USER_AGENT')

        # Set 'user_agent' to a default value if it's not present
        if user_agent is None:
            user_agent = 'Unknown'

        # Assign the value to request.user_agent
        request.user_agent = user_agent
        response = get_response(request)
        print('after get response')
        return response

    return middleware


class CountRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0
        self.response_count = 0
        self.exception_count = 0

    def __call__(self, request:HttpRequest):
        self.request_count += 1
        print('request count', self.request_count)
        response = self.get_response(request)
        self.response_count += 1
        print('response count',self.response_count)
        return response

    def process_exception(self, request:HttpRequest, exception:Exception):
        self.exception_count += 1
        print('got',self.exception_count, 'exceptions so far')

