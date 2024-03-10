from table_thread import TableThread
class TablePool():
    tables=[]

    def quick_seat(player):
        for table in TablePool.tables :
            if table.quick_seat(player) :
                #print("DEBUG : [TablePool.quick_seat] success")
                return True
        #print("DEBUG : [TablePool.quick_seat] fail")
        #print("DEBUG : [TablePool.quick_seat] ",TablePool.tables)
        assert False,"did not find a table for player"
    def register_table(table):
        TablePool.tables.append(table)

    def get_view():
        table_pool_view={}
        for index,table in enumerate(TablePool.tables):
            table_pool_view.setdefault(index)
            table_view=table.get_view()
            meta=table_view.get("table_view_meta")
            table_pool_view[index]=meta
        return table_pool_view
    def get_table_by_id(table_id):
        for table in TablePool.tables :
            if table.table_id==table_id:
                return table
        raise
    def unscubscribe_from_all_observers(client_id):
        for table in TablePool.tables :
            if table.observer.has_subscription_from_client_id(client_id)==True:
                table.observer.unregister_subscription(client_id)

class TableThreadPool():
    table_thread_workers={}
    proxy=None
    def register_table(table):
        table_thread=TableThread(table)
        table_id=table.table_id
        TableThreadPool.table_thread_workers.setdefault(table_id)
        TableThreadPool.table_thread_workers[table_id]=table_thread

    def start_all_tables():
        table_ids=list(TableThreadPool.table_thread_workers.keys())
        #print(TableThreadPool.table_thread_workers)
        for table_id in table_ids :
            table_thread=TableThreadPool.table_thread_workers.get(table_id)
            table_thread.set_proxy(TableThreadPool.proxy)
            table_thread.start()
