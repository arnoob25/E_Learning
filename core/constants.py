# Use with permission required mixin or decorator
PERMISSION_DENIED_MESSAGE = 'You do not have permission to view this page.'

# Use when displaying lists

def listHeading(listname):
    return f'List of {listname.lower()}s'

GENERATE_PAGE_HEADING = listHeading

def emptylistmessage(listname):
    return f'No {listname.lower()}s yet'

GENERATE_EMPTY_LIST_MESSAGE = emptylistmessage

