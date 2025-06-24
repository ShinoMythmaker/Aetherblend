def row_label_operator(layout, label, icon, operator, op_text, op_icon="NONE", **op_kwargs):
    row = layout.row()
    row.label(text=label, icon=icon)
    op = row.operator(operator, text=op_text, icon=op_icon)
    for k, v in op_kwargs.items():
        setattr(op, k, v)
    return row

def row_label(layout, label, icon="NONE"):
    row = layout.row()
    row.label(text=label, icon=icon)
    return row

def row_operator(layout, operator, op_text, op_icon="NONE", **op_kwargs):
    row = layout.row()
    op = row.operator(operator, text=op_text, icon=op_icon)
    for k, v in op_kwargs.items():
        setattr(op, k, v)
    return row