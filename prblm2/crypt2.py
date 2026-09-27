import math

# read ciphertext 
with open('output.txt', 'r') as f:
    saved_ciphertext = f.read()

clean_cipher = []
for char in saved_ciphertext:
    if char.isalpha():
        clean_cipher.append(char)

# Create a string_pattern searching
cipher_string = "".join(clean_cipher) 

print("--- (a) Predicting Key Length (Kasiski Examination) ---")

#(GCD METHOD)
distances = []
found_patterns = [] # Added to show what found

# Look for repeated 3-letter patterns
for i in range(len(cipher_string) - 5):
    pattern = cipher_string[i:i+3]
    next_occurrence = cipher_string.find(pattern, i + 3)
    
    if next_occurrence != -1:
        distance = next_occurrence - i
        distances.append(distance)
        if len(found_patterns) < 20:     # currenty found_patt ee kichu nei, 10 porjnoto Save the first 10 to display
            found_patterns.append((pattern, distance))

best_len = 1       #if case no patterns are found

if len(distances) > 0:
    print("[+] Found repeating 3-letter patterns! Here are a few examples:")
    for pat, dist in found_patterns:
        print(f"    -> Pattern '{pat}' repeated at distance: {dist}")
        
    print("\n    Calculating Greatest Common Divisor (GCD) of these distances...")
    current_gcd = distances[0]
    print(f"    -> Starting GCD with first distance: {current_gcd}")
    
    # Calculate GCD of the first 20 valid distances (prevents noise from massive texts)
    for d in distances[1:20]: 
        new_gcd = math.gcd(current_gcd, d)
        print(f"    -> GCD({current_gcd}, {d}) = {new_gcd}")
        current_gcd = new_gcd
    
    if current_gcd > 1:
        best_len = current_gcd
        print(f"\nSUCCESS: The mathematical GCD is {best_len}. Predicting Key Length = {best_len} ")
    else:
        print("\n-> GCD reduced to 1. The patterns might be coincidental. Defaulting to length 1 (Caesar).")
else:
    print("-> No repeating sequences found. Defaulting to length 1.")



#predict the key
print("\n--- (b) Predicting the Key & Message ---")
print("[+] Frequency Analysis per Column.")
print("[+] Assuming the most common English letter is 'e' (Index 30 on our 0-51 scale).")
print("[+] Mathematical Formula: Key_Value = (Cipher_Value - 30) % 52\n")

predicted_key = ""
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

for col_index in range(best_len):
    column = []
    for i in range(len(clean_cipher)):
        if i % best_len == col_index:
            column.append(clean_cipher[i])
            
    max_count = 0
    most_freq_char = 'A'
    for letter in alphabet:
        count = column.count(letter)
        if count > max_count:
            max_count = count
            most_freq_char = letter
            
    # Convert Cipher char to 0-51 scale
    if 'A' <= most_freq_char <= 'Z':  c_val = ord(most_freq_char) - 65
    else: c_val = ord(most_freq_char) - 97 + 26
        
    # Assume the most frequent character is 'e' (index 30 on 0-51 scale)
    k_val = (c_val - 30) % 52
    
    # Convert Key value back to char
    if 0 <= k_val <= 25: 
        key_char = chr(k_val + 65)
    else: 
        key_char = chr(k_val - 26 + 97)
        
    predicted_key += key_char
    
    # Printing the math logic
    print(f"    Column {col_index + 1}: Most frequent character is '{most_freq_char}' (Numeric Value: {c_val})")
    print(f"    -> Math: ({c_val} - 30) % 52 = {k_val}")
    print(f"    -> Converting {k_val} back to character = '{key_char}'")
    print(f"    ------------------------------------------------")

print(f"\n-> Final Predicted Key is: {predicted_key} ")


#decrypting predicted the msg
predicted_message = ""

for i in range(len(clean_cipher)):
    c_char = clean_cipher[i]
    k_char = predicted_key[i % best_len]
    
    # Get numeric values
    if 'A' <= c_char <= 'Z': c_val = ord(c_char) - 65
    else: c_val = ord(c_char) - 97 + 26
        
    if 'A' <= k_char <= 'Z': k_val = ord(k_char) - 65
    else: k_val = ord(k_char) - 97 + 26
        
    #Vigenere subtraction
    p_val = (c_val - k_val) % 52
    
    # convert back to character
    if 0 <= p_val <= 25: predicted_message += chr(p_val + 65)
    else: predicted_message += chr(p_val - 26 + 97)

with open('predicted.txt', 'w') as f:
    f.write(predicted_message)

print("\n--- (c) Execution & Comparison ---")
print("SUCCESS: Decryption complete. Check 'predicted.txt'!")