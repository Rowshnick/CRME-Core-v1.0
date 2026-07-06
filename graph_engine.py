class GraphEngine:
    def __init__(self, index):
        self.index = index

    def find_by_type(self, obj_type):
        return [
            o for o in self.index["objects"]
            if o["type"] == obj_type
        ]

    def find_related(self, object_id):
        return [
            r for r in self.index["relations"]
            if r["from"] == object_id or r["to"] == object_id
        ]

    def trace_chain(self, object_id):
        chain = [object_id]

        current = object_id
        while True:
            next_rel = next(
                (r for r in self.index["relations"] if r["from"] == current),
                None
            )
            if not next_rel:
                break
            chain.append(next_rel["to"])
            current = next_rel["to"]

        return chain


