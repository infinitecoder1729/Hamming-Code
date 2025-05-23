# hamming_example.py

from Hamming import HammingCode

# Step 1: Initialize HammingCode with r=3 (Hamming(7,4))
hc = HammingCode(r=3)

# Step 2: Define 4 data bits to encode
data_bits = [1, 0, 1, 1]
print("Original Data Bits:", data_bits)

# Step 3: Encode the data bits into a codeword
codeword = hc.encode(data_bits)
print("Encoded Codeword:", codeword)

# Step 4: Simulate a single-bit error at position 3
error_position = 3
corrupted_codeword = hc.simulate_error(codeword, error_position)
print(f"Corrupted Codeword (Error at position {error_position}):", corrupted_codeword)

# Step 5: Decode the corrupted codeword
decoded_data, correction_applied = hc.decode(corrupted_codeword)
print("Decoded Data Bits:", decoded_data)
print("Was Correction Applied?", correction_applied)

# Step 6: Visualize the structure of the Hamming code
hc.plot_structure()

# Step 7: Visualize error simulation and correction
hc.plot_error_simulation(data_bits)
