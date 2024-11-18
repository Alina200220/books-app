from ajax_select import register, LookupChannel
from .models import Books

@register('title')
class TagsLookup(LookupChannel):

    model = Books

    def get_query(self, q, request):
        return self.model.objects.filter(book_title__icontains=q)

    def format_item_display(self, item):
        return u"<span class='title'>%s</span>" % item.name