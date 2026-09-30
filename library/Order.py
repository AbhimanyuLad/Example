

class Order:

    def __init__(self, order_id, user_id, resource, order_type, quantity, price, side):
        self.order_id = order_id,
        self.user_id = user_id,
        self.resource = resource,
        self.order_type = order_type,
        self.quantity = quantity,
        self.price = price
        self.side = side

        self.remaining_quantity = quantity
        self.status = "PENDING"


    def create_order(self, order_id, user_id, resource, side, quantity, price, timestamp):
        return Order(order_id, user_id, resource, side, quantity, price, timestamp)
    

    def validate_order(self, order):
        if(order.quantity <= 0 and order.price <= 0):
            return False

        if(order.side not in ["BUY", "SELL"]):
            return False

        if(not order.resource):
            return False

        return True
                    






    