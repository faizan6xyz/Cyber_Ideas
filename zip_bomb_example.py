
import zipfile
import os
# Create a zip bomb demonstration (safe, small scale)
def create_mini_zip_bomb():
    # Step 1: Create highly compressible data
    data = b'A' * 1000000  # 1 MB of repeated 'A'
    # Step 2: Compress it multiple times
    current_data = data
    for i in range(3):
        # Write to a temporary zip
        temp_zip = f'temp_{i}.zip'
        with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
            if i == 0:
                zf.writestr('data.txt', current_data.decode())
            else:
                zf.write(f'temp_{i-1}.zip', f'data_{i-1}.zip')
        # Read the compressed file
        with open(temp_zip, 'rb') as f:
            current_data = f.read()
        print(f"Layer {i}: {len(current_data)} bytes")
    # Cleanup
    for i in range(3):
        if os.path.exists(f'temp_{i}.zip'):
            os.remove(f'temp_{i}.zip')
    print(f"\nOriginal data: {len(data)} bytes (1 MB)")
    print(f"Final compressed: {len(current_data)} bytes")
    print(f"Compression ratio: {len(data)/len(current_data):.1f}x")
create_mini_zip_bomb()

# Result 
# Layer 0: 1100 bytes
# Layer 1: 213 bytes
# Layer 2: 285 bytes

# Original data: 1000000 bytes (1 MB)
# Final compressed: 285 bytes
# Compression ratio: 3508.8x
