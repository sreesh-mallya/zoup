LOCATIONS = [
    ('kochi', 'Kochi'),
    ('bengaluru', 'Bengaluru'),
    ('mumbai', 'Mumbai'),
]

CUISINES = (
    ('North Indian', 'North Indian'),
    ('South Indian', 'South Indian'),
    ('Indian', 'Indian'),
    ('Tandoor', 'Tandoor'),
    ('Chinese', 'Chinese'),
    ('Thai', 'Thai'),
    ('Asian', 'Asian'),
    ('Keralite', 'Keralite'),
    ('Karnataka', 'Karnataka'),
    ('Hyderabad', 'Hyderabad'),
    ('Italian', 'Italian'),
    ('American', 'American'),
    ('English', 'English'),
    ('Other', 'Other'),
)

ITEM_TYPES = (
    ('Appetizer', 'Appetizer'),
    ('Main Course', 'Main Course'),
    ('Dessert', 'Dessert'),
    ('Beverage', 'Beverage')
)

ACCOUNT_TYPES = {
    'SUPERUSER': 0,
    'ADMIN': 1,
    'RESTAURANT': 2,
    'STAFF': 3,
    'CUSTOMER': 4
}

ORDER_STATUS_CHOICES = (
    ('placed', 'Placed'),
    ('accepted', 'Accepted'),
    ('preparing', 'Preparing'),
    ('prepared', 'Prepared'),
    ('picked-up', 'Picked Up'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
)
