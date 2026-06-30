import torch


def test_pytorch():
    print(f"PyTorch Version: {torch.__version__}")

    # Create a random tensor
    x = torch.rand(5, 3)
    print("\nRandom Tensor (5x3):")
    print(x)


    if torch.backends.mps.is_available():
        mps_device = torch.device("mps")
        x_mps = x.to(mps_device)
        print(f"Tensor moved to MPS device: {x_mps.device}")
    else:
        print("\nMPS is not available. Using CPU instead.")

if __name__ == "__main__":
    test_pytorch()
