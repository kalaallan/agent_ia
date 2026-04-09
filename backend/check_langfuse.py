import langfuse

print("Version:", langfuse.__version__)
print("File:", langfuse.__file__)
print("Available:", [n for n in dir(langfuse) if not n.startswith("_")])

try:
    from langfuse.decorators import observe

    print("decorators module exists")
except ImportError as e:
    print("decorators import error:", e)
