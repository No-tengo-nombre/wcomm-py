from wcomm.message import Message


def main():
    test_msg = Message.from_file("wcomm/examples/resources/img/img_house.jpeg")
    # test_msg = Message.from_file("wcomm/examples/resources/binaries/data_test")
    # print(test_msg.as_string())
    # print(test_msg)
