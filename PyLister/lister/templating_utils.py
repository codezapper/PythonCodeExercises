from django.template import loader


def render_wrapper(request):
    template = loader.get_template('lister/wrapper.html')
    context = {}

    return template.render(context, request)


def render_for_songs_list(request, album='', artist='', year=''):
    template = loader.get_template('lister/songs.html')
    context = {}
    return template.render(context, request)
