from cron import create_folder
from readwise import main as readwise_main
from md import main as md_main

def main():
    path = create_folder()
    readwise_main(write_path=path + '/data.json')
    md_main(read_path=path + '/data.json', write_path=path + '/readwise.txt')

if __name__ == "__main__":
    main()