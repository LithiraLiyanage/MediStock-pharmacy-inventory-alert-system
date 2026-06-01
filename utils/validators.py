from utils.helpers import days_until
CATEGORIES=['Antibiotic','Pain Relief','Vitamins','Allergy','Diabetes','Blood Pressure','Cold & Flu','Digestive Health','First Aid','Other']
def validate_medicine(data, duplicate_exists=False):
    errors=[]; warnings=[]; name=data.get('medicine_name','').strip(); batch=data.get('batch_number','').strip(); supplier=data.get('supplier_name','').strip(); storage=data.get('storage_location','').strip(); notes=data.get('notes','').strip()
    if not name: errors.append('Medicine name is required.')
    elif len(name)<2: errors.append('Medicine name must be at least 2 characters.')
    elif len(name)>100: errors.append('Medicine name must be less than 100 characters.')
    if not data.get('category'): errors.append('Category is required.')
    if not batch: errors.append('Batch number is required.')
    elif len(batch)<2: errors.append('Batch number must be at least 2 characters.')
    try:
        if int(data.get('quantity',0))<0: errors.append('Quantity cannot be negative.')
    except Exception: errors.append('Quantity must be a valid integer.')
    try:
        if float(data.get('unit_price',0))<0: errors.append('Unit price cannot be negative.')
    except Exception: errors.append('Unit price must be a valid number.')
    try:
        if int(data.get('reorder_level',0))<0: errors.append('Reorder level cannot be negative.')
    except Exception: errors.append('Reorder level must be a valid integer.')
    if duplicate_exists: errors.append('Duplicate batch detected: same medicine name and batch number already exists.')
    if supplier and len(supplier)>100: errors.append('Supplier name must be less than 100 characters.')
    if storage and len(storage)>100: errors.append('Storage location must be less than 100 characters.')
    if notes and len(notes)>300: errors.append('Notes must be less than 300 characters.')
    exp=data.get('expiry_date')
    if not exp: errors.append('Expiry date is required.')
    else:
        remaining=days_until(exp)
        if remaining is not None:
            if remaining<0: warnings.append('This medicine is already expired.')
            elif remaining<=30: warnings.append('This medicine is near expiry.')
    return errors,warnings
def validate_stock_update(selected_id,movement_type,amount,available,note=''):
    errors=[]
    if not selected_id: errors.append('Medicine must be selected.')
    try:
        amount=int(amount)
        if amount<=0 and movement_type!='Set Exact Stock': errors.append('Quantity change must be greater than 0.')
        if amount<0 and movement_type=='Set Exact Stock': errors.append('Adjustment quantity cannot be negative.')
    except Exception: return ['Quantity change must be a valid integer.']
    if movement_type=='Stock Out' and amount>int(available): errors.append('Cannot reduce stock below zero.')
    if len(str(note))>200: errors.append('Movement note must be less than 200 characters.')
    return errors
