from functions.run_python_file import run_python_file
def main():
    print(run_python_file("calculator", "main.py"))
    print(run_python_file("calculator", "tests.py"))
    print(run_python_file("calculator", "../main.py")) # (this should return an error)
    print(run_python_file("calculator", "nonexistent.py")) # (this should return an error)
if __name__ == "__main__":
    main()
