#python file to control categories at top of screen
from .models import Category
def menu_links(request):
    links=Category.objects.all()
    return dict(links=links)
# you have to add this to settings file under templates