update_path = []
print(len(update_path))
print(
tuple([x[0] for x in update_path]) if len(update_path) > 1 else f"('{[x[0] for x in update_path][0]}')" if len(update_path) == 1 else "('')"
)


print(
f"""
{tuple([x[0] for x in update_path]) if len(update_path) > 1 else 
f"('{[x[0] for x in update_path][0]}')" if len(update_path) == 1 else "('')"}
"""
)