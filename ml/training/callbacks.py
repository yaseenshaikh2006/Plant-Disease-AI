"""
Training Callbacks Module
Plant Disease AI
"""

from pathlib import Path
from typing import List
import tensorflow as tf
from tensorflow.keras.callbacks import (
    ModelCheckpoint,
    EarlyStopping,
    ReduceLROnPlateau,
    CSVLogger
)


def get_training_callbacks(
    checkpoint_path: Path,
    csv_log_path: Path,
    early_stopping_patience: int = 6,
    reduce_lr_patience: int = 3,
    reduce_lr_factor: float = 0.2,
    min_lr: float = 1e-6
) -> List[tf.keras.callbacks.Callback]:
    """
    Creates standard academic training callbacks:
    - Best model checkpointing based on val_loss
    - Early stopping to prevent overfitting
    - Dynamic learning rate reduction on plateaus
    - CSV logging for reproducible academic charting
    """
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    csv_log_path.parent.mkdir(parents=True, exist_ok=True)

    callbacks = [
        ModelCheckpoint(
            filepath=str(checkpoint_path),
            monitor="val_loss",
            verbose=1,
            save_best_only=True,
            mode="min"
        ),
        EarlyStopping(
            monitor="val_loss",
            patience=early_stopping_patience,
            verbose=1,
            restore_best_weights=True,
            mode="min"
        ),
        ReduceLROnPlateau(
            monitor="val_loss",
            factor=reduce_lr_factor,
            patience=reduce_lr_patience,
            min_lr=min_lr,
            verbose=1,
            mode="min"
        ),
        CSVLogger(
            filename=str(csv_log_path),
            separator=",",
            append=False
        )
    ]
    return callbacks
