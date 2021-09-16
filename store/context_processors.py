from store.models import Categories

def extras(request):
    categories = Categories.objects.all()

    return {'categories': categories}