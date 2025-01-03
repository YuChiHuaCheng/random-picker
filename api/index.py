from RandomPicker import app

# 将 Flask 应用暴露给 Vercel
def handler(request):
    return app(request)
