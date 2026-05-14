from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import ShoppingItem, ShoppingList, CalendarEvent, Note


def register(request):
    if request.user.is_authenticated:
        return redirect('/mylist/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/mylist/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def mylist(request):
    if request.method == 'POST':
        list_id = request.POST.get('list_id')
        shopping_list = get_object_or_404(ShoppingList, id=list_id, user=request.user)
        ShoppingItem.objects.create(name=request.POST['itemName'], shopping_list=shopping_list)
    all_lists = ShoppingList.objects.prefetch_related('items').filter(user=request.user)
    return render(request, 'shoppinglist.html', {'all_lists': all_lists})


@login_required
def toggle_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(ShoppingItem, id=item_id, shopping_list__user=request.user)
        item.done = not item.done
        item.save()
        return JsonResponse({'success': True, 'done': item.done})
    return JsonResponse({'success': False}, status=405)


@login_required
def delete_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(ShoppingItem, id=item_id, shopping_list__user=request.user)
        item.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=405)


@login_required
def edit_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(ShoppingItem, id=item_id, shopping_list__user=request.user)
        new_name = request.POST.get('newName', '').strip()
        if new_name:
            item.name = new_name
            item.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@login_required
def create_list(request):
    if request.method == 'POST':
        name = request.POST.get('listName', '').strip()
        if name:
            ShoppingList.objects.create(name=name, user=request.user)
            return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@login_required
def events(request):
    if request.method == 'POST':
        date_str = request.POST.get('date', '').strip()
        title = request.POST.get('title', '').strip()
        if date_str and title:
            CalendarEvent.objects.create(date=date_str, title=title, user=request.user)
            return JsonResponse({'success': True})
        return JsonResponse({'success': False}, status=400)
    all_events = list(CalendarEvent.objects.filter(user=request.user).values('id', 'date', 'title'))
    for e in all_events:
        e['date'] = str(e['date'])
    return JsonResponse({'events': all_events})


@login_required
def delete_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(CalendarEvent, id=event_id, user=request.user)
        event.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=405)


@login_required
def notes(request):
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            note = Note.objects.create(text=text, user=request.user)
            return JsonResponse({'success': True, 'id': note.id})
        return JsonResponse({'success': False}, status=400)
    all_notes = list(Note.objects.filter(user=request.user).values('id', 'text'))
    return JsonResponse({'notes': all_notes})


@login_required
def delete_note(request, note_id):
    if request.method == 'POST':
        note = get_object_or_404(Note, id=note_id, user=request.user)
        note.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=405)
