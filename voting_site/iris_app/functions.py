def handle_uploaded_files(f):
    with open('iris_app/media/media/votes'+f.name, 'wb+')as destination:
        for chunk in f.chunks():
            destination.write(chunk)
