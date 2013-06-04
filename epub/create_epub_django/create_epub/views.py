from django.views.generic import CreateView, DetailView, ListView
from django.shortcuts import render
from django.http import HttpResponseRedirect
import os
import logging

from models import Epub
from forms import EpubCreateForm
from epub_creator import EpubCreator

def create(request):
    if request.method == 'POST':
        form = EpubCreateForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            # Save in database
            new_epub = form.save(commit=False)
            
            logging.debug('Saving EPUB: author = ' + new_epub.author + ', title = ' + new_epub.title + ', text = ' + new_epub.text)            
            new_epub.save() # not necessary if commit = True

            # Create epub in file system
            epub_creator = EpubCreator()
            epub_creator.create_epub(title = new_epub.title, text = new_epub.text, creator = new_epub.author)
            
            # Redirect after POST
            return HttpResponseRedirect('/epubs/') 
    else:
        form = EpubCreateForm() # An unbound form

    return render(request, 'create.html', {
        'form': form,
    })

'''  
class EpubCreateView(CreateView):
    model = Epub
    template_name = 'create.html'
    form_class = EpubCreateForm
    context_object_name = 'new_epub'
    
    def create(request):
        logging.debug("TIIIIIIIIIIIIIIIIIITLE")
        if request.method == 'POST':
            form = EpubCreateForm(request.POST) # A form bound to the POST data
            if form.is_valid():
                # Create epub in file system
                logging.debug("TIIIIIIIIIIIIIIIIIITLE" + new_epub.title)
                EpubCreator.create_epub(title = new_epub.title, text = new_epub.text, creator = epub.author)

                # Save in database
                new_epub = form.save(commit=False)
                new_epub.save() # not necessary if commit = True
                
                # Redirect after POST
                return HttpResponseRedirect('/epubs/') 
        else:
            form = EpubCreateForm() # An unbound form

        return render(request, 'create33.html', {
            'form': form,
        })
'''

class EpubListView(ListView):
    model = Epub
    template_name = 'list.html'
    context_object_name = 'epub_list'
    #queryset = models.Epub.objects.filter(is_published = True)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EpubListView, self).get_context_data(**kwargs)
        
        logging.debug('EpubListView.get_context_data(): ' + os.path.dirname(os.path.abspath(__file__)))
        context['epub_count'] = self.model.objects.all().count()
        context['request'] = self.request
        
        return context
    
    
class EpubDetailsView(DetailView):
    model = Epub
    template_name = 'detail.html'
    context_object_name = 'epub_details'
