import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from torch.utils.data import Dataset, DataLoader, Subset
from sklearn.model_selection import KFold

class GenotypePhenotypeDataset(Dataset):
    def __init__(self, genotypes, phenotypes):
        self.genotypes = torch.tensor(genotypes, dtype=torch.float32)
        self.phenotypes = torch.tensor(phenotypes, dtype=torch.float32)

    def __len__(self):
        return len(self.genotypes)

    def __getitem__(self, index):
        return self.genotypes[index], self.phenotypes[index]

class GenotypeModel(nn.Module):
    def __init__(self, input_size, output_size):
        super(GenotypeModel, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_size, 128),  # Input layer
            nn.ReLU(),                  # Activation function
            # nn.Dropout(0.1),  # Dropout layer

            nn.Linear(128, 32),         # Hidden layer
            nn.ReLU(),
            # nn.Dropout(0.1),  # Dropout layer

            nn.Linear(32, output_size)  # Output layer
        )

    def forward(self, x):
        return self.fc(x)
    
class FitnessFunction:
    def __init__(self):
        self.model = None
        self.best_mean_val_loss = None  # Track the best mean validation loss

    def train_with_cross_validation(self, genotypes, phenotypes, is_classification=False):
        # Hyperparameters
        learning_rate = 0.01
        epochs = 20
        batch_size = 32
        k_folds = 10

        # Dataset and KFold Splitter
        dataset = GenotypePhenotypeDataset(genotypes, phenotypes)
        kfold = KFold(n_splits=k_folds, shuffle=True, random_state=42)

        # Cross-validation results
        fold_results = []
        accuracy_results = []
        best_model = None
        best_mean_val_loss = float('inf')

        for fold, (train_ids, val_ids) in enumerate(kfold.split(dataset)):
            print(f"--- Fold {fold + 1}/{k_folds} ---")

            # Subset datasets
            train_subsampler = Subset(dataset, train_ids)
            val_subsampler = Subset(dataset, val_ids)

            # DataLoaders
            train_loader = DataLoader(train_subsampler, batch_size=batch_size, shuffle=True)
            val_loader = DataLoader(val_subsampler, batch_size=batch_size, shuffle=False)

            # Model, Loss, Optimizer
            input_size = genotypes.shape[1]
            output_size = 1 if not is_classification else len(np.unique(phenotypes))
            model = GenotypeModel(input_size, output_size)

            # Loss function: MSE for regression, CrossEntropy for classification
            criterion = nn.CrossEntropyLoss() if is_classification else nn.MSELoss()
            optimizer = optim.Adam(model.parameters(), lr=learning_rate)

            # Training Loop
            for epoch in range(epochs):
                model.train()
                for inputs, targets in train_loader:
                    optimizer.zero_grad()
                    outputs = model(inputs)

                    # Adjust target shape for classification
                    if is_classification:
                        targets = targets.long()
                    loss = criterion(outputs.squeeze(), targets)
                    loss.backward()
                    optimizer.step()

            # Validation Loop
            model.eval()
            val_loss = 0.0
            correct = 0
            total = 0
            with torch.no_grad():
                for inputs, targets in val_loader:
                    outputs = model(inputs)
                    if is_classification:
                        targets = targets.long()
                        _, predicted = torch.max(outputs, 1)  # Get predicted class
                        correct += (predicted == targets).sum().item()
                        total += targets.size(0)
                    loss = criterion(outputs.squeeze(), targets)
                    val_loss += loss.item()

            val_loss /= len(val_loader)
            fold_results.append(val_loss)

            if is_classification:
                fold_accuracy = correct / total
                accuracy_results.append(fold_accuracy)
                print(f"Fold {fold + 1}, Accuracy: {fold_accuracy:.4f}")

            print(f"Fold {fold + 1}, Validation Loss: {val_loss:.4f}")

        # Calculate the mean validation loss across all folds
        mean_val_loss = np.mean(fold_results)
        print(f"Mean Validation Loss: {mean_val_loss:.4f}")

        # Save the best model based on mean validation loss
        if mean_val_loss < best_mean_val_loss:
            best_mean_val_loss = mean_val_loss
            self.model = model  # Save the last model trained in this cross-validation run

        self.best_mean_val_loss = best_mean_val_loss  # Store the best mean validation loss
        return best_mean_val_loss

    def predict(self, genotypes):
        """
        Predict phenotypes based on the input genotypes.
        
        Args:
            genotypes (numpy.ndarray or torch.Tensor): Input genotypes to predict for.

        Returns:
            numpy.ndarray: Predicted phenotypes.
        """
        if self.model is None:
            raise ValueError("The model has not been trained yet. Please train the model before making predictions.")

        # Ensure input is a tensor
        if isinstance(genotypes, np.ndarray):
            genotypes = torch.tensor(genotypes, dtype=torch.float32)

        # Put the model in evaluation mode
        self.model.eval()
        with torch.no_grad():
            predictions = self.model(genotypes)

        # Return predictions as a numpy array
        return predictions.numpy()