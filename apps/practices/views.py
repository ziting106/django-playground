from django.http import HttpResponse


def hello_world(request):
    return HttpResponse("""
    <html>
    <body>
    <h1>Hello, World!</h1>
    <p>This is a test of the Django framework.</p>
    </body>
    </html>
    """)
