import sys, inspect
from homework import dags

def print_classes():
    for name, obj in inspect.getmembers(sys.modules[dags.__name__]):
        if inspect.isclass(obj):
            print(obj)


if __name__ == "__main__":
    print_classes()