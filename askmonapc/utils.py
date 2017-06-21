def bind(widget, event):
    def a(func):
        widget.Bind(event, func)
    return a