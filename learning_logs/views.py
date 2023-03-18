from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    '''Homepage Learning Log app'''
    return render(request, 'learning_logs/index.html')

def topics(request):
    '''Displays a list of topics'''
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    '''Displays one topic and all its entries'''
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

def new_topic(request):
    '''Defines a new topic'''
    if request.method != 'POST':
        # No data was sent; creating empty form
        form = TopicForm()
    else:
        # POST data sent; processing data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')
    
    # Output an empty or invalid form
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

def new_entry(request, topic_id):
    '''Adds a new entry on a specific topic'''
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # No data was sent; creating empty form
        form = EntryForm()
    else:
        # POST data sent; processing data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
        
    # Output an empty or invalid form
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

def edit_entry(request, entry_id):
    '''Edits existing entry'''
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        # The original request; the form is filled with the data of the current record
        form = EntryForm(instance=entry)
    else:
        # POST data sent; processing data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    
    # Output an empty or invalid form
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
