from wcomm.message import Message


def main():
    test1 = Message("010011")
    test2 = Message.from_binary("010011")

    print(test1)
    print(test2)
