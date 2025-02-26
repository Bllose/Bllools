class Observable:
    """
    通过观察模型，同步多个模块下的环境变量
    每个需要观察的类都需要实现_update_env方法
    通过register_observer注册观察者，unregister_observer注销观察者
    然后通过调用notify_observers方法通知所有观察者
    """

    def __init__(self):
        self.observers = []

    def register_observer(self, observer):
        """注册观察者"""
        if observer not in self.observers:
            self.observers.append(observer)

    def unregister_observer(self, observer):
        """注销观察者"""
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self, new_env):
        """通知所有观察者"""
        for observer in self.observers:
            observer._update_env(new_env)