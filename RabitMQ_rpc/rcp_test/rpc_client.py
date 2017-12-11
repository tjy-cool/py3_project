import pika, uuid, time
class FibonacciRpcClient(object):
    "斐波那契数列rpc客户端"
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

    def on_response(self, ch, method, property, body):
        print('=====> ', method, property)
        if self.corr_id == property.correlation_id:
            self.response = body
    
    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.publish(exchange='',
                             routing_key='rpc_queue',
                             properties=pika.BasicProperties(
                                 reply_to = self.callback_queue,
                                 correlation_id=self.corr_id),
                            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
            print("no msg...")
            time.sleep(0.5)
        return int(self.response)

if __name__ == '__main__':
    fibonacci_rpc = FibonacciRpcClient()
    num = input('>> ').strip()
    print(num, type(int(num)))
    print('[x] requesting fib(%s)'%num)
    res = fibonacci_rpc.call(int(num))
    print('[.] got %r' % res)
