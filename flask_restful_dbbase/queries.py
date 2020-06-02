# flask_restful_dbbase/queries.py
"""
This module implements some query methods.

query={title: "The Cell"}


query={title: ['like', "The Cell%"]}

query={title: {op: 'like', "The Cell%"}}

query=[
    ["title", "like", "The Cell%"], 
    ["pub_year", "gte", 2008]
]

or {"query": [{"title": ["like", "The Cell%"]}, {"pub_year": ["gte", 2008]}]}

query
"""

ops = {
    'eq_',
    'like_',
    'ilike'
    'gt_', 
    'gte_', 
    'lt_', 
    'lte_', 
    'bt_', 
    'not_', 
    'in_', 
    'not_in_', 
    'or_', 
    'and_', 
    'orderby_'   # {"invoiceNo": "asc"}
}


def parse_query(query, obj_params, model_class):
    """ parse_query
    
    This function parses a query, breaking it down into elements for a 
    selection process.
    
    Args:
        query: (list) : The query in a dictionary format.
        obj_params: (dict) : The document dictionary for a table

    query = [
        ["and_", 
            ["pub_year", "lte_", 2010], 
            ["author_id", "eq_", 2]
        ],
        ["orderby_", ["pub_year", "asc"], "author_id", "desc"]
    
    ]
    ops = ['gt', 'gte', 'lt', 'lte', 'bt', 'not', 'in', 'not_in', 'oe', 'and', 'orderby']
    """

    qry = model_class.query  # starts with assumption of the model 
    for key, query_elements in query:
        
        for op, value in query_elements.items():
            if op not in ops:
                return False, f"Unknown query key {op}"
            qry = eval_triple(model_class, qry, triple)
    
    return qry


def eval_triple(model_class, qry, triple, no_query=False):
    """
    This function creates portion of a query.
    
    In most cases it uses a triple of key, op and value.
    
    However for `or` and `and`, it is different
    """
    
    db = model_class.db
    if triple[0] in ('or_', 'and_'):
        op = triple[0]
        values = triple[1:]
        if op == 'or_':
            qrys = []
            for part in values:
                qrys.append(eval_triple(model_class, qry, part, no_query=True))
            
            qry = qry.filter(db.or_(*qrys))
        elif op == 'and_':
            qrys = []
            for part in values:
                qrys.append(eval_triple(model_class, qry, part, no_query=True))
            
            qry = qry.filter(db.or_(*qrys))        
            return qry

    key, op, value = triple

    if isinstance(value, list):
        if len(value) == 3:
            # is it a triple 
            if value[0] in ops:
                # evaluate it first 
                value = eval_triple(qry, *value)
    
    if op == 'eq_':
        column = getattr(model_class, key)
        binary_exp = column == value
    elif op == 'like_':
        column = getattr(model_class, key)
        binary_exp = column.like(value)
    elif op == 'ilike_':
        column = getattr(model_class, key)
        binary_exp = column.ilike(value)
    elif op == 'gt_':
        column = getattr(model_class, key)
        binary_exp = column > value
    elif op == 'gte_':
        column = getattr(model_class, key)
        binary_exp = column >= value
    elif op == 'lt_':
        column = getattr(model_class, key)
        binary_exp = column < value
    elif op == 'lte_':
        column = getattr(model_class, key)
        binary_exp = column <= value
    elif op == 'between_':
        column = getattr(model_class, key)
        binary_exp = db.between(column, value[0], value[1])
    # come back to this one
    # elif op == 'not_':  # should resolve to None
    #     column = getattr(model_class, key)
    #     qry = qry.filter(column.isnot(B))
    elif op == 'in_':
        column = getattr(model_class, key)
        binary_exp = column.in_(value)
        qry = qry.filter()
    elif op == 'not_in_':
        column = getattr(model_class, key)
        binary_exp = column.notin_(value)
        qry = qry.filter()
    elif op == 'order_by_':
        column = getattr(model_class, key)
        binary_exp = key <= value
    else:
        raise ValueError('Unknown operation{}'.format(op))

    if no_query:
        return binary_exp
    qry = qry.filter(binary_exp)
    return qry

























