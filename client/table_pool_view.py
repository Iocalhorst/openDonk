from table_pool_view_renderer import TablePoolViewRenderer

class  TablePoolView():
    def __init__(self,renderer):
        self.renderer=renderer
        self.table_datasets=[]
        self.user_events=[]
    def has_user_events(self):
        if len(self.user_events)>0 :
            return True
        else :
            return False
    def pop_user_event(self):
        user_event=self.user_events.pop(0)
        return user_event
    def clear(self):
        self.table_datasets.clear()
    def slurp(self,pool_view_data):
        verified_table_datasets=self.verify_pool_view_data(pool_view_data)
        for dataset in self.table_datasets :
            if dataset not in verified_table_datasets :
                self.table_datasets.remove(dataset)
        for dataset in verified_table_datasets :
            if dataset not in self.table_datasets :
                self.table_datasets.append(dataset)

    def verify_pool_view_data(self,pool_view_data):
        dataset_indizes=list(pool_view_data.keys())
        assert len(dataset_indizes)>0,"pool_view_data has no keys"
        table_datasets=[]
        for dataset_index in dataset_indizes :
            table_datasets.append(pool_view_data.get(dataset_index))
        assert len(table_datasets)>0,"pool_view_data has values/datasets"

        expected_keys=["table_id","table_name","game_type","num_seats","stakes"]

        for table_dataset in table_datasets :
            #key validation
            for key in list(table_dataset.keys()) :
                e="unexpected key['"+str(key)+"'] in table_dataset"
                assert key in expected_keys,e
            for expected_key in expected_keys :
                e="missing key['"+str(expected_key)+"'] in table_dataset"
                assert table_dataset.get(expected_key) is not None,e
            #value validation
            for expected_key in expected_keys :
                e="missing value for key['"+expected_key+"'], value : "+str(table_dataset.get(expected_key))
                assert table_dataset.get(expected_key) is not None,e
        return table_datasets
    def update_self(self):
        if self.renderer.has_user_events():
            user_event=self.renderer.pop_user_event()
            self.user_events.append(user_event)
    def draw_self(self):
        assert self.table_datasets is not None,"table_datasets are None"
        #if self.pool_view_data is None :
        #    return
        self.renderer.slurp(self.table_datasets)
        self.renderer.draw_table()
