```python
from compiler import Compiler

def main():
    # Example program
    source = """
    program exemplo1;
    var fat, num, cont: integer;
    begin
        read(num);
        fat := 1;
        cont := 2;
        while cont <= num do
        begin
            fat := fat * num;
            cont := cont + 1
        end;
        write(fat)
    end.
    """
    
    try:
        compiler = Compiler(source)
        compiler.compile()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```