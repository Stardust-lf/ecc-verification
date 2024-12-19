for x in range(256):
    # Calculate the polynomial result modulo 512
    result = (x**8 + x**2 + x**1 + 1) % 512

    # Check if the 9th bit (bit at index 8) is 1
    if (result >> 8) & 1 == 1:
        print(f"x: {x}, result: {bin(result)}")
