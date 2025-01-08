import hashlib

my_frst_input = input('Enter first hash data: ')
my_secnd_input = input('Enter second hash data: ')

hash_obj = hashlib.md5(my_frst_input.encode())
hash_sec_obj = hashlib.md5(my_secnd_input.encode())

print(hash_obj.hexdigest())
print(hash_sec_obj.hexdigest())
