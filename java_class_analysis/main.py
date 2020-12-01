from argparse import ArgumentParser
from lib.analysis import analysis


def main():
    argParser = ArgumentParser(description="Java Class Dependency Analyze")
    argParser.add_argument("-c", "--class", help="The class name with full package path such as com.abc.ClassA")
    args = argParser.parse_args()
    analysis(args)

    
if __name__ == "__main__":
    main()
