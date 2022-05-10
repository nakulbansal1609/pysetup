def rule_procc(rule):
    import re
    ####
    if rule.startswith('String'):
        result = re.search(r'\(([^()]*)\)$', rule).group(1).split(',')[1].strip().replace("'", '')
        rule = 'string'
        return (rule,result)
    elif rule.startswith('Numeric'):
        result = re.search(r'\(([^()]*)\)$', rule).group(1).split(',')[1].strip().replace("'", '')
        rule='numeric'
        return (rule,result)
    elif rule.startswith('ID'):
        result = re.search(r'\(([^()]*)\)$', rule).group(1).split(',')[1].strip().replace("'", '')
        rule='ID'
        return (rule,result)
    elif rule.startswith('Datetime'):
        result = re.search(r'\(([^()]*)\)$', rule).group(1).split(',')[1].strip().replace("'", '')
        rule='datetime'
        return (rule,result)
    elif rule.startswith('DateOb'):
        result = re.search(r'\(([^()]*)\)$', rule).group(1).split(',')[1].strip().replace("'", '')
        rule='date'
        return (rule,result)
    elif rule.startswith('DateYY'):
        result = re.search(r'\(([^()]*)\)$', rule).group(1).split(',')[1].strip().replace("'", '')
        rule='date'
        return (rule,result)
    elif rule.startswith('RandomItem'):
        rule='randomItem'
        result = ''
        return (rule,result)
    elif rule.startswith('RandomBool'):
        rule = 'randomBool'
        result = ''
        return (rule,result)
    else:
        raise ValueError("Rule passed not in the list of defined ones")
##### Datetime Obfuscation #####
def add_days(curr_date,variance,rule):
    from datetime import datetime, timedelta
    ####
    if rule == 'datetime':
        curr_date = datetime.strptime(str(curr_date), '%Y-%m-%dT%H:%M:%S.%f') + timedelta(int(variance))
        curr_date = datetime.strftime(curr_date, '%Y-%m-%dT%H:%M:%S.%f')[:-3]
    elif rule == 'date':
        if str(curr_date) == '0':
            return curr_date
        else:
            curr_date = datetime.strftime(datetime.strptime(str(curr_date), '%Y%m') + timedelta(int(variance)), '%Y%m')
    return curr_date
def subtract_days(curr_date,variance,rule):
    from datetime import datetime, timedelta
    ####
    if rule == 'datetime':
        curr_date = datetime.strptime(str(curr_date), '%Y-%m-%dT%H:%M:%S.%f') - timedelta(int(variance))
        curr_date = datetime.strftime(curr_date, '%Y-%m-%dT%H:%M:%S.%f')[:-3]
    elif rule == 'date':
        if str(curr_date) == '0':
            return curr_date
        else:
            curr_date = datetime.strftime(datetime.strptime(str(curr_date), '%Y%m') + timedelta(int(variance)), '%Y%m')
    return curr_date
##### IDMap Obfuscation #####
def randomize_integer(value):
    low = 0
    high = 100000000
    random.seed(int(value))
    return random.randint(low, high)
def randomize_string(value):
    value = str(value)
    byt_value = value.encode('utf-8')
    int_value = int.from_bytes(byt_value, 'little')
    str_value = 'S' + str(int_value)[:11]
    if str_value[-2:] == '.0':
        str_value = str_value[:-2]
    return str_value
##### Numeric Obfuscation #####
def add_number(curr_number,variance):
    curr_number = float(curr_number)
    if curr_number.is_integer():
        curr_number = int(curr_number)
    curr_number += int(variance)
    return abs(curr_number)
def subtract_number(curr_number,variance):
    curr_number = float(curr_number)
    if curr_number.is_integer():
        curr_number = int(curr_number)
    curr_number -= int(variance)
    return abs(curr_number)
##### String Obfuscation #####
def num_obs(lst):
    import string
    import random
    ####
    if lst.isdigit():
        lst_fin = ''.join([random.choice(string.digits) for ind in range(len(lst))])
    elif lst.isalpha():
        lst_fin = ''.join([random.choice(string.ascii_letters) for ind in range(len(lst))])
    else:
        lst_fin = lst
    return lst_fin
def string_obfuscation(value,filter):
    import re
    ####
    list_substrings = re.findall(r'[A-Za-z]+|\d+| |[^\w\s]', value)
    if filter=='DEFAULT':
        list_substrings = [num_obs(x) for x in list_substrings]
        obfus_string = ''.join(list_substrings)
    elif filter == 'only char':
        list_substrings = [num_obs(x) if x.isalpha() else x for x in list_substrings]
        obfus_string = ''.join(list_substrings)
    elif filter == 'only numeric':
        list_substrings = [num_obs(x) if x.isdigit() else x for x in list_substrings]
        obfus_string = ''.join(list_substrings)
    else:
        obfus_string = None
    return obfus_string

#### Data Obfuscation ####
def data_obsfuscation(value, rule):
    import string
    import re
    from datetime import datetime, timedelta
    import random
    #### Process Rule ####
    rule,result = rule_procc(rule)
    #### String Obfuscation ####
    if rule == 'string':
        value = string_obfuscation(value,result)
    #### IDMap Obfuscation ####
    elif rule == 'ID':
        if result == 'string':
            value = randomize_string(value)
        elif result == 'int':
            value = randomize_int(value)
        else:
            value = None 
    #### Numeric Obfuscation ####
    elif rule == 'numeric':
        value = random.choice([add_number(value,result),subtract_number(value,result)])
    #### DateObfuscation && DatetimeObfuscation ####
    elif (rule == 'date') or (rule == 'datetime'):
        value = random.choice([add_days(value,result,rule),subtract_days(value,result,rule)])
    #### RandomItem ####
    elif rule == 'randomItem':
        value = random.choice(value)
    #### RandomBool ####
    elif rule == 'randomBool':
        value = random.randint(0, 1)
    else:
        value = None
    #### Return value #####
    return value
