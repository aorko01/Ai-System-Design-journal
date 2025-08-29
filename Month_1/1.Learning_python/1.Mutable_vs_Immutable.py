# IMMUTABLE vs MUTABLE

# IMMUTABLE:
# Immutable Objects Cannot be changed after creation.
# Examples: int,float,str,tuple,frozenset,bytes

x = "hello"
print(id(x))   # object ID in memory
x = x + " world"   # looks like modification
print(id(x))   # different ID → new object created

# MUTABLE:
# Mutable Objects Can be changed after creation.
# Examples:list,dict,set,bytearray,custom objects (usually)

lst = [1, 2, 3]
print(id(lst))  # memory location
lst.append(4)   # modifies in place
print(id(lst))  # same ID → same object updated

