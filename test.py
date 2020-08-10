import os

d = '.'
print([folder for folder in [os.path.join(d, o)[2:] for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))] if folder not in ['.git', 'venv', '__pycache__']])