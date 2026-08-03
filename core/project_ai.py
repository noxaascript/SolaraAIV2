def generate_code(request):
    request = request.lower()

    # simple templates (bisa diganti AI nanti)
    if "login" in request:
        return """# Login System (simple)
username = input('Username: ')
password = input('Password: ')

if username == 'admin' and password == '1234':
    print('Login success')
else:
    print('Login failed')
"""

    if "calculator" in request:
        return """# Calculator
a = int(input('A: '))
b = int(input('B: '))

print('Hasil:', a + b)
"""

    # fallback
    return f"# AI generated code for: {request}\nprint('hello world')"
