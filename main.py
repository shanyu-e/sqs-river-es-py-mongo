import boto3

__author__ = 'dengjing'


def test_sqs():
    # sqs_client = boto3.client('sqs')
    # print(sqs_client.list_queues())
    sqs_resource = boto3.resource('sqs')
    queue = sqs_resource.get_queue_by_name(QueueName='river')
    # print(queue.attributes.get('DelaySeconds'))
    # print(sqs_resource.get_available_subresources())
    response = queue.send_message(MessageBody='hello world!')
    print response


def test_sqs_receive_messages():
    sqs_resource = boto3.resource('sqs')
    queue = sqs_resource.get_queue_by_name(QueueName='river')
    message = queue.receive_messages(MaxNumberOfMessages=10)
    print len(message)
    print message[0].body
    print queue


def base_test():
    # client = boto3.client('sqs')
    # print(client.list_queues())
    sqs = boto3.resource('sqs')
    queue = sqs.Queue(url='https://us-west-2.queue.amazonaws.com/052792705405/river')
    print queue.receive_messages()[0].body
    print dir(queue)


if __name__ == '__main__':
    # test_sqs()
    # test_sqs_receive_messages()
    base_test()