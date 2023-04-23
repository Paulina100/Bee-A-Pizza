from order_generation import *

slices = generate_n_slices_per_customer(2,5,7)
preferences = generate_preferences(7, 10, 3, 3)
acts = assign_customers_to_slices(slices)
gpbs = get_preferences_by_slice(preferences, slices)
print(slices)
print(preferences)
# print(acts)
# print(gpbs)
customer_likes = np.where(preferences == 1)
print(customer_likes)


def export_generated_customers(preferences: np.ndarray, n_slices_per_customer: np.ndarray):
    n_customers = len(preferences)
    # n_slices_per_customer
    customer_likes = np.where(preferences == 1)