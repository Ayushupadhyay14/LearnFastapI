from tables import create_tables
from services import *

# Create Tables
create_tables()

# Create Data
# create_user("sonam", "sonam@example.com")
# create_user("raj", "raj@example.com")
# create_post(1, "Hello World", "This is Sonam's first post")
# create_post(1, "Bye World", "This is Sonam's second post")
# create_post(1, "No World", "This is Sonam's third post")
# create_post(2, "Raj's Post 1", "Hi from Raj! 1")
# create_post(2, "Raj's Post 2", "Hi from Raj! 2")

print(get_posts_with_author())