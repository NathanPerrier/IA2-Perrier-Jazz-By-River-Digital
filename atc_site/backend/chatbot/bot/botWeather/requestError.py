
def handle_errors(default_message):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                return default_message
        return wrapper
    return decorator