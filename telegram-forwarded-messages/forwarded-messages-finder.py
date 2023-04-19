import colorama
import json
import argparse

# init the colorama module
colorama.init()

GREEN = colorama.Fore.GREEN
YELLOW = colorama.Fore.YELLOW
GRAY = colorama.Fore.CYAN
RESET = colorama.Fore.RESET
RED = colorama.Fore.RED

USER_NAME = 'user_name'


def get_arg():
    """
    Getting command line arguments
    :return: Dict of args
    """
    parser = argparse.ArgumentParser(description='Finds forwarded messages in Telegram chat history')
    parser.add_argument('-f', '--file', help='Path to file containing Telegram chat history (.json)')
    args = vars(parser.parse_args())
    return args


def parse(file_descr):
    chat = json.load(file_descr)
    chat_name = chat['name']
    # chat_name = 'chat_name'
    messages = chat['messages']
    for item in messages:
        if 'forwarded_from' in item and item['forwarded_from'] != USER_NAME and item['forwarded_from'] != chat_name:
            # print(item)
            print(f"[{item['date']}] {item['from']} - {item['forwarded_from']}")


def main(args):
    try:
        # region input args parsing
        # trying to get 'file' attribute and open this file
        filename = args['file']
        file_descr = None
        if filename is not None:
            file_descr = open(f'{filename}', 'r', encoding='utf-8')
        # endregion
        parse(file_descr)

    except Exception as e:
        print(f'{RED}[!] [main] Error: {str(e)}{RESET}')


if __name__ == '__main__':
    args = get_arg()
    main(args)
