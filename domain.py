"""Помощник редактора — самостоятельный первый сценарий."""
HELP = '/submit текст — создать заявку\n/mine — мои заявки\n/queue — очередь (админ)\n/status ID | accepted/rejected/done — изменить статус (админ)'

def handle(s, u, cmd, arg, admin):
    from core import require_admin, parts, positive, add, item, listing

    if cmd == '/submit':
        if not arg: raise ValueError('Добавьте текст заявки.')
        key = add(s, title=arg, owner=u, status='new')
        return 'Создано #' + key
    if cmd == '/mine': return listing(s, lambda x: x['owner'] == u)
    if cmd == '/queue':
        require_admin(admin)
        return listing(s)
    if cmd == '/status':
        require_admin(admin)
        key, status = parts(arg, 2)
        row = item(s, key)
        allowed = {'new': ['accepted', 'rejected'], 'accepted': ['done'], 'rejected': [], 'done': []}
        if status not in allowed[row['status']]: raise ValueError('Недопустимый переход статуса.')
        row['status'] = status
        return 'Статус: ' + status
