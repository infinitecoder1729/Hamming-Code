import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple

class HammingCode:
    """
    Hamming Code implementation supporting (2^r - 1, 2^r - r - 1) codes.
    Allows encoding, decoding (with single-bit error correction), and visualization.

    Usage:
        ham = HammingCode(r=3)
        codeword = ham.encode([1,0,1,1])
        decoded, corrected = ham.decode(codeword_with_error)

    For industrial integration, import HammingCode and call encode()/decode().
    """
    def __init__(self, r: int):
        self.r = r
        self.n = 2**r - 1
        self.k = self.n - r
        # parity bit positions (1-based indexing)
        self.parity_positions = [2**i for i in range(r)]

    def encode(self, data_bits: List[int]) -> List[int]:
        """Encode data_bits into Hamming codeword."""
        if len(data_bits) != self.k:
            raise ValueError(f"Data length must be {self.k}")
        code = [0] * (self.n + 1)  # 1-based indexing
        # Place data bits
        j = 0
        for i in range(1, self.n+1):
            if i not in self.parity_positions:
                code[i] = data_bits[j]
                j += 1
        # Compute parity bits
        for p in self.parity_positions:
            # parity covers bits with binary index having p's bit set
            bits = [code[i] for i in range(1, self.n+1) if i & p]
            code[p] = sum(bits) % 2
        return code[1:]

    def decode(self, codeword: List[int]) -> Tuple[List[int], bool]:
        """Decode codeword, correct single-bit error if present.
        Returns (data_bits, corrected_flag)."""
        if len(codeword) != self.n:
            raise ValueError(f"Codeword length must be {self.n}")
        # compute syndrome
        syndrome = 0
        for p in self.parity_positions:
            bits = [codeword[i-1] for i in range(1, self.n+1) if i & p]
            if sum(bits) % 2:
                syndrome += p
        code = codeword.copy()
        corrected = False
        if syndrome != 0:
            code[syndrome-1] ^= 1
            corrected = True
        # extract data bits
        data = [code[i-1] for i in range(1, self.n+1) if i not in self.parity_positions]
        return data, corrected

    def simulate_error(self, codeword: List[int], pos: int) -> List[int]:
        """Flip the bit at position pos (1-based) to simulate error."""
        if pos < 1 or pos > self.n:
            raise IndexError("Position out of range")
        cw = codeword.copy()
        cw[pos-1] ^= 1
        return cw

    # --- Visualization methods ---
    def plot_structure(self):
        """Show the bit layout of a codeword (parity vs data)"""
        positions = list(range(1, self.n+1))
        types = ['Parity' if pos in self.parity_positions else 'Data' for pos in positions]
        colors = ['red' if t=='Parity' else 'blue' for t in types]
        plt.figure()
        plt.bar(positions, [1]*self.n, color=colors)
        plt.xticks(positions)
        plt.xlabel('Bit Position')
        plt.title(f'Hamming({self.n},{self.k}) Structure')
        plt.show()

    def plot_error_simulation(self, data_bits: List[int]):
        """Visualize encoding, error introduction at each position, and correction."""
        orig = self.encode(data_bits)
        positions = list(range(1, self.n + 1))  # 1-based positions

        for i in positions:
            err = self.simulate_error(orig, i)
            decoded_data, corrected = self.decode(err)
            corrected_codeword = self.encode(decoded_data)

            fig, axes = plt.subplots(3, 1, figsize=(8, 6))

            axes[0].bar(positions, orig)
            axes[0].set_title('Original Codeword')

            axes[1].bar(positions, err)
            axes[1].set_title(f'Corrupted Codeword (Error at position {i})')

            axes[2].bar(positions, corrected_codeword)
            axes[2].set_title('Corrected Codeword')

            plt.tight_layout()
            plt.show()


# Example CLI for industrial usage
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Hamming Code encoder/decoder')
    parser.add_argument('r', type=int, help='Number of parity bits')
    parser.add_argument('--encode', type=str, help='Data bits as comma-separated list')
    parser.add_argument('--decode', type=str, help='Codeword bits as comma-separated list')
    args = parser.parse_args()
    ham = HammingCode(args.r)
    if args.encode:
        data = list(map(int, args.encode.split(',')))
        print('Codeword:', ham.encode(data))
    if args.decode:
        cw = list(map(int, args.decode.split(',')))
        data, corr = ham.decode(cw)
        print('Decoded Data:', data)
        print('Correction applied:', corr)
