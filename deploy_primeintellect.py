import os
import time
from dotenv import load_dotenv
from primeintellect import Client as PrimeIntellectClient

# Load environment variables from .env file
load_dotenv()

def deploy_to_primeintellect():
    # Get API key from environment
    api_key = os.getenv('PRIMEINTELLECT_API_KEY')
    if not api_key:
        raise ValueError("PRIMEINTELLECT_API_KEY not found in environment variables")
    
    # Initialize Prime Intellect client
    client = PrimeIntellectClient(api_key=api_key)
    
    print("Starting speedrun attempt...")
    print("Target: Train on 8x H100s, aiming for <4 minutes")
    print("Current record: ~4 minutes")
    
    # Configure the deployment for maximum speed
    config = {
        "image": "pytorch/pytorch:2.2.2-cuda12.1-cudnn8-runtime",  # Optimized PyTorch image
        "gpu_type": "H100",
        "num_gpus": 8,  # 8x H100 SXM5 GPUs required
        "command": "python -m torch.distributed.run --nproc_per_node=8 train_gpt.py",
        "env_vars": {
            "CUDA_VISIBLE_DEVICES": "0,1,2,3,4,5,6,7",
            "PRIMEINTELLECT_API_KEY": api_key,
            "MAX_RUNTIME_MINUTES": "10",  # Auto-terminate if exceeds 10 minutes
            "PYTORCH_CUDA_ALLOC_CONF": "max_split_size_mb=512"  # Optimize CUDA memory allocation
        },
        "timeout_minutes": 10  # Hard timeout after 10 minutes
    }
    
    start_time = time.time()
    try:
        # Deploy the training job
        print("Deploying to Prime Intellect...")
        deployment = client.deploy(config)
        print(f"Deployment started with ID: {deployment.id}")
        print("Monitor your training at: https://app.primeintellect.ai")
        
        # Monitor the deployment
        while True:
            status = deployment.get_status()
            elapsed_minutes = (time.time() - start_time) / 60
            
            print(f"Status: {status}, Elapsed time: {elapsed_minutes:.2f} minutes")
            
            if status == "completed":
                print("Training completed successfully!")
                break
            elif status == "failed":
                print("Training failed!")
                break
            elif elapsed_minutes > 10:
                print("Exceeded 10 minute limit, terminating...")
                deployment.terminate()
                break
                
            time.sleep(10)  # Check status every 10 seconds
            
    except Exception as e:
        print(f"Error during deployment: {e}")
        
    finally:
        elapsed_minutes = (time.time() - start_time) / 60
        print(f"\nTotal time: {elapsed_minutes:.2f} minutes")

if __name__ == "__main__":
    deploy_to_primeintellect() 