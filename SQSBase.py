# coding=utf-8
import boto3

__author__ = 'dengjing'

sqs_r = boto3.resource('sqs')
queue = sqs_r.Queue(url='https://us-west-2.queue.amazonaws.com/052792705405/river')


def is_empty():
    m = queue.receive_messages()
    return len(m) == 0


def get_message():
    return queue.receive_messages()


if __name__ == '__main__':
    # get_message()
    # print(is_empty())
    print queue