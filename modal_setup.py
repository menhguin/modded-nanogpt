import subprocess
import sys
import os

def run_command(command, description):
    print(f"\n=== {description} ===")
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Output: {e.output}")
        return False

def main():
    # Check Python version
    print(f"Python version: {sys.version}")
    
    # Check if pip is installed
    if not run_command("pip --version", "Checking pip installation"):
        print("Please install pip first")
        return

    # Install or upgrade pip
    run_command("python -m pip install --upgrade pip", "Upgrading pip")

    # Install Modal
    if not run_command("pip install modal", "Installing Modal"):
        print("Failed to install Modal")
        return

    # Check Modal version
    run_command("python -m modal --version", "Checking Modal version")

    # Create test directory
    test_dir = "modal_test"
    os.makedirs(test_dir, exist_ok=True)
    print(f"\nCreated test directory: {test_dir}")

    # Create GPU test script
    gpu_test_script = '''import modal

# Define the Modal app
stub = modal.Stub("gpu-test")

# Create an image that includes PyTorch
image = modal.Image.debian_slim().pip_install("torch")

@stub.function(gpu="A10G", image=image)
def test_gpu():
    import torch
    
    # Check if CUDA is available
    print(f"CUDA available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        # Print device information
        print(f"Current device: {torch.cuda.get_device_name(0)}")
        print(f"Device count: {torch.cuda.device_count()}")
        
        # Run a simple GPU computation
        x = torch.rand(3, 3, device="cuda")
        y = torch.rand(3, 3, device="cuda")
        z = x @ y
        print("\\nTest matrix multiplication result:")
        print(z)
    else:
        print("No GPU available!")

@stub.local_entrypoint()
def main():
    test_gpu.remote()
'''

    # Write GPU test script
    with open(os.path.join(test_dir, "gpu_test.py"), "w") as f:
        f.write(gpu_test_script)
    print("Created GPU test script: gpu_test.py")

    print("\n=== Setup Complete ===")
    print("\nNext steps:")
    print("1. Run 'python -m modal setup' to configure your Modal token")
    print("2. cd into the modal_test directory")
    print("3. Run 'modal run gpu_test.py' to test GPU functionality")

if __name__ == "__main__":
    main()