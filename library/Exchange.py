import heapq
from types import Order as OrderType
import datetime


class Exchange:

    order_counter = 0


    @classmethod
    def get_counter(cls):
        number_assigned = cls.order_counter
        cls.order_counter += 1
        return number_assigned
    

    @staticmethod
    def get_buy_and_sell_orders(order: OrderType, buy_heap: list[OrderType], sell_heap: list[OrderType]) -> tuple[OrderType|None, OrderType|None]:
        
        sell_order: OrderType|None = None if order[6] else order
        buy_order: OrderType|None = order if order[6] else None

        if not sell_order:
            sell_order = sell_heap[0] if sell_heap else None

        if not buy_order:
            buy_order = buy_heap[0] if buy_heap else None

        return buy_order, sell_order


    @staticmethod
    def assign_order_id(order: OrderType):
        if order[0]: return order
        return (
            Exchange.get_counter(),
            order[1],
            order[2],
            order[3],
            order[4],
            order[5],
            order[6],
        )
    

    @staticmethod
    def can_exchange(buy_order: OrderType|None, sell_order: OrderType|None) -> bool:
        return bool(buy_order and sell_order and buy_order[0] and sell_order[0] and sell_order[0] <= buy_order[0])


    @staticmethod
    def get_trade_price(buy_order: OrderType, sell_order: OrderType) -> float:
        return (abs(buy_order[0] - sell_order[0]) / 2) + min(buy_order[0], sell_order[0])


    @staticmethod
    def adjust_order_quantity(quantity: int, order: OrderType) -> OrderType:
        return (
            max(order[0] - quantity, 0),
            order[1],
            order[2],
            order[3],
            order[4],
            order[5],
            order[6],
        )
    

    @staticmethod
    def exchange(order: OrderType, buy_heap: list[OrderType], sell_heap: list[OrderType]):

        buy_order, sell_order = Exchange.get_buy_and_sell_orders(order, buy_heap, sell_heap)
        if buy_order: buy_order = Exchange.assign_order_id(buy_order)
        if sell_order: sell_order = Exchange.assign_order_id(sell_order)

        current_order: OrderType = buy_order if order[6] else sell_order

        can_exchange = Exchange.can_exchange(buy_order, sell_order)
        trades = []
        while can_exchange:

            quantity_to_adjust: int = min(buy_order[4], sell_order[4])
            adjusted_buy_order = Exchange.adjust_order_quantity(quantity_to_adjust, buy_order)
            adjusted_sell_order = Exchange.adjust_order_quantity(quantity_to_adjust, sell_order)

            # buy order
            if current_order[5]:
                sell_heap[2] = adjusted_sell_order
                if not buy_order[0]: _ = heapq.heappop(buy_heap)
                current_order = adjusted_buy_order

            # sell order
            else:
                buy_heap[2] = adjusted_buy_order
                if not buy_order[0]: _ = heapq.heappop(sell_heap)
                current_order = adjusted_sell_order


            # register trades (id will see later)
            trade_price: float = Exchange.get_trade_price(buy_order, sell_order)
            trades.append((1, buy_order[2], sell_order[2], quantity_to_adjust, trade_price, datetime.datetime.now()))


            # check if current order is exhausted
            if current_order[0]: break

            # get new orders
            next_buy_order, next_sell_order = Exchange.get_buy_and_sell_orders(current_order, buy_heap, sell_heap)
            can_exchange = Exchange.can_exchange(next_buy_order, next_sell_order)


        # current order not satisfied
        if current_order[0] and current_order[5]:
            heapq.heappush(buy_heap, current_order)
        
        if current_order[0] and not current_order[5]:
            heapq.heappush(sell_heap, current_order)
        

            
