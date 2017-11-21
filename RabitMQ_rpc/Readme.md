# 基于RabbitMQ rpc实现的主机管理
    可以对指定机器异步的执行多个命令
    例子：
    >>:run "df -h" --hosts 192.168.3.55 10.4.3.4 
    task id: 45334
    >>: check_task 45334 
    >>:
    注意，每执行一条命令，即立刻生成一个任务ID,不需等待结果返回，通过命令check_task TASK_ID来得到任务结果 