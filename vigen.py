# 1. READ THE FILES
with open('input.txt', 'r') as f:
    raw_plaintext = f.read()

with open('key.txt', 'r') as f:
    raw_key = f.read()



# 2. OPERATION (A): CLEAN THE TEXT
clean_pt = ""
for char in raw_plaintext:
    if ('A' <= char <= 'Z') or ('a' <= char <= 'z'):
        clean_pt += char

clean_k = ""
for char in raw_key:
    if ('A' <= char <= 'Z') or ('a' <= char <= 'z'):
        clean_k += char


#ENCRYPT (MOD 52)
ciphertext = ""
key_length = len(clean_k)

for i in range(len(clean_pt)):
    p_char = clean_pt[i]
    k_char = clean_k[i % key_length]
    
    #Convert Plaintext letter to a number between 0 and 51
    if 'A' <= p_char <= 'Z':
        p_val = ord(p_char) - ord('A')      # A-Z becomes 0 to 25
    else:
        p_val = ord(p_char) - ord('a') + 26 # a-z becomes 26 to 51
        
    #Convert Key letter to a number between 0 and 51
    if 'A' <= k_char <= 'Z':
        k_val = ord(k_char) - ord('A')
    else:
        k_val = ord(k_char) - ord('a') + 26
        
    #The Mod 52 Math
    c_val = (p_val + k_val) % 52
    
    #Convert the number back into a letter
    if c_val < 26:
        ciphertext += chr(c_val + ord('A'))      # It's an uppercase letter
    else:
        ciphertext += chr(c_val - 26 + ord('a')) # It's a lowercase letter



#Format TO 5 CHARACTERS
formatted_ciphertext = ""
for i in range(len(ciphertext)):
    formatted_ciphertext += ciphertext[i]
    # Add a space every 5 characters, unless it's the very end of the text
    if (i + 1) % 5 == 0 and (i + 1) != len(ciphertext):
        formatted_ciphertext += " "

with open('output.txt', 'w') as f:
    f.write(formatted_ciphertext)
print("Encryption finished. Check 'output.txt'.")



#DECRYPT
with open('output.txt', 'r') as f:
    saved_ciphertext = f.read()

# Remove the spaces we added in Operation before
unformatted_ciphertext = ""
for char in saved_ciphertext:
    if char != " ":
        unformatted_ciphertext += char

decrypted_message = ""

for i in range(len(unformatted_ciphertext)):
    c_char = unformatted_ciphertext[i]
    k_char = clean_k[i % key_length]
    
    #Convert Ciphertext letter to a number between 0 and 51
    if 'A' <= c_char <= 'Z':
        c_val = ord(c_char) - ord('A')
    else:
        c_val = ord(c_char) - ord('a') + 26
        
    #Convert Key letter to a number between 0 and 51
    if 'A' <= k_char <= 'Z':
        k_val = ord(k_char) - ord('A')
    else:
        k_val = ord(k_char) - ord('a') + 26
        
    #The Mod 52 Math (Subtraction for decryption)
    p_val = (c_val - k_val) % 52
    
    #Convert the number back into a letter
    if p_val < 26:
        decrypted_message += chr(p_val + ord('A'))
    else:
        decrypted_message += chr(p_val - 26 + ord('a'))



# 6.PRINT RESULTS
print("\n--- Verification ---")
print(f"Original clean message : {clean_pt}")
print(f"Decoded message        : {decrypted_message}")
if clean_pt == decrypted_message:
    print("\nSuccess: The decoded message matches!")