import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Tuple, Optional
from dataclasses import dataclass
from pathlib import Path
import logging

# scikit-learn 1.3.0
from sklearn.preprocessing import MinMaxScaler

import tensorflow as tf
import tensorflow_addons as tfa  # 引入 tensorflow_addons 库

layers = tf.keras.layers
models = tf.keras.models
callbacks = tf.keras.callbacks

@dataclass
class ModelConfig:
    sequence_length: int = 60
    batch_size: int = 32
    learning_rate: float = 0.001
    epochs: int = 50
    input_channels: int = 5  # OHLCV
    mixed_precision: bool = True

# 如果支持GPU则启用混合精度
if tf.config.list_physical_devices('GPU'):
    tf.keras.mixed_precision.set_global_policy('mixed_float16')

class CryptoCNN(models.Model):
    def __init__(self, config: ModelConfig):
        super().__init__()

        self.feature_extractor = tf.keras.Sequential([
            layers.Conv1D(64, kernel_size=3, padding='same'),
            layers.BatchNormalization(),
            layers.ReLU(),
            layers.MaxPooling1D(2),
            layers.Dropout(0.2),

            layers.Conv1D(128, kernel_size=3, padding='same'),
            layers.BatchNormalization(),
            layers.ReLU(),
            layers.MaxPooling1D(2),
            layers.Dropout(0.2),

            layers.Conv1D(256, kernel_size=3, padding='same'),
            layers.BatchNormalization(),
            layers.ReLU(),
            layers.GlobalAveragePooling1D()
        ])

        self.regressor = tf.keras.Sequential([
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(1)
        ])

    def call(self, inputs):
        x = self.feature_extractor(inputs)
        return self.regressor(x)

def prepare_data(
    data_path: Path,
    config: ModelConfig
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, MinMaxScaler]:
    # 读取数据
    df = pd.read_csv(data_path)
    data = df[['open', 'high', 'low', 'close', 'volume']].values

    # 数据标准化
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)

    # 创建序列数据
    X, y = [], []
    for i in range(len(scaled_data) - config.sequence_length):
        X.append(scaled_data[i:(i + config.sequence_length)])
        y.append(scaled_data[i + config.sequence_length, 3])  # 预测收盘价

    X = np.array(X)
    y = np.array(y)

    # 划分训练集和验证集
    train_size = int(len(X) * 0.8)
    X_train, X_val = X[:train_size], X[train_size:]
    y_train, y_val = y[:train_size], y[train_size:]

    return X_train, y_train, X_val, y_val, scaler

def create_model(config: ModelConfig) -> models.Model:
    model = CryptoCNN(config)

    # 编译模型，使用 tensorflow_addons 中的 AdamW 优化器
    optimizer = tfa.optimizers.AdamW(
        learning_rate=config.learning_rate,
        weight_decay=0.01
    )

    model.compile(
        optimizer=optimizer,
        loss='mse',
        metrics=['mae']
    )

    return model

def main():
    # 设置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # 配置参数
    config = ModelConfig()

    # 准备数据
    data_path = Path("crypto_data.csv")
    X_train, y_train, X_val, y_val, scaler = prepare_data(data_path, config)

    # 创建模型
    model = create_model(config)

    # 设置回调函数
    callbacks_list = [
        callbacks.ModelCheckpoint(
            filepath='models/best_model.h5',
            monitor='val_loss',
            save_best_only=True
        ),
        callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            verbose=1
        ),
        callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
    ]

    # 训练模型
    history = model.fit(
        X_train, y_train,
        epochs=config.epochs,
        batch_size=config.batch_size,
        validation_data=(X_val, y_val),
        callbacks=callbacks_list,
        verbose=1
    )

    # 绘制训练历史
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(history.history['mae'], label='Training MAE')
    plt.plot(history.history['val_mae'], label='Validation MAE')
    plt.title('Model MAE')
    plt.xlabel('Epoch')
    plt.ylabel('MAE')
    plt.legend()

    plt.tight_layout()
    plt.savefig('training_history.png')
    plt.close()

    # 保存模型
    model.save('models/final_model.h5')

    logging.info("Training completed successfully!")

def predict(model_path: str, data: np.ndarray, scaler: MinMaxScaler) -> np.ndarray:
    """
    使用保存的模型进行预测
    """
    model = models.load_model(model_path, custom_objects={'AdamW': tfa.optimizers.AdamW})
    scaled_pred = model.predict(data)

    # 反向转换预测结果
    dummy = np.zeros((scaled_pred.shape[0], scaler.n_features_in_))
    dummy[:, 3] = scaled_pred.flatten()  # 3 是收盘价的索引
    predictions = scaler.inverse_transform(dummy)[:, 3]

    return predictions

if __name__ == "__main__":
    main()
