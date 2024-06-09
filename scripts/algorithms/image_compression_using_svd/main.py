import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color

# Load the grayscale image
image_path = '/mnt/data/image.png'
image = io.imread(image_path)
gray_image = color.rgb2gray(image)

# Compute the SVD of the image matrix
U, S, Vt = np.linalg.svd(gray_image, full_matrices=False)

def reconstruct_image(U, S, Vt, rank):
    """
    Reconstruct the image using the first 'rank' singular values.
    """
    S_truncated = np.zeros((rank, rank))
    np.fill_diagonal(S_truncated, S[:rank])
    return np.dot(U[:, :rank], np.dot(S_truncated, Vt[:rank, :]))

# Ranks for the approximation
ranks = [5, 25, 100]

# Plot the original and reconstructed images
fig, axes = plt.subplots(1, len(ranks) + 1, figsize=(15, 5))
axes[0].imshow(gray_image, cmap='gray')
axes[0].set_title('Original image')
axes[0].axis('off')

for i, rank in enumerate(ranks):
    reconstructed_image = reconstruct_image(U, S, Vt, rank)
    axes[i + 1].imshow(reconstructed_image, cmap='gray')
    axes[i + 1].set_title(f'Rank {rank} approximation')
    axes[i + 1].axis('off')

plt.tight_layout()
plt.savefig('/mnt/data/reconstructed_images.png')
plt.close()

# Plot the singular values
plt.figure(figsize=(8, 6))
plt.plot(S, 'b-o')
plt.yscale('log')
plt.xlabel('Index $i$')
plt.ylabel('Singular value $\sigma_i$')
plt.title('Singular values of the image of the forest')
plt.grid(True)
plt.savefig('/mnt/data/singular_values.png')
plt.close()

# Calculate the energy ratio for different ranks
total_energy = np.sum(S**2)
energy_ratios = np.cumsum(S**2) / total_energy

# Plot the energy ratio as a function of the truncated SVD size
plt.figure(figsize=(8, 6))
plt.plot(energy_ratios, 'b-o')
plt.xlabel('Truncated SVD size $r$')
plt.ylabel('Energy ratio $\mathcal{E}(r)$')
plt.title('Energy ratios in dependence on the size of the truncated SVD')
plt.axhline(y=0.99, color='r', linestyle='--')
plt.grid(True)
plt.savefig('/mnt/data/energy_ratios.png')
plt.close()
