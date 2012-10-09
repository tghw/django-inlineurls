# Django Inline Urls

`django-inlineurls` defines a decorator, `view()`, which define what URL a view will be accessible by. It also has options for what template to render, whether the view requires login, and any other url kwargs.

If a template is specified, you can simply return a context for it to be rendered with.

## Use

    from inlineurl.decorators import view

    @view('/search/(?P<query>[^/]+/') # A view with no template
    def search(request, query):
        return render(request, 'search.html', {'query': query})

    @view('/home/', 'home.html') # A view with a template defined. Note only the context is returned
    def home(request):
        return {'date': now()}

    @view('/dashboard/', 'dashboard.html', True) # A login_required view
    def home(request):
        return {'user': request.user}

