import torch
import time

epoch = 100000

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# device = torch.device("cpu")
print(f"Using device: {device}")

def generate(x, parameters, noise_added):
    noise = 0.1 * torch.rand(x.size(0), 1, device=device)
    if noise_added:
        return torch.matmul(x, parameters) + 2 + noise
    else:
        return torch.matmul(x, parameters) + 2


def Create_Dataset(samples, features, noise_added):
    x = torch.rand(samples, features, device=device) # sample number of data points between 0 and 1
    parameters_true = torch.rand(features, 1, device=device) # True Parameters for the training set
    y_true = generate(x, parameters_true, noise_added) # Ground Truth
    return x, y_true


def Closed_form(X, y_true):
    ones = torch.ones(X.size(0), 1, device=device)
    X_aug = torch.cat([X, ones], dim=1)

    start = time.time()

    # closed form update
    W_closed = torch.inverse(X_aug.T @ X_aug) @ X_aug.T @ y_true
    # Mathematically stable version
    # W_closed = torch.linalg.lstsq(X_aug, y_true).solution

    y_pred_closed = X_aug @ W_closed
    # MSE
    loss = torch.mean((y_pred_closed - y_true) ** 2)

    # Sync CUDA before stopping timer (CUDA ops are async, so we must wait for completion)
    if device.type == "cuda":
        torch.cuda.synchronize()

    elapsed = time.time() - start
    print(f"MSE for closed form: {loss.item()}")
    print(f"Time for closed form (on {device}): {elapsed:.6f}s")


def Optimization_Form(X, y_true, lr=0.01):
    ones = torch.ones(X.size(0), 1, device=device)
    X_aug = torch.cat([X, ones], dim=1)

    W_init = torch.rand(X_aug.size(1), 1, device=device)
    W_with_loss_backward = W_init.clone().detach().requires_grad_(True)
    W_without_loss_backward = W_init.clone().detach() # no need for gradient tracking if calculating manually

    start = time.time()

    for i in range(epoch):
        y_pred_with_loss_backward = X_aug @ W_with_loss_backward
        loss_with_backward = torch.mean((y_pred_with_loss_backward - y_true) ** 2)

        y_pred_without_loss_backward = X_aug @ W_without_loss_backward
        loss_without_backward = torch.mean((y_pred_without_loss_backward - y_true) ** 2)

        # with loss.backward
        loss_with_backward.backward()

        with torch.no_grad():
            W_with_loss_backward -= lr * W_with_loss_backward.grad
            W_with_loss_backward.grad.zero_()

        # without loss.backward
        grad_W = (2 / X_aug.size(0)) * X_aug.T @ (y_pred_without_loss_backward - y_true)

        W_without_loss_backward -= lr * grad_W

        if i == epoch - 1:
            print(f"Epoch {i} with loss.backward, Loss: {loss_with_backward.item()}")
            print(f"Epoch {i} without loss.backward, Loss: {loss_without_backward.item()}")

    # Sync CUDA before stopping timer (CUDA ops are async, so we must wait for completion)
    if device.type == "cuda":
        torch.cuda.synchronize()

    elapsed = time.time() - start
    print(f"Time for optimization form (on {device}): {elapsed:.6f}s")


def main():
    #Create the Dataset
    #swap the True or False to add or remove noise
    #If no noise is added MSE should be exactly or nearly zero as it would be exactly straight line
    X, y_true = Create_Dataset(5000, 10, True) 

    # Why closed-form solution is often not used in practice:
    # 1. Computational cost: Inverting X^T X takes O(n^3), slow for large datasets
    # 2. Memory issues: Storing X^T X can be huge if there are many features
    # 3. Numerical instability: Matrix inversion can be unstable if X^T X is nearly singular
    # 4. Less flexible: Hard to include regularization, mini-batch, or online updates
    # -> Gradient descent scales better and works well in deep learning
    Closed_form(X, y_true)

    # Why we use iterative optimization (gradient descent) instead of closed-form:
    # 1. Scales better: Closed-form requires inverting X^T X, which is slow and memory-heavy for large datasets
    # 2. Works with mini-batches / online updates, which closed-form cannot handle
    # 3. Supports complex models like neural networks where no closed-form exists
    # 4. Easy to include regularization (L1/L2) directly in the update step
    Optimization_Form(X, y_true)


main()


